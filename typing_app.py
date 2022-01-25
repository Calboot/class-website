from flask import render_template, request, redirect, session, Blueprint
import user_app
typing_app = Blueprint('typing_app', __name__)


@typing_app.route('/typing')
def index():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    return render_template('typing/index.html')