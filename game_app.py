import pymongo
from flask import Blueprint, render_template, session
import user_app

game_app = Blueprint('game_app', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db_game = client['db_web']
c_game = db_game['game']


@game_app.before_request
def before_request():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)


@game_app.route('/snake')
def snake():
    username = session.get("username")
    scoreList = c_game.find({"name": "snake"}).sort("score", pymongo.DESCENDING)
    return render_template('snake/index.html', t_scoreList=scoreList, t_username=username)


@game_app.route('/monkey')
def monkey():
    username = session.get("username")
    scoreList = c_game.find({"name": "monkey"}).sort("score", pymongo.DESCENDING)
    return render_template('monkey/index.html', t_scoreList=scoreList, t_username=username)


@game_app.route('/typing')
def typing():
    username = session.get("username")
    scoreList = c_game.find({"name": "typing"}).sort("score", pymongo.DESCENDING)
    return render_template('typing/index.html', t_scoreList=scoreList, t_username=username)


@game_app.route('/calorie')
def calorie():
    return render_template('calorie/index.html')

