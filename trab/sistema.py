from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

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

if (__name__) == '__main__':
    app.run(debug=True)


'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes import main
import os

# Inicialização da aplicação
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização de extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registro das rotas
app.register_blueprint(main)

# Importa os modelos para que o Migrate funcione corretamente
from models import Produto, Cliente, Fornecedor

# Execução
if __name__ == '__main__':
    app.run(debug=True)
'''