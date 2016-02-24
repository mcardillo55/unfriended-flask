from BeautifulSoup import BeautifulSoup
import json

def parseFBHTML(htmlFile):
    soup = BeautifulSoup(htmlFile)

    allFriends = soup.findAll("div", { "class": "fsl fwb fcb" })

    print len(allFriends)

    friendIDs = []

    for friend in allFriends:
        datagt = friend.a.get("data-gt")
        if datagt:
            uid = json.loads(datagt)
            friendIDs.append(int(uid["engagement"]["eng_tid"]))
    return friendIDs