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
    
    from routes import init_app
    init_app(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)