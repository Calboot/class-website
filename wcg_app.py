import pymongo
from flask import Blueprint, render_template, session, Flask
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
def wcgmain():
    return render_template('wcg/index.html')


@wcg_app.route('/wcggame')
def wcggame():
    username = session.get('username')
    return render_template('wcg/game.html', t_username=username)


@wcg_app.route('/wcginform')
def wcginform():
    return render_template('wcg/inform.html')


@wcg_app.route('/wcgpreload')
def wcgpreload():
    return render_template('wcg/preload.html')


@wcg_app.route('/wcgteach')
def wcgteach():
    return render_template('wcg/teach.html')
