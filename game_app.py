from flask import Blueprint, render_template, request, session, redirect
import pymongo
import datetime
import uuid
import user_app

game_app = Blueprint('game_app', __name__)


@game_app.route('update_score')
def update_score():
    username = session.get('username')
    if user_app.check_login():
        return render_template('user/login.html', t_error='请登录')
    if user_app.check_user():
        return render_template('user/login.html', t_error='此账号已被封禁', t_color=1)
    return
