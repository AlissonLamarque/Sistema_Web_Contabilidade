from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    preco_venda = FloatField('Preço de Venda', validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('disponível', 'Disponível'), ('indisponível', 'Indisponível')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

class CompraForm(FlaskForm):
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()], choices=[])
    nf_entrada = StringField('NF Entrada', validators=[DataRequired()])
    data_compra = StringField('Data da Compra', validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Compra')

class VendaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()], choices=[])
    forma_pagamento = SelectField('Forma de Pagamento',
                                choices=[('vista', 'À Vista'), ('prazo', 'A Prazo')],
                                validators=[DataRequired()])
    data_venda = StringField('Data da Venda', validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
                       validators=[DataRequired()])
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