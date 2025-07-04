from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, NumberRange

# Forms Básicos

## Define o formulário para cadastro de produtos
class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    preco_compra = FloatField('Preço de Compra', validators=[DataRequired()])
    preco_venda = FloatField('Preço de Venda', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Produto')

## Define o formulário para edição de produtos
class EditarProdutoForm(ProdutoForm):
    status = SelectField('Status', 
                       choices=[('disponível', 'Disponível'), ('indisponível', 'Indisponível')],
                       validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

## Define o formulário para cadastro de clientes
class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    submit = SubmitField('Cadastrar Produto')

## Define o formulário para edição de clientes
class EditarClienteForm(ClienteForm):
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

## Define o formulário para cadastro de fornecedores
class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    cidade = StringField('Cidade')
    estado = StringField('Estado')
    submit = SubmitField('Cadastrar Produto')

## Define o formulário para edição de fornecedores
class EditarFornecedorForm(FornecedorForm):
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')],
                       validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

# Forms de Compras e Vendas

## Define o formulário para cadastro de compras
class CompraForm(FlaskForm):
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()], choices=[])
    forma_pagamento = SelectField('Forma de Pagamento',
                                choices=[('vista', 'À Vista'), ('prazo', 'A Prazo')],
                                validators=[DataRequired()])
    data_compra = DateField('Data da Compra', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Compra')

## Define o formulário para cadastro de vendas
class VendaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()], choices=[])
    forma_pagamento = SelectField('Forma de Pagamento',
                                choices=[('avista', 'À Vista'), ('prazo', 'A Prazo')],
                                validators=[DataRequired()])
    data_venda = DateField('Data da Venda', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Venda')

# Forms de Patrimônio e Movimentação Financeira

## Define o formulário para cadastro de bem patrimonial
class PatrimonioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    valor = FloatField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    data_aquisicao = DateField('Data de Aquisição', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Status', choices=[('ativo', 'Ativo'), ('manutencao', 'Em Manutenção'), ('vendido', 'Vendido')])
    submit = SubmitField('Cadastrar Bem')

## Define o formulário para edição de bem patrimonial
class EditarPatrimonioForm(PatrimonioForm):
    status = SelectField('Status', 
                       choices=[('ativo', 'Ativo'), ('manutencao', 'Em Manutenção'), ('vendido', 'Vendido')],
                       validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

## Define o formulário para compra de bem patrimonial
class CompraPatrimonioForm(FlaskForm):
    patrimonio_id = SelectField('Bem Patrimonial', coerce=int, validators=[DataRequired()], choices=[])
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()], choices=[])
    data_compra = DateField('Data da Compra', format='%Y-%m-%d', validators=[DataRequired()])
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
    data = DateField('Data de Inserção', format='%Y-%m-%d', validators=[DataRequired()])
    descricao = TextAreaField('Descrição', default='Integralização de Capital Social Inicial')
    submit = SubmitField('Registrar Capital Social')