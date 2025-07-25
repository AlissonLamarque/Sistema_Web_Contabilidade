from flask import render_template, url_for, redirect, flash, Blueprint
from forms import CompraPatrimonioForm
from models import db, CompraPatrimonio, MovimentacaoFinanceira
from sqlalchemy import func

patrimonio_bp = Blueprint('patrimonio_bp', __name__, template_folder='templates', static_folder='static')

@patrimonio_bp.route('/bens')
def bens():
    bens_ativos = CompraPatrimonio.query.filter_by(status='Ativo').order_by(CompraPatrimonio.nome).all()
    bens_manutencao = CompraPatrimonio.query.filter_by(status='Manutencao').order_by(CompraPatrimonio.nome).all()

    return render_template('patrimonio/bens.html', 
                           bens_ativos=bens_ativos,
                           bens_manutencao=bens_manutencao)

@patrimonio_bp.route('/comprar_bem', methods=['GET', 'POST'])
def comprar_bem():
    form = CompraPatrimonioForm()
    
    forma_de_pagamento = form.forma_pagamento.data
    valor_da_compra = form.valor.data
    
    if forma_de_pagamento != 'prazo':
            status_pagamento = 'Pago'
            
    if forma_de_pagamento != 'prazo':
                saldo_caixa = db.session.query(func.sum(MovimentacaoFinanceira.valor)).scalar() or 0.0
                if saldo_caixa < valor_da_compra:
                    flash(f'Saldo em caixa (R$ {saldo_caixa:.2f}) é insuficiente para esta compra.', 'danger')
                    return render_template('patrimonio/comprar_patrimonio.html', form=form, titulo='Comprar Bem Patrimonial')
    
    if form.validate_on_submit():
        try:
            novo_bem = CompraPatrimonio(
                nome=form.nome.data,
                descricao=form.descricao.data,
                valor=form.valor.data,
                data_compra=form.data_compra.data,
                forma_pagamento=form.forma_pagamento.data,
                status_pagamento=status_pagamento
            )
            
            db.session.add(novo_bem)
            
            if status_pagamento == 'Pago':
                db.session.flush()

                saida_caixa = MovimentacaoFinanceira(
                    data=novo_bem.data_compra,
                    descricao=f'Pagamento do bem patrimonial: {novo_bem.nome}',
                    valor=-abs(valor_da_compra),
                    origem=novo_bem
                )
                db.session.add(saida_caixa)
            
            db.session.commit()
            
            flash('Bem patrimonial adquirido com sucesso!', 'success')
            return redirect(url_for('patrimonio_bp.bens'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao comprar o bem: {str(e)}', 'danger')

    return render_template('patrimonio/comprar_patrimonio.html', form=form, titulo='Comprar Bem Patrimonial')

@patrimonio_bp.route('/bem/<int:bem_id>/manutencao', methods=['POST'])
def mover_para_manutencao(bem_id):
    bem = CompraPatrimonio.query.get_or_404(bem_id)
    
    if bem.status == 'Ativo':
        try:
            bem.status = 'Manutencao'
            db.session.commit()
            flash(f'O bem "{bem.nome}" foi movido para manutenção.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o status do bem: {str(e)}', 'danger')
    else:
        flash(f'O bem "{bem.nome}" não está com status "ativo" para ser movido para manutenção.', 'warning')
        
    return redirect(url_for('patrimonio_bp.bens'))

@patrimonio_bp.route('/bem/<int:bem_id>/ativar', methods=['POST'])
def retornar_ativo(bem_id):
    bem = CompraPatrimonio.query.get_or_404(bem_id)
    
    if bem.status == 'Manutencao':
        try:
            bem.status = 'Ativo'
            db.session.commit()
            flash(f'O bem "{bem.nome}" foi reativado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao reativar o bem: {str(e)}', 'danger')
    else:
        flash(f'O bem "{bem.nome}" não está em manutenção para ser reativado.', 'warning')
        
    return redirect(url_for('patrimonio_bp.bens'))

@patrimonio_bp.route('/bem/<int:bem_id>/excluir', methods=['POST'])
def excluir_bem(bem_id):
    bem = CompraPatrimonio.query.get_or_404(bem_id)
    
    if bem.status == 'Manutencao':
        try:
            db.session.delete(bem)
            db.session.commit()
            flash(f'O bem "{bem.nome}" foi excluído com sucesso.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir o bem: {str(e)}', 'danger')
    else:
        flash(f'O bem "{bem.nome}" só pode ser excluído se estiver em manutenção.', 'danger')
        
    return redirect(url_for('patrimonio_bp.bens'))