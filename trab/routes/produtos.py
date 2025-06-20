from flask import render_template, url_for, redirect, flash, Blueprint
from forms import ProdutoForm
from models import db, Produto

produtos_bp = Blueprint('produtos_bp', __name__, template_folder='templates', static_folder='static')

@produtos_bp.route("/produtos")
def produtos():
    produtos_disponiveis = Produto.query.filter_by(status='disponivel').order_by(Produto.nome).all()
    produtos_indisponiveis = Produto.query.filter_by(status='indisponivel').order_by(Produto.nome).all()
    return render_template('produto/produtos.html', 
                           produtos_disponiveis=produtos_disponiveis,
                           produtos_indisponiveis=produtos_indisponiveis)

@produtos_bp.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    form = ProdutoForm()
    if form.validate_on_submit():
        produto = Produto(
            nome = form.nome.data,
            preco_compra = form.preco_compra.data,
            preco_venda = form.preco_venda.data,
        )
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos_bp.produtos'))
    return render_template('produto/cadastrar_produto.html', form=form)

@produtos_bp.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = ProdutoForm(obj=produto)
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.preco_compra = form.preco_compra.data
        produto.preco_venda = form.preco_venda.data
        produto.status = form.status.data
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos_bp.produtos'))
    return render_template('produto/cadastrar_produto.html', form=form, titulo='Editar Produto')
