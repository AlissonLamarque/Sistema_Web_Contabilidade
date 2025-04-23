'''
from flask import Blueprint, render_template, redirect, url_for, request
from models import db, Produto, Cliente, Fornecedor
from forms import ProdutoForm, ClienteForm, FornecedorForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@bp.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome=form.nome.data,
            preco_compra=form.preco_compra.data,
            preco_venda=form.preco_venda.data,
            icms_credito=form.icms_credito.data,
            icms_debito=form.icms_debito.data,
        )
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('cadastrar_produto.html', form=form)

@bp.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            cpf=form.cpf.data,
            cidade=form.cidade.data,
            estado=form.estado.data
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('cadastrar_cliente.html', form=form)

@bp.route('/cadastrar_fornecedor', methods=['GET', 'POST'])
def cadastrar_fornecedor():
    form = FornecedorForm()
    if form.validate_on_submit():
        fornecedor = Fornecedor(
            nome=form.nome.data,
            cnpj=form.cnpj.data,
            cidade=form.cidade.data,
            estado=form.estado.data
        )
        db.session.add(fornecedor)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('cadastrar_fornecedor.html', form=form)
'''