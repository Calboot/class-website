from flask import Blueprint, render_template
mario_app = Blueprint('mario_app', __name__)
@mario_app.route('/mario')
def index():
    return render_template('mario/index.html')