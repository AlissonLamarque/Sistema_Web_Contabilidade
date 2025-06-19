from flask import render_template, url_for, redirect, flash, request, Blueprint
from forms import ProdutoForm, ClienteForm, FornecedorForm, CompraForm, VendaForm
from models import db, Produto, Cliente, Fornecedor, Compra, Item_compra, Venda, Item_venda

vendas_bp = Blueprint('vendas_bp', __name__, template_folder='templates', static_folder='static')

@vendas_bp.route('/vendas')
def vendas():
    vendas = Venda.query.options(
        db.joinedload(Venda.cliente),
        db.joinedload(Venda.itens).joinedload(Item_venda.produto)).all()
    
    for venda in vendas:
        for item in venda.itens:
            item.custo_total = item.quantidade * item.produto.preco_compra
    return render_template('venda/vendas.html', vendas=vendas)

@vendas_bp.route('/cadastrar_venda', methods=['GET', 'POST'])
def cadastrar_venda():
    form = VendaForm()
    form.cliente_id.choices = [(c.id, c.nome) for c in Cliente.query.filter_by(status='ativo').all()]
    produtos = Produto.query.filter(
        Produto.status == 'disponível',
        Produto.estoque > 0
    ).all()
    
    if request.method == 'POST':
        try:
            cliente_id = form.cliente_id.data
            forma_pagamento = form.forma_pagamento.data
            data_venda = form.data_venda.data

            if not all([cliente_id, forma_pagamento, data_venda]):
                flash('Preencha todos os campos obrigatórios', 'danger')
                return redirect(url_for('cadastrar_venda'))

            nova_venda = Venda(
                cliente_id=form.cliente_id.data,
                forma_pagamento=form.forma_pagamento.data,
                data_venda=form.data_venda.data,
                valor_total=0.0,
            )
            db.session.add(nova_venda)
            db.session.flush()
            
            valor_total = 0.0
            produtos_ids = request.form.getlist('produto_id')
            quantidades = request.form.getlist('quantidade')
            precos_unitarios = request.form.getlist('preco_unitario')

            if not produtos_ids:
                flash('Adicione pelo menos um item à venda', 'danger')
                db.session.rollback()
                return redirect(url_for('cadastrar_venda'))
            
            for produto_id, quantidade, preco_unitario in zip(produtos_ids, quantidades, precos_unitarios):
                if not all([produto_id, quantidade, preco_unitario]):
                    continue
                
                quantidade = int(quantidade)
                preco_unitario = float(preco_unitario)
                produto = Produto.query.get(produto_id)

                if produto.estoque < quantidade:
                    flash(f'Estoque insuficiente para {produto.nome}', 'danger')
                    db.session.rollback()
                    return redirect(url_for('cadastrar_venda'))

                item = Item_venda(
                    venda_id=nova_venda.id,
                    produto_id=produto_id,
                    quantidade=quantidade,
                    preco_unitario=preco_unitario
                )
                db.session.add(item)

                produto.estoque -= quantidade
                if produto.estoque <= 0:
                    produto.status = 'indisponível'

                valor_total += quantidade * preco_unitario

            nova_venda.valor_total = valor_total
            db.session.commit()
            flash('Venda registrada com sucesso!', 'success')
            return redirect(url_for('vendas_bp.vendas'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar venda: {str(e)}', 'danger')
            vendas_bp.logger.error(f"Erro em cadastrar_venda: {str(e)}", exc_info=True)
    
    return render_template('venda/cadastrar_venda.html', form=form, produtos=produtos)

@vendas_bp.route('/cancelar_venda/<int:venda_id>', methods=['POST'])
def cancelar_venda(venda_id):
    venda = Venda.query.get_or_404(venda_id)
    
    try:
        for item in venda.itens:
            produto = Produto.query.get(item.produto_id)
            produto.estoque += item.quantidade
            produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'
        
        venda.status = 'cancelada'
        db.session.commit()
        
        flash('Venda cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar venda: {str(e)}', 'danger')
    
    return redirect(url_for('vendas_bp.vendas'))