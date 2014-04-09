from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    fbId = db.Column(db.BigInteger)

    def __init__(self, name=None, fbId=None):
        self.name = name
        self.fbId = fbId


class Friend(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    userFbId = db.Column(db.BigInteger)
    friendFbId = db.Column(db.BigInteger)

    def __init__(self, userFbId=None, friendFbId=None):
        self.userFbId = userFbId
        self.friendFbId = friendFbId
