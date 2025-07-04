from flask import render_template, redirect, url_for, flash, Blueprint
from forms import CapitalSocialForm
from models import db, MovimentacaoFinanceira, Produto, Compra, Venda, CompraPatrimonio
from sqlalchemy import func
from datetime import datetime

financeiro_bp = Blueprint('financeiro_bp', __name__, template_folder='templates')

@financeiro_bp.route('/capital-social', methods=['GET', 'POST'])
def capital_social():
    form = CapitalSocialForm()
    if form.validate_on_submit():
        try:
            nova_movimentacao = MovimentacaoFinanceira(
                data=form.data.data,
                descricao=form.descricao.data,
                valor=form.valor.data,
                origem_tipo='Capital Social',
                origem_id=None
            )
            db.session.add(nova_movimentacao)
            db.session.commit()

            flash('Capital Social registrado com sucesso!', 'success')
            return redirect(url_for('financeiro_bp.movimentacoes')) 
        
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar o capital social: {str(e)}', 'danger')
            
    return render_template('financeiro/capital_social.html', form=form, titulo='Registrar Capital Social')

@financeiro_bp.route('/movimentacoes')
def movimentacoes():
    total_entradas = db.session.query(func.sum(MovimentacaoFinanceira.valor)).filter(MovimentacaoFinanceira.valor > 0).scalar() or 0.0
    total_saidas = db.session.query(func.sum(MovimentacaoFinanceira.valor)).filter(MovimentacaoFinanceira.valor < 0).scalar() or 0.0
    saldo_caixa = total_entradas + total_saidas

    total_compras_a_pagar = db.session.query(func.sum(Compra.valor_total)).filter(Compra.status_pagamento == 'Pendente').scalar() or 0.0
    total_patrimonio_a_pagar = db.session.query(func.sum(CompraPatrimonio.valor)).filter(CompraPatrimonio.status_pagamento == 'Pendente').scalar() or 0.0
    contas_a_pagar = total_compras_a_pagar + total_patrimonio_a_pagar

    contas_a_receber = db.session.query(func.sum(Venda.valor_total)).filter(Venda.status_pagamento == 'Pendente').scalar() or 0.0

    valor_total_bens = db.session.query(func.sum(CompraPatrimonio.valor)).filter(CompraPatrimonio.status != 'Manutencao').scalar() or 0.0
    valor_total_estoque = db.session.query(func.sum(Produto.preco_compra * Produto.estoque)).scalar() or 0.0
    saldo_patrimonio = valor_total_bens + valor_total_estoque

    movimentacoes = MovimentacaoFinanceira.query.order_by(MovimentacaoFinanceira.data.desc()).all()

    return render_template('financeiro/movimentacoes.html', 
                           movimentacoes=movimentacoes,
                           total_entradas=total_entradas,
                           total_saidas=total_saidas,
                           saldo_caixa=saldo_caixa,
                           contas_a_pagar=contas_a_pagar,
                           contas_a_receber=contas_a_receber,
                           saldo_patrimonio=saldo_patrimonio,
                           titulo="Movimentações Financeiras")

@financeiro_bp.app_context_processor
def inject_financial_data():
    saldo_caixa = db.session.query(func.sum(MovimentacaoFinanceira.valor)).scalar() or 0.0

    valor_total_bens = db.session.query(func.sum(CompraPatrimonio.valor))\
        .filter(CompraPatrimonio.status != 'Manutencao').scalar() or 0.0
    
    valor_total_estoque = db.session.query(func.sum(Produto.preco_compra * Produto.estoque)).scalar() or 0.0
    
    saldo_patrimonio = valor_total_bens + valor_total_estoque

    return dict(
        saldo_caixa=saldo_caixa,
        saldo_patrimonio=saldo_patrimonio
    )