import pymongo
from flask import Blueprint, render_template
notice_app = Blueprint('notice_app', __name__)


@notice_app.route('/notice')
def notice():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_notice = client['db_notice']
    c_notice = db_notice['notice']
    notice = c_notice.find()
    return render_template('notice/index.html', t_notice=notice)
