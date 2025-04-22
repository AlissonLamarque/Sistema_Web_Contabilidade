from flask import Flask, render_template, url_for
app = Flask(__name__)

produtos = [
    {
        'nome' : 'Televisão',
        'preco' : 3000.00
    },
    {
        'nome' : 'Geladeira',
        'preco' : 4000.00
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', produtos=produtos)

@app.route("/about")
def about():
    return render_template('about.html', titulo="Teste")

if (__name__) == '__main__':
    app.run(debug=True)