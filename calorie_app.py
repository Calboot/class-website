from flask import Blueprint, render_template
calorie_app = Blueprint('calorie_app', __name__)
@calorie_app.route('/calorie')
def index():
    return render_template('calorie/index.html')

