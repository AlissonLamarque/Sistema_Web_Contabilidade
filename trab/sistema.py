from flask import Flask, render_template, url_for, redirect, request
from forms import ProdutoForm
from models import db, Produto

app = Flask(__name__)

app.config['SECRET_KEY'] = 'minha_chave_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:laboratorio@localhost/sistemadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


produtos = [
    {
        'nome' : 'Televisão',
        'preco' : 3000.00
    },
    {
        'nome' : 'Geladeira',
        'preco' : 4000.00
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', produtos=produtos)

@app.route("/about")
def about():
    return render_template('about.html', titulo="Teste")

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
        return redirect(url_for('home'))
    return render_template('cadastrar_produto.html', form=form)

if (__name__) == '__main__':
    app.run(debug=True)

with app.app_context():
    db.create_all()