from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length

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