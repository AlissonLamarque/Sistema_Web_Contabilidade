from flask import render_template, url_for, redirect, flash, request, Blueprint
from forms import CompraForm
from models import db, Produto, Fornecedor, Compra, Item_compra

compras_bp = Blueprint('compras_bp', __name__, template_folder='templates', static_folder='static')

@compras_bp.route('/compras')
def compras():
    compras = Compra.query.options(
        db.joinedload(Compra.fornecedor),
        db.joinedload(Compra.itens).joinedload(Item_compra.produto)
    ).order_by(Compra.data_compra.desc()).all()
    return render_template('compra/compras.html', compras=compras)

@compras_bp.route('/cadastrar_compra', methods=['GET', 'POST'])
def cadastrar_compra():
    form = CompraForm()
    fornecedores = Fornecedor.query.filter_by(status='ativo').all()
    form.fornecedor_id.choices = [(f.id, f"{f.nome} - {f.cnpj}") for f in fornecedores]
    produtos = Produto.query.all()
    
    if request.method == 'POST':
        try:
            if not all([form.fornecedor_id.data, form.nf_entrada.data, form.data_compra.data]):
                flash('Preencha todos os campos obrigatórios', 'danger')
                return redirect(url_for('compras_bp.cadastrar_compra'))

            nova_compra = Compra(
                fornecedor_id=form.fornecedor_id.data,
                nf_entrada=form.nf_entrada.data,
                data_compra=form.data_compra.data,
                status=form.status.data,
                valor_total=0
            )
            db.session.add(nova_compra)
            db.session.flush()

            produtos_ids = request.form.getlist('produto_id')
            quantidades = request.form.getlist('quantidade')
            precos_unitarios = request.form.getlist('preco_unitario')

            if not produtos_ids:
                flash('Adicione pelo menos um item', 'danger')
                db.session.rollback()
                return redirect(url_for('compras_bp.cadastrar_compra'))

            for i in range(len(produtos_ids)):
                produto = Produto.query.get(produtos_ids[i])
                if not produto:
                    continue

                item = Item_compra(
                    compra_id=nova_compra.id,
                    produto_id=produtos_ids[i],
                    quantidade=int(quantidades[i]),
                    preco_unitario=float(precos_unitarios[i])
                )
                db.session.add(item)
                
                produto.estoque += int(quantidades[i])
                produto.status = 'disponível' if produto.estoque > 0 else 'indisponível'
                
                nova_compra.valor_total += item.quantidade * item.preco_unitario

            db.session.commit()
            flash('Compra registrada com sucesso!', 'success')
            return redirect(url_for('compras_bp.compras'))

        except ValueError as e:
            db.session.rollback()
            flash(f'Erro nos valores informados: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar compra: {str(e)}', 'danger')
            compras_bp.logger.error(f"Erro em cadastrar_compra: {str(e)}", exc_info=True)

    return render_template('compra/cadastrar_compra.html', form=form, fornecedores=fornecedores, produtos=produtos)

@compras_bp.route('/cancelar_compra/<int:compra_id>', methods=['POST'])
def cancelar_compra(compra_id):
    compra = Compra.query.get_or_404(compra_id)
    
    try:
        for item in compra.itens:
            produto = Produto.query.get(item.produto_id)
            produto.estoque -= item.quantidade
            if produto.estoque > 0:
                produto.status = 'disponível'
        
        compra.status = 'cancelada'
        db.session.commit()
        flash('Compra cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar compra: {str(e)}', 'danger')
    
    return redirect(url_for('compras_bp.compras'))
