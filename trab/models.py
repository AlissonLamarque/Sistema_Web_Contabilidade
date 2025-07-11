from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='indisponível')

    compras = db.relationship('Item_compra', backref='produto', lazy=True)
    vendas = db.relationship('Item_venda', backref='produto', lazy=True)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    status = db.Column(db.String(10), nullable=False, default='ativo')

    vendas = db.relationship('Venda', backref='cliente', lazy=True)

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False, unique=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    status = db.Column(db.String(10), nullable=False, default='ativo')

    compras = db.relationship('Compra', backref='fornecedor', lazy=True)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    nf_entrada = db.Column(db.String(50), nullable=False)
    data_compra = db.Column(db.DateTime, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmada')

    itens = db.relationship('Item_compra', backref='compra', lazy=True, cascade="all, delete-orphan")

class Item_compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    data_venda = db.Column(db.DateTime, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='confirmada')

    itens = db.relationship('Item_venda', backref='venda', lazy=True, cascade="all, delete-orphan")

class Item_venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)