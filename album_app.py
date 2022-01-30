import datetime
from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, session, send_file
import uuid
import pymongo
import user_app

album_app = Blueprint('album_app', __name__)


@album_app.route('/album_list')
def album_list():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    album_list = find_all_album()
    return render_template('album/album_list.html', t_album_list=album_list, t_username=username)


@album_app.route('/image_list')
def image_list():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    albumname = request.args['albumname']
    imgs_list = find_album(albumname)
    return render_template('album/image_list.html', t_albumname=albumname, t_imgs_list=imgs_list, t_username=username)


@album_app.route('/create')
def create():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    return render_template('album/create_album.html', t_username=username)


@album_app.route('/create_check', methods=['POST'])
def create_check():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = str(datetime.date.today())
    img = request.files['img']
    filename = img.filename
    ext = filename.split('.')[-1]
    img_path = 'static/album/upload/' + str(uuid.uuid1()) + '.' + ext
    img.save(img_path)
    albumname = request.form['albumname']
    username = session.get('username')
    new_album = {'albumname': albumname, 'name': filename, 'path': img_path, 'owner': username, 'time': today}
    insert_album(new_album)
    return redirect('/album_list')


@album_app.route('/upload')
def upload():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    album_list = find_all_album()
    return render_template('album/upload.html', t_album_list=album_list, t_username=username)


@album_app.route('/download')
def download():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    condition = {'_id': ObjectId(request.args.get('id'))}
    album = c_album.find_one(condition)
    return send_file(album['path'], as_attachment=True, download_name=album['name'])


@album_app.route('/upload_check', methods=['POST'])
def upload_check():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = str(datetime.date.today())
    img = request.files['img']
    filename = img.filename
    ext = filename.split('.')[-1]
    img_path = 'static/album/upload/' + str(uuid.uuid1()) + '.' + ext
    img.save(img_path)
    albumname = request.form['albumname']
    username = session.get('username')
    new_album = {'albumname': albumname, 'name': filename, 'path': img_path, 'owner': username, 'time': today}
    insert_album(new_album)
    return redirect('/album_list')


'''
    --------自定义函数--------

    insert_album()       将“某个相册的数据”存储到数据库中
    find_album()         从数据库中“根据相册名”获取该相册的数据
    find_all_album()     从数据库中获取所有相册的数据
    update_album()       更新数据库中某个相册的数据

'''


def insert_album(album):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    c_album.insert_one(album)


def find_album(albumname):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    condition = {'albumname': albumname}
    album = c_album.find(condition)
    return album


def find_all_album():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    res = c_album.aggregate(
        [{
            "$group":
                {"_id": "$albumname",
                 "num": {"$sum": 1}
                 }}
        ])
    # for i in res:
    #     print(i)
    # res = c_album.find()
    # album_list = []
    # for album in res:
    #     album_list.append(album)
    return res


def update_album(albumname, img_path):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_album = client['db_album']
    c_album = db_album['album']
    condition = {'albumname': albumname}
    album = c_album.find_one(condition)
    imgs_list = album['imgs']
    imgs_list.append(img_path)
    c_album.update_one({'albumname': albumname},  {"$set": album})
