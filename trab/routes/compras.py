from flask import render_template, url_for, redirect, flash, request, Blueprint
from forms import CompraForm
from models import db, Produto, Fornecedor, Compra, ItemCompra, MovimentacaoFinanceira
from datetime import datetime
from sqlalchemy import func

compras_bp = Blueprint('compras_bp', __name__, template_folder='templates', static_folder='static')

@compras_bp.route('/compras')
def compras():
    options = [
        db.joinedload(Compra.itens).joinedload(ItemCompra.produto)
    ]
    
    compras_confirmadas = Compra.query.options(*options)\
        .filter_by(status='Confirmada')\
        .order_by(Compra.data_compra.desc()).all()
    compras_canceladas = Compra.query.options(*options)\
        .filter_by(status='Cancelada')\
        .order_by(Compra.data_compra.desc()).all()
    
    for compra in compras_confirmadas:
        for item in compra.itens:
            item.custo_total = item.quantidade * item.produto.preco_compra
    for compra in compras_canceladas:
        for item in compra.itens:
            item.custo_total = item.quantidade * item.produto.preco_compra
    
    return render_template('compra/compras.html', 
                           compras_confirmadas=compras_confirmadas,
                           compras_canceladas=compras_canceladas)

@compras_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_compra():
    form = CompraForm()
    fornecedores = Fornecedor.query.filter_by(status='ativo').all()
    form.fornecedor_id.choices = [(f.id, f"{f.nome} - {f.cnpj}") for f in fornecedores]
    produtos = Produto.query.all()
    
    if request.method == 'POST':
        try:
            if not all([form.fornecedor_id.data, form.forma_pagamento.data, form.data_compra.data]):
                flash('Preencha todos os campos obrigatórios do cabeçalho', 'danger')
                return render_template('compra/cadastrar_compra.html', form=form, produtos=produtos)

            forma_de_pagamento = form.forma_pagamento.data
            
            produtos_ids = request.form.getlist('produto_id')
            quantidades = request.form.getlist('quantidade')
            precos_unitarios = request.form.getlist('preco_unitario')

            if not produtos_ids:
                flash('Adicione pelo menos um item à compra.', 'danger')
                return render_template('compra/cadastrar_compra.html', form=form, produtos=produtos)

            valor_total_calculado = sum(int(q) * float(p) for q, p in zip(quantidades, precos_unitarios))

            if forma_de_pagamento != 'A Prazo':
                saldo_caixa = db.session.query(func.sum(MovimentacaoFinanceira.valor)).scalar() or 0.0
                
                if saldo_caixa < valor_total_calculado:
                    flash(f'Saldo em caixa (R$ {saldo_caixa:.2f}) é insuficiente para esta compra de R$ {valor_total_calculado:.2f}.', 'danger')
                    return render_template('compra/cadastrar_compra.html', form=form, produtos=produtos)
            
            status_pagamento_final = 'Pago' if forma_de_pagamento != 'A Prazo' else 'Pendente'

            nova_compra = Compra(
                fornecedor_id=form.fornecedor_id.data,
                forma_pagamento=forma_de_pagamento,
                data_compra=form.data_compra.data,
                status_pagamento=status_pagamento_final,
                valor_total=valor_total_calculado
            )
            db.session.add(nova_compra)
            
            for i in range(len(produtos_ids)):
                produto = Produto.query.get(produtos_ids[i])
                if not produto: continue

                item = ItemCompra(
                    compra=nova_compra,
                    produto_id=produtos_ids[i],
                    quantidade=int(quantidades[i]),
                    preco_unitario=float(precos_unitarios[i])
                )
                db.session.add(item)
                
                produto.estoque += int(quantidades[i])
                produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'

            if status_pagamento_final == 'Pago':
                db.session.flush()

                saida_caixa = MovimentacaoFinanceira(
                    data=nova_compra.data_compra,
                    descricao=f'Pagamento da compra #{nova_compra.id}',
                    valor=-abs(nova_compra.valor_total),
                    origem=nova_compra
                )
                db.session.add(saida_caixa)

            db.session.commit()
            flash('Compra registrada com sucesso!', 'success')
            return redirect(url_for('compras_bp.compras'))

        except (ValueError, TypeError) as e:
            db.session.rollback()
            flash(f'Erro nos valores informados: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar compra: {str(e)}', 'danger')

    return render_template('compra/cadastrar_compra.html', form=form, produtos=produtos)

@compras_bp.route('/cancelar_compra/<int:compra_id>', methods=['POST'])
def cancelar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    
    try:
        for item in compra.itens:
            produto = Produto.query.get(item.produto_id)
            produto.estoque -= item.quantidade
            produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'
        
        compra.status = 'Cancelada'
        db.session.commit()
        flash('Compra cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar compra: {str(e)}', 'danger')
    
    return redirect(url_for('compras_bp.compras'))

@compras_bp.route('/excluir_compra/<int:compra_id>', methods=['POST'])
def excluir_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    
    try:
        db.session.delete(compra)
        db.session.commit()
        flash('Compra excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir compra: {str(e)}', 'danger')
    
    return redirect(url_for('compras_bp.compras'))

@compras_bp.route('/pagar_compra/<int:compra_id>', methods=['POST'])
def pagar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)

    if compra.status_pagamento == 'Pendente':
        try:
            compra.status_pagamento = 'Pago'
            
            saida_caixa = MovimentacaoFinanceira(
                data=datetime.utcnow(),
                descricao=f'Pagamento da compra #{compra.id} (Fornecedor: {compra.fornecedor.nome})',
                valor=-abs(compra.valor_total),
                origem=compra 
            )
            db.session.add(saida_caixa)
            
            
            db.session.commit()
            flash(f'Pagamento da compra #{compra.id} registrado com sucesso!', 'success')
        
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao processar o pagamento: {str(e)}', 'danger')
    
    else:
        flash('Esta compra já estava com o status "Pago".', 'info')

    return redirect(url_for('compras_bp.compras'))