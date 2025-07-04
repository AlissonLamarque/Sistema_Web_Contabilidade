from flask import render_template, url_for, redirect, flash, request, Blueprint
from forms import VendaForm
from models import db, Produto, Cliente, Venda, ItemVenda, MovimentacaoFinanceira
from datetime import datetime

vendas_bp = Blueprint('vendas_bp', __name__, template_folder='templates', static_folder='static')

@vendas_bp.route('/vendas')
def vendas():
    options = [
        db.joinedload(Venda.itens).joinedload(ItemVenda.produto)
    ]
    
    vendas_confirmadas = Venda.query.options(*options)\
        .filter_by(status='Confirmada')\
        .order_by(Venda.data_venda.desc()).all()
    vendas_canceladas = Venda.query.options(*options)\
        .filter_by(status='Cancelada')\
        .order_by(Venda.data_venda.desc()).all()
    
    for venda in vendas_confirmadas:
        for item in venda.itens:
            item.custo_total = item.quantidade * item.produto.preco_compra
    for venda in vendas_canceladas:
        for item in venda.itens:
            item.custo_total = item.quantidade * item.produto.preco_compra

    return render_template('venda/vendas.html', 
                           vendas_confirmadas=vendas_confirmadas, 
                           vendas_canceladas=vendas_canceladas)

@vendas_bp.route('/cadastrar_venda', methods=['GET', 'POST'])
def cadastrar_venda():
    form = VendaForm()
    form.cliente_id.choices = [(c.id, c.nome) for c in Cliente.query.filter_by(status='ativo').all()]
    
    if form.validate_on_submit():
        try:
            produtos_ids = request.form.getlist('produto_id')
            quantidades = request.form.getlist('quantidade')
            precos_unitarios = request.form.getlist('preco_unitario')

            if not produtos_ids:
                flash('Adicione pelo menos um item à venda.', 'danger')
                produtos = Produto.query.filter(Produto.status == 'disponível', Produto.estoque > 0).all()
                return render_template('venda/cadastrar_venda.html', form=form, produtos=produtos)

            valor_total_calculado = 0
            itens_para_adicionar = []
            for produto_id, qtd_str, preco_str in zip(produtos_ids, quantidades, precos_unitarios):
                quantidade = int(qtd_str)
                produto = Produto.query.get(produto_id)
                
                if produto.estoque < quantidade:
                    flash(f'Estoque insuficiente para o produto "{produto.nome}". Disponível: {produto.estoque}', 'danger')
                    produtos_disponiveis = Produto.query.filter(Produto.status == 'disponível', Produto.estoque > 0).all()
                    return render_template('venda/cadastrar_venda.html', form=form, produtos=produtos_disponiveis)
                
                itens_para_adicionar.append({'produto': produto, 'quantidade': quantidade, 'preco': float(preco_str)})
                valor_total_calculado += quantidade * float(preco_str)

            forma_de_pagamento = form.forma_pagamento.data
            status_pagamento_final = 'Pendente'
            if forma_de_pagamento != 'A Prazo':
                status_pagamento_final = 'Pago'

            nova_venda = Venda(
                cliente_id=form.cliente_id.data,
                forma_pagamento=forma_de_pagamento,
                data_venda=form.data_venda.data,
                status_pagamento=status_pagamento_final,
                valor_total=valor_total_calculado
            )
            db.session.add(nova_venda)

            for item_info in itens_para_adicionar:
                item = ItemVenda(
                    venda=nova_venda,
                    produto_id=item_info['produto'].id,
                    quantidade=item_info['quantidade'],
                    preco_unitario=item_info['preco']
                )
                db.session.add(item)
                
                produto = item_info['produto']
                produto.estoque -= item_info['quantidade']
                if produto.estoque <= 0:
                    produto.status = 'indisponível'

            if status_pagamento_final == 'Pago':
                db.session.flush()
                entrada_caixa = MovimentacaoFinanceira(
                    data=nova_venda.data_venda,
                    descricao=f"Recebimento da venda #{nova_venda.id}",
                    valor=abs(nova_venda.valor_total),
                    origem=nova_venda
                )
                db.session.add(entrada_caixa)

            db.session.commit()
            flash('Venda registrada com sucesso!', 'success')
            return redirect(url_for('vendas_bp.vendas'))

        except (ValueError, TypeError) as e:
            db.session.rollback()
            flash(f'Erro nos valores dos itens informados: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro inesperado ao registrar a venda: {str(e)}', 'danger')
    
    produtos_disponiveis = Produto.query.filter(Produto.status == 'disponível', Produto.estoque > 0).all()
    return render_template('venda/cadastrar_venda.html', form=form, produtos=produtos_disponiveis)

@vendas_bp.route('/cancelar_venda/<int:venda_id>', methods=['POST'])
def cancelar_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    
    try:
        for item in venda.itens:
            produto = Produto.query.get(item.produto_id)
            produto.estoque += item.quantidade
            produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'
        
        venda.status = 'Cancelada'
        db.session.commit()
        
        flash('Venda cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar venda: {str(e)}', 'danger')
    
    return redirect(url_for('vendas_bp.vendas'))

@vendas_bp.route('/excluir_venda/<int:venda_id>', methods=['POST'])
def excluir_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    
    try:
        for item in venda.itens:
            produto = Produto.query.get(item.produto_id)
            produto.estoque += item.quantidade
            produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'
        
        db.session.delete(venda)
        db.session.commit()
        
        flash('Venda excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir venda: {str(e)}', 'danger')
    
    return redirect(url_for('vendas_bp.vendas'))

@vendas_bp.route('/receber_venda/<int:venda_id>', methods=['POST'])
def receber_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    
    if venda.status_pagamento == 'Pendente':
        try:
            venda.status_pagamento = 'Pago'

            entrada_caixa = MovimentacaoFinanceira(
                data=datetime.utcnow(),
                descricao=f'Recebimento da venda a prazo #{venda.id}',
                valor=abs(venda.valor_total),
                origem=venda
            )
            db.session.add(entrada_caixa)
            
            db.session.commit()
            flash('Venda marcada como recebida com sucesso!', 'success')

        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao marcar venda como recebida: {str(e)}', 'danger')
    else:
        flash('Esta venda já foi marcada como recebida.', 'info')
    
    return redirect(url_for('vendas_bp.vendas'))