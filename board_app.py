from flask import Blueprint, render_template, request, session, redirect
from flask_paginate import Pagination, get_page_parameter
import pymongo
import datetime
import uuid
import user_app
import markdown

board_app = Blueprint('board_app', __name__)
per_page = 10
client = pymongo.MongoClient("mongodb://localhost:27017")
db_board = client['db_web']
c_board = db_board['board']


@board_app.before_request
def before_request():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)


@board_app.route('/board')
def list_page():
    username = session.get('username')
    condition = {'public': '1'}
    date = request.args.get('date')
    kw = request.args.get('kw')
    subject = request.args.get('subject')
    # if date is None:
    #     date = '全部'
    # elif date == '今天':
    #     condition['date'] = str_today()
    # elif date == '昨天':
    #     condition['date'] = str_yesterday()
    if subject is None:
        subject = '全部'
    elif subject != '全部':
        condition['subject'] = subject
    # {'$or': [{"title" : {$regex : "测试"}}, {"content" : {$regex : "测试"}}]}
    # db.getCollection('todo').createIndex({"title": "text", "content": "text"})
    # { $text: { $search: "\"coffee shop\""}}

    page = request.args.get(get_page_parameter(), type=int, default=1)
    alist = find_board(condition, page, kw)
    pagination = Pagination(page=page, per_page=per_page, total=c_board.count_documents(condition), search=False,
                            record_name='alist')
    date_options = ['全部', '今天', '昨天']
    subject_options = ['全部', '综合', '公告', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治', '编程']
    return render_template('board/list.html', t_username=username, t_board_list=alist, t_date_options=date_options,
                           t_subject_options=subject_options, t_date=date, t_subject=subject, pagination=pagination,
                           t_kw=kw or '')


@board_app.route('/board_list')
def board_list():
    username = session.get("username")
    _id = request.args['id']
    title = c_board.find_one({'_id': _id})['title']
    content = c_board.find_one({'_id': _id})['content']
    condition = {'parent': _id}
    alist = find_board(condition)
    for item in alist:
        item['html'] = markdown.markdown(
            item['content'], extensions=["fenced_code", "tables", "codehilite"]
        )
    alist.reverse()
    return render_template('board/board_list.html', t_board_list=alist, t_id=_id, t_title=title, t_content=content,
                           t_username=username)


@board_app.route('/reply_check', methods=['POST'])
def reply_check():
    username = session.get("username")
    parent = request.form.get("id")
    content = request.form.get("content")
    today = str_now()
    c_board.insert_one({'content': content, 'date': today, 'public': '1', 'parent': parent, 'owner': username})
    return redirect('/board_list?id=' + parent)


@board_app.route('/board/add')
def board_add():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = str_today()
    subjects = ['综合', '公告', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '地理', '政治', '编程']
    return render_template('board/board_add.html', t_subject_options=subjects, t_date=today, t_username=username)


@board_app.route('/board/add_check', methods=['POST'])
def add_check():
    username = session.get('username')
    id = str(uuid.uuid1())
    board = {'subject': request.form.get('subject'), 'content': request.form.get('content'), 'date': str_now(),
             '_id': str(id), 'owner': username, 'public': "1", 'title': request.form.get("title"),
             'parent': str(id)}
    insert_board(board)
    return redirect('/board')


'''
    --------与任务本有关的自定义函数--------

    insert_board()      存储新的任务
    find_board()        根据条件查询任务
    finish_board()      将任务状态改为“已完成”
    unfinish_board()    将任务状态改为“未完成”
    delete_board()      将任务状态改为“已删除”，即删除任务

'''


def insert_board(board):
    c_board.insert_one(board)


def find_board(condition, page=0, kw=''):
    parent_cond = {}
    if kw is not None and kw != '':
        parent_cond['$or'] = [{"title": {'$regex': kw}}, {"content": {'$regex': kw}}]
        res = c_board.find(parent_cond)
        plist = []
        for item in res:
            plist.append(item['parent'])
        plist = list(set(plist))
        condition['parent'] = {'$in': plist}
    cond = {'$and': [condition]}
    if page == 0:
        res = c_board.find(cond).sort("date", pymongo.DESCENDING)
    else:
        res = c_board.find(cond).sort([{"sticky", pymongo.DESCENDING}, {"date", pymongo.DESCENDING}])\
            .skip((page-1) * per_page).limit(per_page)
    alist = []
    for item in res:
        alist.append(item)
    return alist


def finish_board(board_id):
    board = c_board.find_one({'_id': board_id})
    board['state'] = 'finished'
    c_board.update_one({'_id': board_id}, {"$set": {'state': 'finished'}})


def unfinish_board(board_id):
    board = c_board.find_one({'_id': board_id})
    board['state'] = 'unfinished'
    c_board.update_one({'_id': board_id}, {"$set": {'state': 'unfinished'}})


def delete_board(board_id):
    board = c_board.find_one({'_id': board_id})
    board['state'] = 'deleted'
    c_board.update_one({'_id': board_id}, {"$set": {'state': 'deleted'}})


def str_now():
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return today


def str_today():
    today = datetime.date.today()
    return str(today)
