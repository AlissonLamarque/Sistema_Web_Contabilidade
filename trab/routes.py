from flask import render_template, url_for, redirect, flash, request
from forms import ProdutoForm, ClienteForm, FornecedorForm, CompraForm, VendaForm
from models import db, Produto, Cliente, Fornecedor, Compra, Item_compra, Venda, Item_venda

def init_app(app):
    # PRODUTOS

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/produtos")
    def produtos():
        produtos = Produto.query.all()
        return render_template('produto/produtos.html', produtos=produtos)

    @app.route('/cadastrar_produto', methods=['GET', 'POST'])
    def cadastrar_produto():
        form = ProdutoForm()
        if form.validate_on_submit():
            produto = Produto(
                nome = form.nome.data,
                preco_compra = form.preco_compra.data,
                preco_venda = form.preco_venda.data,
                status = form.status.data
            )
            db.session.add(produto)
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('produtos'))
        return render_template('produto/cadastrar_produto.html', form=form)

    @app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
    def editar_produto(produto_id):
        produto = Produto.query.get_or_404(produto_id)
        form = ProdutoForm(obj=produto)
        if form.validate_on_submit():
            produto.nome = form.nome.data
            produto.preco_compra = form.preco_compra.data
            produto.preco_venda = form.preco_venda.data
            produto.status = form.status.data
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos'))
        return render_template('produto/cadastrar_produto.html', form=form, titulo='Editar Produto')

    # CLIENTES

    @app.route('/clientes')
    def clientes():
        clientes = Cliente.query.all()
        return render_template('cliente/clientes.html', clientes=clientes)

    @app.route('/cadastrar_cliente', methods=['GET', 'POST'])
    def cadastrar_cliente():
        form = ClienteForm()
        if form.validate_on_submit():
            cliente = Cliente(
                nome = form.nome.data,
                cpf = form.cpf.data,
                cidade = form.cidade.data,
                estado = form.estado.data,
                status = form.status.data
            )
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('clientes'))
        return render_template('cliente/cadastrar_cliente.html', form=form)

    @app.route('/editar_cliente/<int:cliente_id>', methods=['GET', 'POST'])
    def editar_cliente(cliente_id):
        cliente = Cliente.query.get_or_404(cliente_id)
        form = ClienteForm(obj=cliente)
        if form.validate_on_submit():
            cliente.nome = form.nome.data
            cliente.cpf = form.cpf.data
            cliente.cidade = form.cidade.data
            cliente.estado = form.estado.data
            cliente.status = form.status.data
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('clientes'))
        return render_template('cliente/cadastrar_cliente.html', form=form, titulo='Editar Cliente')

    # FORNECEDORES

    @app.route('/fornecedores')
    def fornecedores():
        fornecedores = Fornecedor.query.all()
        return render_template('fornecedor/fornecedores.html', fornecedores=fornecedores)

    @app.route('/cadastrar_fornecedor', methods=['GET', 'POST'])
    def cadastrar_fornecedor():
        form = FornecedorForm()
        if form.validate_on_submit():
            fornecedor = Fornecedor(
                nome = form.nome.data,
                cnpj = form.cnpj.data,
                cidade = form.cidade.data,
                estado = form.estado.data,
                status = form.status.data
            )
            db.session.add(fornecedor)
            db.session.commit()
            flash('Fornecedor cadastrado com sucesso!', 'success')
            return redirect(url_for('fornecedores'))
        return render_template('fornecedor/cadastrar_fornecedor.html', form=form)

    @app.route('/editar_fornecedor/<int:fornecedor_id>', methods=['GET', 'POST'])
    def editar_fornecedor(fornecedor_id):
        fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
        form = FornecedorForm(obj=fornecedor)
        if form.validate_on_submit():
            fornecedor.nome = form.nome.data
            fornecedor.cnpj = form.cnpj.data
            fornecedor.cidade = form.cidade.data
            fornecedor.estado = form.estado.data
            fornecedor.status = form.status.data
            db.session.commit()
            flash('Fornecedor atualizado com sucesso!', 'success')
            return redirect(url_for('fornecedores'))
        return render_template('fornecedor/cadastrar_fornecedor.html', form=form, titulo='Editar Fornecedor')

    # COMPRAS

    @app.route('/compras')
    def compras():
        compras = Compra.query.order_by(Compra.data_compra.desc()).all()
        return render_template('compra/compras.html', compras=compras)

    @app.route('/cadastrar_compra', methods=['GET', 'POST'])
    def cadastrar_compra():
        form = CompraForm()
        fornecedores = Fornecedor.query.all()
        produtos = Produto.query.all()
        
        form.fornecedor_id.choices = [(f.id, f.nome) for f in fornecedores]
        
        if form.validate_on_submit():
            try:
                nova_compra = Compra(
                    fornecedor_id = form.fornecedor_id.data,
                    nf_entrada = form.nf_entrada.data,
                    data_compra = form.data_compra.data,
                    status = form.status.data,
                    valor_total = 0 
                )
                db.session.add(nova_compra)
                db.session.flush()
                
                valor_total = 0
                produtos_ids = request.form.getlist('produto_id')
                quantidades = request.form.getlist('quantidade')
                precos_unitarios = request.form.getlist('preco_unitario')
                
                for produto_id, quantidade, preco_unitario in zip(produtos_ids, quantidades, precos_unitarios):
                    if not produto_id or not quantidade or not preco_unitario:
                        continue
                        
                    item = Item_compra(
                        compra_id = nova_compra.id,
                        produto_id = produto_id,
                        quantidade = float(quantidade),
                        preco_unitario = float(preco_unitario)
                    )
                    db.session.add(item)
                    
                    valor_total += float(quantidade) * float(preco_unitario)
                
                nova_compra.valor_total = valor_total
                db.session.commit()
                
                flash('Compra registrada com sucesso!', 'success')
                return redirect(url_for('compras'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar compra: {str(e)}', 'danger')
        
        return render_template('compra/cadastrar_compra.html', form=form, fornecedores=fornecedores, produtos=produtos)

    # VENDAS

    @app.route('/vendas')
    def vendas():
        vendas = Venda.query.options(db.joinedload(Venda.cliente)).all()
        return render_template('venda/vendas.html', vendas=vendas)

    @app.route('/cadastrar_venda', methods=['GET', 'POST'])
    def cadastrar_venda():
        form = VendaForm()
        clientes = Cliente.query.all()
        produtos = Produto.query.all()
        
        form.cliente_id.choices = [(c.id, c.nome) for c in clientes]
        
        if form.validate_on_submit():
            try:
                nova_venda = Venda(
                    cliente_id = form.cliente_id.data,
                    forma_pagamento = form.forma_pagamento.data,
                    data_venda = form.data_venda.data,
                    status = form.status.data,
                    valor_total = 0
                )
                db.session.add(nova_venda)
                db.session.flush()
                
                valor_total = 0
                produtos_ids = request.form.getlist('produto_id')
                quantidades = request.form.getlist('quantidade')
                precos_unitarios = request.form.getlist('preco_unitario')
                
                for produto_id, quantidade, preco_unitario in zip(produtos_ids, quantidades, precos_unitarios):
                    if not produto_id or not quantidade or not preco_unitario:
                        continue
                        
                    quantidade = float(quantidade)
                    preco_unitario = float(preco_unitario)
                    
                    item = Item_venda(
                        venda_id=nova_venda.id,
                        produto_id=produto_id,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario
                    )
                    db.session.add(item)
                    
                    valor_total += quantidade * preco_unitario
                
                nova_venda.valor_total = valor_total
                db.session.commit()
                
                flash('Venda registrada com sucesso!', 'success')
                return redirect(url_for('vendas'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao registrar venda: {str(e)}', 'danger')
        
        return render_template('venda/cadastrar_venda.html', form=form, clientes=clientes, produtos=produtos)