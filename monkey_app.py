import pymongo
from flask import Blueprint, render_template, session
import user_app
monkey_app = Blueprint('monkey_app', __name__)


@monkey_app.route('/monkey')
def index():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get("username")
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_game = client['db_user']
    c_game = db_game['game']
    scoreList = c_game.find({"name": "monkey"}).sort("score", pymongo.DESCENDING)
    return render_template('monkey/index.html', t_scoreList=scoreList, t_username=username)

