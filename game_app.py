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


def game(name, sort_method=pymongo.DESCENDING, **kwargs):
    username = session.get("username")
    scoreList = c_game.find({"name": name}).sort("score", sort_method)
    return render_template(name + '/index.html', t_scoreList=scoreList, t_username=username, **kwargs)


@game_app.route('/monkey2')
def monkey2():
    return game('monkey2')


@game_app.route('/snake')
def snake():
    return game('snake')


@game_app.route('/monkey')
def monkey():
    return game('monkey')


@game_app.route('/typing')
def typing():
    return game('typing')


@game_app.route('/snake2')
def snake2():
    return game('snake2')


@game_app.route('/ndigit/<int:n>')
def ndigit(n):
    return render_template('ndigit/index.html', num=n)

# @game_app.route('/calorie')
# def calorie():
#     return render_template('calorie/index.html')
