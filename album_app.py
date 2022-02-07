import datetime
import os

from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, session, send_file
import uuid
import pymongo
import user_app

album_app = Blueprint('album_app', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db_album = client['db_web']
c_album = db_album['album']


@album_app.route('/album_list')
def album_list():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    album_list = find_all_album()
    total = c_album.count_documents({"public": "1"})
    deleted_total = c_album.count_documents({"deleted": "1", 'owner': session.get("username")})
    return render_template('album/album_list.html', t_album_list=album_list, t_username=username,
                           t_total=total, t_deleted_total=deleted_total)


@album_app.route('/image_list')
def image_list():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    username = session.get('username')
    albumname = request.args['albumname']
    if albumname == "共享的文件":
        imgs_list = c_album.find({"public": "1"})
    elif albumname == "回收站":
        imgs_list = c_album.find({"deleted": "1", 'owner': session.get("username")})
    else:
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
    today = str_now()
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


@album_app.route('/album/set_share')
def share():
    id = request.args.get("id")
    album = c_album.find_one({"_id": ObjectId(id), "owner": session.get("username")})
    if album is not None:
        if (not "public" in album) or album["public"] == "0":
            c_album.update_one({"_id": ObjectId(id)}, {"$set": {'public': '1'}})
        else:
            c_album.update_one({"_id": ObjectId(id)}, {"$set": {'public': '0'}})
        return redirect("/image_list?albumname=" + album["albumname"])
    return redirect("/album_list")


@album_app.route('/album/set_delete')
def delete():
    id = request.args.get("id")
    album = c_album.find_one({"_id": ObjectId(id), "owner": session.get("username")})
    if album is not None:
        if (not "deleted" in album) or album["deleted"] == "0":
            c_album.update_one({"_id": ObjectId(id)}, {"$set": {'deleted': '1', 'public': '0'}})
            return redirect("/image_list?albumname=" + album["albumname"])
        else:
            c_album.update_one({"_id": ObjectId(id)}, {"$set": {'deleted': '0'}})
            return redirect("/image_list?albumname=回收站")
    return redirect("/album_list")


@album_app.route('/album/delete_file')
def delete_file():
    id = request.args.get("id")
    album = c_album.find_one({"_id": ObjectId(id), "owner": session.get("username")})
    if album is not None:
        path = album["path"]
        os.remove(path)
        c_album.delete_one({'_id': ObjectId(id)})
        return redirect("/image_list?albumname=回收站")
    return redirect("/album_list")


@album_app.route('/album/delete_all')
def delete_all():
    album = c_album.find({"owner": session.get("username"), 'deleted': '1'})
    if album is not None:
        for item in album:
            path = item["path"]
            os.remove(path)
            c_album.delete_one({'_id': ObjectId(item["_id"])})
        return redirect("/image_list?albumname=回收站")
    return redirect("/album_list")



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
    condition = {'_id': ObjectId(request.args.get('id'))}
    album = c_album.find_one(condition)
    return send_file(album['path'], as_attachment=True, download_name=album['name'])


@album_app.route('/upload_check', methods=['POST'])
def upload_check():
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    today = str_now()
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
    c_album.insert_one(album)


def find_album(albumname):
    condition = {'$and': [{'albumname': albumname}, {"owner": session.get("username")},
                          {'$or': [{'deleted': {'$exists': False}}, {'deleted': '0'}]}]}
    album = c_album.find(condition)
    return album


def find_all_album():
    res = c_album.aggregate([
        {
            "$match":
                {'$and': [
                    {"owner": session.get("username")},
                    {'$or': [{'deleted': {'$exists': False}}, {'deleted': '0'}]}
                ]}
        },
        {
            "$group":
                {"_id": "$albumname",
                 "num": {"$sum": 1}
                 }
        }
    ])
    # for i in res:
    #     print(i)
    # res = c_album.find()
    # album_list = []
    # for album in res:
    #     album_list.append(album)
    return res


def update_album(albumname, img_path):
    condition = {'albumname': albumname}
    album = c_album.find_one(condition)
    imgs_list = album['imgs']
    imgs_list.append(img_path)
    c_album.update_one({'albumname': albumname}, {"$set": album})


def str_now():
    today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return today
