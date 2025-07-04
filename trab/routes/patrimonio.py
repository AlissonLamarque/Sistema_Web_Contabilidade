from flask import render_template, url_for, redirect, flash, Blueprint
from forms import PatrimonioForm, EditarPatrimonioForm, CompraPatrimonioForm
from models import db, Patrimonio, CompraPatrimonio, Fornecedor

patrimonio_bp = Blueprint('patrimonio_bp', __name__, template_folder='templates', static_folder='static')

@patrimonio_bp.route('/bens')
def bens():
    bens_ativos = Patrimonio.query.filter_by(status='ativo').order_by(Patrimonio.nome).all()
    bens_manutencao = Patrimonio.query.filter_by(status='manutencao').order_by(Patrimonio.nome).all()
    bens_vendidos = Patrimonio.query.filter_by(status='vendido').order_by(Patrimonio.nome).all()
    return render_template('patrimonio/bens.html',  
                           bens_ativos=bens_ativos, 
                           bens_manutencao=bens_manutencao, 
                           bens_vendidos=bens_vendidos)

@patrimonio_bp.route('/comprar_bem', methods=['GET', 'POST'])
def comprar_bem():
    form = PatrimonioForm()
    
    if form.validate_on_submit():
        try:
            novo_bem = Patrimonio(
                nome=form.nome.data,
                descricao=form.descricao.data,
                valor=form.valor.data,
                data_aquisicao=form.data_aquisicao.data
            )
            
            db.session.add(novo_bem)
            db.session.commit()
            
            flash('Bem patrimonial adquirido com sucesso!', 'success')
            return redirect(url_for('patrimonio_bp.bens'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ocorreu um erro ao comprar o bem: {str(e)}', 'danger')

    return render_template('patrimonio/comprar_patrimonio.html', form=form, titulo='Comprar Bem Patrimonial')