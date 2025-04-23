'''
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    preco_venda = FloatField('Preço de Venda', validators=[DataRequired()])
    icms_credito = FloatField('ICMS Crédito')
    icms_debito = FloatField('ICMS Débito')
    submit = SubmitField('Cadastrar')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    submit = SubmitField('Cadastrar')

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    submit = SubmitField('Cadastrar')
'''