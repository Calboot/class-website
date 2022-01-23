from flask import render_template, request, redirect, session, Blueprint
typing_app = Blueprint('typing_app', __name__)
@typing_app.route('/typing')
def index():
    return render_template('typing/index.html')