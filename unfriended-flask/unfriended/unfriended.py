from flask import Blueprint, render_template, session
from models import User, Friend
from database import db

from facebook.facebook import facebookOAuth

unfriended = Blueprint('unfriended', '__name__')


def compareFriends(first, second):
    '''Takes two lists of longs, returns friends in first but not
    in second'''
    return list(set(first) - set(second))


def storeNewUser(name, fbId):
    user = User(name=name, fbId=fbId)
    db.session.add(user)
    db.session.commit()


def storeFriends(userFbId, newFriends):
    for friend in newFriends:
        db.session.add(Friend(userFbId=userFbId, friendFbId=friend))
    db.session.commit()


def getStoredFriends(fbId):
    ''' Takes long facebook ID. Returns friends as list of longs'''
    friendQuery = Friend.query.filter_by(userFbId=fbId)
    if friendQuery.first() is None:
        return None
    else:
        storedFriends = []
        for friend in friendQuery.all():
            storedFriends.append(friend.friendFbId)
        return storedFriends


def getCurrentFriends(currentFriendsAPI):
    ''' Takes result JSON data from FB API call. Returns list of longs '''
    currentFriends = []
    for friend in currentFriendsAPI:
        currentFriends.append(long(friend['id']))
    return currentFriends


@unfriended.route('/')
def index():
    if 'oauth_token' in session:
        loggedIn = True
        user = facebookOAuth.get('/me').data
        userId = user['id']
        currentFriends = getCurrentFriends(facebookOAuth.get('me/friends')
                                           .data['data'])
        if User.query.filter_by(fbId=userId).first() is None:
            # First time visiting site
            storeNewUser(name=user['name'], fbId=userId)
            deletedFriends = []
            newFriends = currentFriends
        else:
            storedFriends = getStoredFriends(userId)
            deletedFriends = compareFriends(storedFriends, currentFriends)
            newFriends = compareFriends(currentFriends, storedFriends)
        storeFriends(userId, newFriends)
        return render_template('index.html', loggedIn=loggedIn,
                               deletedFriends=deletedFriends)
    else:
        loggedIn = False
        user = None
        return render_template('index.html', loggedIn=loggedIn)
