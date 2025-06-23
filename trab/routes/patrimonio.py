from flask import render_template, url_for, redirect, flash, Blueprint
from forms import PatrimonioForm, CompraPatrimonioForm
from models import db, Patrimonio, CompraPatrimonio, Fornecedor

patrimonio_bp = Blueprint('patrimonio_bp', __name__, template_folder='templates', static_folder='static')

@patrimonio_bp.route('/bens')
def bens():
    bens_ativos = Patrimonio.query.filter_by(status='ativo').order_by(Patrimonio.nome).all()
    bens_manutencao = Patrimonio.query.filter_by(status='manutencao').order_by(Patrimonio.nome).all()
    bens_vendidos = Patrimonio.query.filter_by(status='vendido').order_by(Patrimonio.nome).all()
    return render_template('patrimonio/bens.html',  
                           bens_ativos=bens_ativos, 
                           bens_manutencao=bens_manutencao, 
                           bens_vendidos=bens_vendidos)