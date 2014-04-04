from flask import Blueprint, render_template, session
from models import User
from database import db

from facebook.facebook import facebookOAuth

unfriended = Blueprint('unfriended', '__name__')

@unfriended.route('/')
def index():
    if 'oauth_token' in session:
        loggedIn = True
        me = facebookOAuth.get('/me').data
        user = User(name=me['name'], fbID=me['id'])
        db.session.add(user)
        db.session.commit()
        newFriends = facebookOAuth.get('me/friends').data['data']
        return render_template('index.html', loggedIn=loggedIn, newFriends = newFriends)
    else:
        loggedIn = False
        me = None
        return render_template('index.html', loggedIn=loggedIn)
