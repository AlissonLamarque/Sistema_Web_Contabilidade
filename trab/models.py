'''
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco_compra = db.Column(db.Float, nullable=False)
    preco_venda = db.Column(db.Float, nullable=False)
    icms_credito = db.Column(db.Float, default=0.0)
    icms_debito = db.Column(db.Float, default=0.0)

    def calcular_custo(self):
        return self.preco_compra + (self.preco_compra * (self.icms_debito / 100))

    def calcular_lucro(self):
        return self.preco_venda - self.calcular_custo()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    tipo_pagamento = db.Column(db.String(10), nullable=False)  # 'avista' ou 'aprazo'
    quantidade = db.Column(db.Integer, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float)
'''