from flask import Blueprint, render_template
monkey_app = Blueprint('monkey_app', __name__)
@monkey_app.route('/monkey')
def index():
    return render_template('monkey/index.html')

