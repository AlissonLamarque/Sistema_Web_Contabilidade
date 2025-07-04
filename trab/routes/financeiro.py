from flask import render_template, redirect, url_for, flash, Blueprint
from forms import CapitalSocialForm
from models import db, MovimentacaoFinanceira
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
            return redirect(url_for('financeiro_bp.movimentacoes_financeiras')) 
        
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar o capital social: {str(e)}', 'danger')
            
    return render_template('financeiro/capital_social.html', form=form, titulo='Registrar Capital Social')

@financeiro_bp.route('/movimentacoes')
def movimentacoes_financeiras():
    movimentacoes = MovimentacaoFinanceira.query.order_by(MovimentacaoFinanceira.data.desc()).all()
    return render_template('financeiro/movimentacoes.html', movimentacoes=movimentacoes)

@financeiro_bp.app_context_processor
def inject_financial_data():
    saldo_caixa = db.session.query(func.sum(MovimentacaoFinanceira.valor)).scalar()
    return dict(saldo_caixa=saldo_caixa)