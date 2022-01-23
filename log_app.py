import pymongo
from flask import Blueprint, render_template
log_app = Blueprint('log_app', __name__)


@log_app.route('/log')
def log():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db_log = client['db_log']
    c_log = db_log['log']
    log = c_log.find()
    return render_template('log/index.html', t_log=log)
