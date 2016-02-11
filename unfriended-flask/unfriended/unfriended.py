from flask import Blueprint, render_template, session, g, request
from models import User, Friend
from database import db
from BeautifulSoup import BeautifulSoup
import urllib
import json
import time

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


def getCurrentFriends():
    ''' Takes result JSON data from FB API call. Returns list of longs 
        This function is no longer used, but keeping around in case FB
        changes there API permissions in the future'''
    facebookOAuth.get('me/friends').data['data']
    currentFriends = []
    for friend in currentFriendsAPI:
        currentFriends.append(long(friend['id']))
    return currentFriends


def getFriendData(friendList):
    ''' Requests FB for name and picture from deleted friends. Does not add to
    list in the case of an error (most likely a deactivated account) '''
    deletedFriendsClean = []
    batch = []
    for friend in friendList:
        batch.append({'method': 'GET',
                      'relative_url': "%lu?fields=name,picture" % friend})
        #maximum FB batch size is 50
        if len(batch) == 50:
            deletedFriendsClean = deletedFriendsClean + sendBatch(batch)
            batch = []
    deletedFriendsClean = deletedFriendsClean + sendBatch(batch)
    return deletedFriendsClean


def parseFBHTML(htmlFile):
    ''' Takes an input file of the full HTML from a users Facebook friend page
        and searches for their friends FB user IDs in it. Returns a long list of
        the friends FB user IDs. This will probably have to be updated frequently
        as FB updates their code '''
    soup = BeautifulSoup(htmlFile)
    allFriends = soup.findAll("div", { "class": "fsl fwb fcb" })
    friendIDs = []

    for friend in allFriends:
        datagt = friend.a.get("data-gt")
        if datagt:
            uid = json.loads(datagt)
            friendIDs.append(long(uid["engagement"]["eng_tid"]))
    return friendIDs


def sendBatch(batch):
    '''Accepts a list of dicts of each deleted friend and returns the cleaned
    list of pictures and names from the FB response'''
    deletedFriendsClean = []
    if batch:
        batch = urllib.urlencode({'batch': batch})
        response = facebookOAuth.post('/', data=batch,
                                      content_type='application/json').data
        for entry in response:
            if entry['code'] == 200:
                userInfo = json.loads(entry['body'])
                cleanFriend = {'name': userInfo['name'],
                               'pic': userInfo['picture']['data']['url']}
                deletedFriendsClean.append(cleanFriend)
    return deletedFriendsClean


@unfriended.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@unfriended.route('/', methods=['GET', 'POST'])
def index():
    if 'oauth_token' in session:
        loggedIn = True
        if request.method == 'POST' :
            fbHTML = request.files['fbHTML']
            #Make sure the user actually uploaded a file
            if fbHTML:
                user = facebookOAuth.get('/me').data
                userId = user['id']

                #BeautifulSoup can bail out if we don't provide a correct HTML file
                try:
                    currentFriends = parseFBHTML(fbHTML)
                except:
                    return render_template('index.html', loggedIn=loggedIn, deletedFriends=False,
                                            error="Error while trying to parse your HTML. Please try again.")
                #Make sure that we actually found friends in the parsed HTML file
                if currentFriends:
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
                    return render_template('index.html', loggedIn=loggedIn, deletedFriends=getFriendData(deletedFriends))
                else:
                    return render_template('index.html', loggedIn=loggedIn, deletedFriends=False,
                                            error="No friends found in file. Are you sure you have the correct HTML file?")
            else:
                return render_template('index.html', loggedIn=loggedIn, deletedFriends=False,
                                        error="Please upload a file.")
        else:
            return render_template('index.html', loggedIn=loggedIn, deletedFriends=False)
    else:
        loggedIn = False
        user = None
        return render_template('index.html', loggedIn=loggedIn)
