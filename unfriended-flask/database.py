from flask.ext.sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


def init_db(app):
    import unfriended.models
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    with app.app_context():
        db.create_all()