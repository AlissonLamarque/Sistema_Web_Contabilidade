from flask import render_template, url_for, redirect, flash, Blueprint
from forms import ClienteForm
from models import db, Cliente

clientes_bp = Blueprint('clientes_bp', __name__, template_folder='templates', static_folder='static')

@clientes_bp.route('/clientes')
def clientes():
    clientes_ativos = Cliente.query.filter_by(status='ativo').order_by(Cliente.nome).all()
    clientes_inativos = Cliente.query.filter_by(status='inativo').order_by(Cliente.nome).all()
    return render_template('cliente/clientes.html', 
                           clientes_ativos=clientes_ativos, 
                           clientes_inativos=clientes_inativos)

@clientes_bp.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome = form.nome.data,
            cpf = form.cpf.data,
            cidade = form.cidade.data,
            estado = form.estado.data,
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('clientes_bp.clientes'))
    return render_template('cliente/cadastrar_cliente.html', form=form)

@clientes_bp.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.cpf = form.cpf.data
        cliente.cidade = form.cidade.data
        cliente.estado = form.estado.data
        cliente.status = form.status.data
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('clientes_bp.clientes'))
    return render_template('cliente/cadastrar_cliente.html', form=form, titulo='Editar Cliente')
