from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth
from config import FB_KEY, FB_SECRET, APP_SECRET

from routes.home import home

BLUEPRINT_MODULES = [home]

app = Flask(__name__)
app.secret_key = APP_SECRET

for module in BLUEPRINT_MODULES:
    app.register_blueprint(module)

oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FB_KEY,
    consumer_secret=FB_SECRET,
    request_token_params={'scope': 'email'}
    )

@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
        (me.data['id'], me.data['name'], request.args.get('next'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

if __name__ == '__main__':
    app.run(debug=True)