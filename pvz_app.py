from flask import Blueprint, render_template
pvz_app = Blueprint('pvz_app', __name__)
@pvz_app.route('/pvz')
def index():
    return render_template('pvz/index.htm')