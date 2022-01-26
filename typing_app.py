import pymongo
from flask import render_template, request, redirect, session, Blueprint
import user_app
typing_app = Blueprint('typing_app', __name__)


@typing_app.route('/typing')
def index():
    username = session.get("username")
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_game = client['db_user']
    c_game = db_game['game']
    scoreList = c_game.find({"name": "typing"}).sort("score", pymongo.DESCENDING)
    return render_template('typing/index.html', t_scoreList=scoreList, t_username=username)
