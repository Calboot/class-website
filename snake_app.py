from flask import Blueprint, render_template
snake_app = Blueprint('snake_app', __name__)
@snake_app.route('/snake')
def index():
    return render_template('snake/index.html')

