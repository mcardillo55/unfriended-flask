from flask import Blueprint, redirect, url_for, session, request
from flask_oauthlib.client import OAuth

from config import FB_KEY, FB_SECRET

facebook = Blueprint('facebook', __name__)

oauth = OAuth()

facebookOAuth = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FB_KEY,
    consumer_secret=FB_SECRET,
    request_token_params={'scope': 'email'}
    )

@facebook.route('/login')
def login():
    return facebookOAuth.authorize(callback=url_for('.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@facebook.route('/login/authorized')
@facebookOAuth.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    return redirect(url_for('home.index'))

@facebookOAuth.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')