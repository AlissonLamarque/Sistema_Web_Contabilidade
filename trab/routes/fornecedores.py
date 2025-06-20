from flask import render_template, url_for, redirect, flash, Blueprint
from forms import FornecedorForm
from models import db, Fornecedor

fornecedores_bp = Blueprint('fornecedores_bp', __name__, template_folder='templates', static_folder='static')

@fornecedores_bp.route('/fornecedores')
def fornecedores():
    fornecedores_ativos = Fornecedor.query.filter_by(status='ativo').order_by(Fornecedor.nome).all()
    fornecedores_inativos = Fornecedor.query.filter_by(status='inativo').order_by(Fornecedor.nome).all()
    return render_template('fornecedor/fornecedores.html', 
                           fornecedores_ativos=fornecedores_ativos, 
                           fornecedores_inativos=fornecedores_inativos)

@fornecedores_bp.route('/cadastrar_fornecedor', methods=['GET', 'POST'])
def cadastrar_fornecedor():
    form = FornecedorForm()
    if form.validate_on_submit():
        fornecedor = Fornecedor(
            nome = form.nome.data,
            cnpj = form.cnpj.data,
            cidade = form.cidade.data,
            estado = form.estado.data,
            status = form.status.data
        )
        db.session.add(fornecedor)
        db.session.commit()
        flash('Fornecedor cadastrado com sucesso!', 'success')
        return redirect(url_for('fornecedores_bp.fornecedores'))
    return render_template('fornecedor/cadastrar_fornecedor.html', form=form)

@fornecedores_bp.route('/editar_fornecedor/<int:fornecedor_id>', methods=['GET', 'POST'])
def editar_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
    form = FornecedorForm(obj=fornecedor)
    if form.validate_on_submit():
        fornecedor.nome = form.nome.data
        fornecedor.cnpj = form.cnpj.data
        fornecedor.cidade = form.cidade.data
        fornecedor.estado = form.estado.data
        fornecedor.status = form.status.data
        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('fornecedores_bp.fornecedores'))
    return render_template('fornecedor/cadastrar_fornecedor.html', form=form, titulo='Editar Fornecedor')
