from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

# Forms Básicos

## Define o formulário para cadastro de produtos
class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    preco_venda = FloatField('Preço de Venda', validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('disponível', 'Disponível'), ('indisponível', 'Indisponível')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

## Define o formulário para cadastro de clientes
class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

## Define o formulário para cadastro de fornecedores
class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

# Forms de Compras e Vendas

## Define o formulário para cadastro de compras
class CompraForm(FlaskForm):
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()], choices=[])
    forma_pagamento = SelectField('Forma de Pagamento',
                                choices=[('vista', 'À Vista'), ('prazo', 'A Prazo')],
                                validators=[DataRequired()])
    data_compra = StringField('Data da Compra', validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
                       validators=[DataRequired()])
    submit = SubmitField('Cadastrar Compra')

## Define o formulário para cadastro de vendas
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

# Forms de Patrimônio e Movimentação Financeira

## Define o formulário para cadastro de bem patrimonial
class PatrimonioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    data_aquisicao = StringField('Data de Aquisição', validators=[DataRequired()])
    status = SelectField('Status', choices=[('ativo', 'Ativo'), ('manutencao', 'Em Manutenção'), ('vendido', 'Vendido')],
                        validators=[DataRequired()])
    submit = SubmitField('Cadastrar Bem Patrimonial')

## Define o formulário para compra de bem patrimonial
class CompraPatrimonioForm(FlaskForm):
    patrimonio_id = SelectField('Bem Patrimonial', coerce=int, validators=[DataRequired()], choices=[])
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()], choices=[])
    data_compra = StringField('Data da Compra', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    forma_pagamento = SelectField('Forma de Pagamento',
                                choices=[('vista', 'À Vista'), ('prazo', 'A Prazo')],
                                validators=[DataRequired()])
    status = SelectField('Status', 
                       choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
                       validators=[DataRequired()])
    submit = SubmitField('Registrar Compra de Patrimônio')

## Define o formulário para ação de inserir o capital inicial
class CapitalSocialForm(FlaskForm):
    valor = FloatField('Valor do Capital Social', validators=[DataRequired(), NumberRange(min=1)])
    data = StringField('Data de Inserção', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', default='Integralização de Capital Social Inicial')
    submit = SubmitField('Registrar Capital Social')