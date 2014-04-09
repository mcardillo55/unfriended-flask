from flask import Blueprint, render_template, session
from models import User, Friend
from database import db

from facebook.facebook import facebookOAuth

unfriended = Blueprint('unfriended', '__name__')


def createCurrentFriendsList(currentFriends):
    currentFriendsList = []
    for friend in currentFriends:
        currentFriendsList.append(long(friend['id']))
    return currentFriendsList
        

@unfriended.route('/')
def index():
    if 'oauth_token' in session:
        loggedIn = True
        user = facebookOAuth.get('/me').data
        userId = user['id']
        currentFriends = createCurrentFriendsList(facebookOAuth.get('me/friends').data['data'])
        if User.query.filter_by(fbId=userId).first() is None:
            for friend in currentFriends:
                db.session.add(Friend(userFbId=userId, friendFbId=friend))
            user = User(name=user['name'], fbId=userId)
            db.session.add(user)
            db.session.commit()
            return "First Visit!!!"
        else:
            deletedFriends = []
            oldFriends = Friend.query.filter_by(userFbId=userId).all()
            for friend in oldFriends:
                if friend.friendFbId not in currentFriends:
                    deletedFriends.append(friend.friendFbId)
            return render_template('index.html', loggedIn=loggedIn,
                                   deletedFriends=deletedFriends)
    else:
        loggedIn = False
        user = None
        return render_template('index.html', loggedIn=loggedIn)
