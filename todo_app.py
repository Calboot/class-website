from flask import Blueprint, render_template, request, session, redirect
import pymongo
import datetime
import uuid
import user_app

todo_app = Blueprint('todo_app', __name__)


@todo_app.route('/todo')
def list_page():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = datetime.date.today()
    one_day = datetime.timedelta(days=7)
    yesterday = str(today - one_day)
    condition = {
        '$or': [
            {'public': '0', 'owner': username},
            {'public': '1', 'date': {'$gt': "2021-01-20"}}
            # {'public': '2', 'to': {'$in': [username]}}
        ]
    }
    date = request.args.get('date')
    subject = request.args.get('subject')
    if date is None:
        date = '全部'
    elif date == '今天':
        condition['date'] = str_today()
    elif date == '昨天':
        condition['date'] = str_yesterday()
    if subject is None:
        subject = '全部'
    elif subject != '全部':
        condition['subject'] = subject
    todo_list = find_todo(condition)
    date_options = ['全部', '今天', '昨天']
    subject_options = ['全部', '综合', '公告', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治', '编程']
    return render_template('todo/list.html', t_username=username, t_todo_list=todo_list, t_date_options=date_options,
                           t_subject_options=subject_options, t_date=date, t_subject=subject)


@todo_app.route('/todo_list')
def todo_list():
    _id = request.args['id']
    condition = {
        '$or': [
            {'_id': _id},
            {'parent': _id}
        ]
    }
    todo_list = find_todo(condition)
    print(todo_list)
    return render_template('todo/todo_list.html', t_todo_list=todo_list, t_id=_id)


@todo_app.route('/todo/add')
def todo_add():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = str_today()
    subjects = ['综合', '公告','语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治', '编程']
    return render_template('todo/todo_add.html', t_subject_options=subjects, t_date=today, t_username=username)


@todo_app.route('/add_check', methods=['POST'])
def add_check():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    todo = {'subject': request.form.get('subject'), 'content': request.form.get('content'), 'date': str_today(),
            '_id': str(uuid.uuid1()), 'state': 'unfinished', 'owner': username, 'public': request.form.get('public')}
    insert_todo(todo)
    return redirect('/todo')


@todo_app.route('/todo/finished')
def todo_finish():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    id_str = request.args.get('_id')
    if id_str is not None:
        finish_todo(id_str)
    return redirect('/todo')


@todo_app.route('/todo/unfinished')
def todo_unfinish():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    id_str = request.args.get('_id')
    if id_str is not None:
        unfinish_todo(id_str)
    return redirect('/todo')


@todo_app.route('/todo/deleted')
def todo_delete():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    id_str = request.args.get('_id')
    if id_str is not None:
        delete_todo(id_str)
    return redirect('/todo')


'''
    --------与任务本有关的自定义函数--------

    insert_todo()      存储新的任务
    find_todo()        根据条件查询任务
    finish_todo()      将任务状态改为“已完成”
    unfinish_todo()    将任务状态改为“未完成”
    delete_todo()      将任务状态改为“已删除”，即删除任务
    str_today()        获取今天的日期(字符串)
    str_yesterday()    获取昨天的日期(字符串)

'''


def insert_todo(todo):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    c_todo.insert_one(todo)


def find_todo(condition):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    res = c_todo.find(condition)
    todo_list = []
    for item in res:
        todo_list.append(item)
    return todo_list


def finish_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'finished'
    c_todo.update_one({'_id': todo_id}, {"$set": {'state': 'finished'}})


def unfinish_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'unfinished'
    c_todo.update_one({'_id': todo_id}, {"$set": {'state': 'unfinished'}})


def delete_todo(todo_id):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_todo = client['db_todo']
    c_todo = db_todo['todo']
    todo = c_todo.find_one({'_id': todo_id})
    todo['state'] = 'deleted'
    c_todo.update_one({'_id': todo_id}, {"$set": {'state': 'deleted'}})


def str_today():
    today = datetime.date.today()
    return str(today)


def str_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return str(yesterday)
