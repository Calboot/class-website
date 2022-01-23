from flask import Blueprint, render_template
a2048_app = Blueprint('a2048_app', __name__)
@a2048_app.route('/2048')
def index():
    return render_template('a2048/index.html')