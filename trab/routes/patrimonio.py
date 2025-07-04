from flask import render_template, url_for, redirect, flash, Blueprint
from forms import CompraPatrimonioForm
from models import db, CompraPatrimonio

patrimonio_bp = Blueprint('patrimonio_bp', __name__, template_folder='templates', static_folder='static')

@patrimonio_bp.route('/bens')
def bens():
    bens_ativos = CompraPatrimonio.query.order_by(CompraPatrimonio.nome).all()
    return render_template('patrimonio/bens.html',  bens_ativos=bens_ativos)

@patrimonio_bp.route('/comprar_bem', methods=['GET', 'POST'])
def comprar_bem():
    form = CompraPatrimonioForm()
    
    forma_de_pagamento = form.forma_pagamento.data
    
    if forma_de_pagamento != 'prazo':
            status_pagamento = 'Pago'
    
    if form.validate_on_submit():
        try:
            novo_bem = CompraPatrimonio(
                nome=form.nome.data,
                descricao=form.descricao.data,
                valor=form.valor.data,
                data_compra=form.data_compra.data,
                forma_pagamento=form.forma_pagamento.data
            )
            
            db.session.add(novo_bem)
            db.session.commit()
            
            flash('Bem patrimonial adquirido com sucesso!', 'success')
            return redirect(url_for('patrimonio_bp.bens'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao comprar o bem: {str(e)}', 'danger')

    return render_template('patrimonio/comprar_patrimonio.html', form=form, titulo='Comprar Bem Patrimonial')