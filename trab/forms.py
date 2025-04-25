from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    preco_venda = FloatField('Preço de Venda', validators=[DataRequired()])
    icms_credito = FloatField('ICMS Crédito')
    icms_debito = FloatField('ICMS Débito')
    submit = SubmitField('Cadastrar Produto')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cpf = StringField('CPF', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')

class CompraForm(FlaskForm):
    fornecedor_id = StringField('Fornecedor ID', validators=[DataRequired()])
    nf_entrada = StringField('NF Entrada', validators=[DataRequired()])
    data_compra = StringField('Data da Compra', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Compra')

class VendaForm(FlaskForm):
    cliente_id = StringField('Cliente ID', validators=[DataRequired()])
    forma_pagamento = StringField('Forma de Pagamento', validators=[DataRequired()])
    data_venda = StringField('Data da Venda', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Venda')

class ItemCompraForm(FlaskForm):
    compra_id = StringField('Compra ID', validators=[DataRequired()])
    produto_id = StringField('Produto ID', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    preco_unitario = FloatField('Preço Unitário', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Cadastrar Item de Compra')

class ItemVendaForm(FlaskForm):
    venda_id = StringField('Venda ID', validators=[DataRequired()])
    produto_id = StringField('Produto ID', validators=[DataRequired()])
    quantidade = FloatField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    preco_unitario = FloatField('Preço Unitário', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Cadastrar Item de Venda')