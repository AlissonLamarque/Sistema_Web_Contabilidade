from flask import Flask, render_template, url_for, redirect, request, flash
from forms import ProdutoForm, ClienteForm
from models import db, Produto, Cliente

app = Flask(__name__)

app.config['SECRET_KEY'] = 'minha_chave_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:laboratorio@localhost/sistemadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# PRODUTOS

@app.route("/")
@app.route("/produtos")
def produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

@app.route('/cadastrar_produto', methods=['GET', 'POST'])
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
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    return render_template('cadastrar_produto.html', form=form)

@app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.preco_compra = form.preco_compra.data
        produto.preco_venda = form.preco_venda.data
        produto.icms_credito = form.icms_credito.data
        produto.icms_debito = form.icms_debito.data
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    return render_template('cadastrar_produto.html', form=form, titulo='Editar Produto')

@app.route('/excluir_produto/<int:produto_id>', methods=['POST'])
def excluir_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produtos'))

# CLIENTES

@app.route('/clientes')
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            endereco=form.endereco.data
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_clientes'))
    return render_template('cadastrar_cliente.html', form=form)

@app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.email = form.email.data
        cliente.telefone = form.telefone.data
        cliente.endereco = form.endereco.data
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
        return redirect(url_for('listar_clientes'))
    return render_template('cadastrar_cliente.html', form=form, titulo='Editar Cliente')


@app.route('/excluir_cliente/<int:cliente_id>', methods=['POST'])
def excluir_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente excluído com sucesso!', 'success')
    return redirect(url_for('listar_clientes'))

if (__name__) == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()