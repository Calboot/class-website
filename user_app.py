from datetime import datetime
from flask import Blueprint, render_template, request, redirect, session
import pymongo
import hashlib

user_app = Blueprint('user_app', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db_user = client['db_web']
c_user = db_user['user']
c_online = db_user['online']


@user_app.route('/register')
def register():
    return render_template('user/register.html')


@user_app.route('/change_password')
def change_password():
    return render_template('user/change_password.html')


@user_app.route('/register_check', methods=['POST'])
def register_check():
    username = request.form['username']
    password = request.form['password']
    user_list = find_user({'username': username})
    if len(user_list) == 0:
        pwd = encrypt(password)
        user = {'username': username, 'password': pwd, 'state': '2'}
        insert_user(user)
        return redirect('/login')
    else:
        return render_template('user/register.html', t_username=username, t_msg='用户名已经存在')


@user_app.route('/change_submit', methods=['POST'])
def change_submit():
    username = session["username"]
    password = request.form['old_password']
    pwd = encrypt(password)
    user_list = find_user({'username': username, 'password': pwd})
    new_pwd = request.form['new_password']
    new_pwd2 = request.form['new_password2']
    if new_pwd != new_pwd2:
        return render_template('user/change_password.html', t_msg='新密码错误')
    elif len(user_list) == 1:
        c_user.update_one({'username': username}, {"$set": {'password': encrypt(new_pwd)}})
        session.pop('username')
        return render_template('user/login.html', t_error='密码修改成功，请重新登录')
    else:
        return render_template('user/change_password.html', t_msg='原密码错误')


'''
    --------与登录有关的路由--------

    /login           访问登录页面
    /login_check     处理登录表单，实现登录功能

'''


@user_app.route('/update_score', methods=['POST'])
def update_score():
    username = session.get('username')
    name = request.form["name"]
    score = int(request.form["score"])
    db_game = client['db_web']
    c_game = db_game['game']
    glist = c_game.find_one({"username": username, "name": name})
    ulist = c_user.find_one({"username": username})
    if glist is None or len(glist) == 0:
        if ulist['state'] != '3':
            c_game.insert_one({"username": username, "name": name, "score": score})
    else:
        if score > int(glist["score"]) and ulist['state'] != '3':
            c_game.update_one({"username": username, "name": name}, {"$set": {"score": score}})
    return {'state': 'ok'}


@user_app.route('/login')
def login():
    return render_template('user/login.html')


@user_app.route('/login_check', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    pwd = encrypt(password)
    user_list = find_user({'username': username, 'password': pwd})
    if len(user_list) == 1:
        if user_list[0]['state'] == "2":
            return render_template('user/login.html', t_error='用户信息待审核', t_color='2')
        elif user_list[0]['state'] != "1":
            session['username'] = username
            return redirect('/main')
        else:
            return render_template('user/login.html', t_error='此账号已被封禁', t_color='1')
    else:
        return render_template('user/login.html', t_error='用户名或密码错误')


@user_app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/main')


'''
    --------与登录、注册有关的自定义函数--------

    insert_user()     将注册用户数据存入数据库
    find_user()       根据条件查找注册用户信息
    encrypt()         对密码进行加密
'''


def insert_user(user):
    c_user.insert_one(user)


def find_user(condition):
    res = c_user.find(condition)
    user_list = []
    for item in res:
        user_list.append(item)
    return user_list


def encrypt(password):
    pwd = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    return pwd


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
    print(1)
    ts = datetime.timestamp(datetime.now())
    if c_online.count_documents({'username': username}) != 0:
        c_online.update_one({'username': username}, {"$set": {'time': ts}})
    else:
        c_online.insert_one({'username': username, 'time': ts})
    return False
