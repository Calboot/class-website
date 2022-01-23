from flask import Blueprint, render_template, request, redirect, session
import ybc_trans as trans

trans_app = Blueprint('trans_app', __name__)


@trans_app.route('/trans')
def index():
    username = session.get('username')
    if username is None:
        username = "游客"
    return render_template('trans/index.html', t_op='英译汉', t_username=username)


@trans_app.route('/trans/do_trans')
def translate():
    username = session.get('username')
    if username is None:
        username = "游客"
    txt = request.args['txt']
    op = request.args['op']
    if op == '英译汉':
        result = trans.en2zh(txt)
    elif op == '汉译英':
        result = trans.zh2en(txt)
    return render_template('trans/index.html', t_txt=txt, t_result=result, t_op=op, t_username=username)
