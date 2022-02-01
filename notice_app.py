import pymongo
from flask import Blueprint, render_template
notice_app = Blueprint('notice_app', __name__)

client = pymongo.MongoClient("mongodb://localhost:27017")
db_notice = client['db_web']
c_notice = db_notice['notice']


@notice_app.route('/notice')
def notice():
    notice = c_notice.find()
    return render_template('notice/index.html', t_notice=notice)
