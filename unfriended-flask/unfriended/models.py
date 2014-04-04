from database import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    fbID = db.Column(db.Integer)

    def __init__(self, name=None, fbID=None):
        self.name = name
        self.fbID = fbID