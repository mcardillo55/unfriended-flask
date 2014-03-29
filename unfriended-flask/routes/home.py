from flask import Blueprint, render_template, session

from facebook.facebook import facebookOAuth

home = Blueprint('home', '__name__')

@home.route('/')
def index():
    if 'oauth_token' in session:
        loggedIn = True
        me = facebookOAuth.get('/me').data
    else:
        loggedIn = False
        me = None
    return render_template('index.html', loggedIn=loggedIn, me=me)
