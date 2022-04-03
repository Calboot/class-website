import pymongo
from flask import Blueprint, render_template, session
import user_app

wcg_app = Blueprint('wcg_app', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db_wcg = client['db_web']
c_wcg = db_wcg['wcg']


@wcg_app.before_request
def before_request():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)


@wcg_app.route('/wcg')
def main():
    return render_template('wcg/index.html')


@wcg_app.route('/play')
def play():
    return render_template('wcg/give.html')
