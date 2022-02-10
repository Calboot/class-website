from flask import Flask, render_template, session, request
from user_app import user_app
from album_app import album_app
from todo_app import todo_app
from trans_app import trans_app
# from notice_app import notice_app
# from log_app import log_app
from board_app import board_app
from game_app import game_app
import pymongo

app = Flask(__name__)
app.secret_key = 'anbio3h4i34og'
app.register_blueprint(user_app)
app.register_blueprint(todo_app)
app.register_blueprint(album_app)
app.register_blueprint(trans_app)
app.register_blueprint(game_app)
# app.register_blueprint(notice_app)
# app.register_blueprint(log_app)
app.register_blueprint(board_app)


@app.route('/')
def welcome():
    return render_template('main/welcome.html', t_my_name='早六1班开发组')


@app.route('/main')
def main():
    ip = request.remote_addr
    username = session.get('username')
    if username is not None:
        is_login = True
    else:
        is_login = False
        username = '游客'
    if check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    return render_template('main/main.html', t_username=username, t_is_login=is_login)


def check_login():
    username = session.get('username')
    if username is None:
        return True


def check_user():
    username = session.get('username')
    user_list = find_user({'username': username})
    if len(user_list) == 0:
        return False
    if user_list[0]['state'] == '1':
        return True
    return False


def find_user(condition):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_user = client['db_user']
    c_user = db_user['user']
    res = c_user.find(condition)
    user_list = []
    for item in res:
        user_list.append(item)
    return user_list


@app.errorhandler(404)
def page_not_found(error):
    return render_template('main/404.html'), 404


if __name__ == '__main__':
    app.run()
