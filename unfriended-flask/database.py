from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
import os.path
import time

db = SQLAlchemy()


def init_db(app):
    import unfriended.models
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    while not os.path.exists('/var/run/mysqld/mysqld.sock'):
        time.sleep(5)
    with app.app_context():
        db.create_all()
