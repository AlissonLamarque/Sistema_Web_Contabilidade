# Sistema de Gestão Comercial

## 📋 Funcionalidades

### 🛒 Cadastro de Produtos
- Preço de compra e venda
- Cálculo automático de ICMS (crédito e débito)
- Controle de estoque
- Status de disponibilidade

### 💰 Operações Comerciais
- Vendas à vista e a prazo
- Registro de compras de fornecedores
- Cálculo automático de custos e lucro

### 👥 Cadastros
- Clientes (nome, CPF, cidade, estado, status)
- Fornecedores (nome, CNPJ, cidade, estado, status)

## 🛠️ Tecnologias Utilizadas

- **Backend**:
  - Python 3.8+
  - Flask
    - Flask-SQLAlchemy
    - Flask-WTF
    - Flask-Migrate
  - MySQL

- **Frontend**:
  - HTML5, CSS3
  - Bootstrap 5
  - JavaScript (Vanilla)

## ⚙️ Configuração do Ambiente

1. Clone o repositório:
```bash
git clone 'https://github.com/AlissonLamarque/Sistema_Web_Contabilidade.git'
cd sistema
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Execute a aplicação:
```bash
flask run
```
