from flask import render_template, Blueprint

base_bp = Blueprint('base_bp', __name__, template_folder='templates', static_folder='static')

@base_bp.route("/")
def index():
    return render_template('index.html')