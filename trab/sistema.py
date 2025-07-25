from flask import Flask
from flask_migrate import Migrate
from models import db

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'minha_chave_super_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:laboratorio@localhost/sistemadb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from routes.base import base_bp
    from routes.clientes import clientes_bp
    from routes.compras import compras_bp
    from routes.fornecedores import fornecedores_bp
    from routes.produtos import produtos_bp
    from routes.vendas import vendas_bp
    from routes.financeiro import financeiro_bp
    from routes.patrimonio import patrimonio_bp
    
    app.register_blueprint(base_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(fornecedores_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(financeiro_bp)
    app.register_blueprint(patrimonio_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)