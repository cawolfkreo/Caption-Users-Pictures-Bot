from datetime import datetime

def messageWithoutAt(textMessage):
    return re.split(startsAtRegEx, textMessage)[-1]

def printTime(textToPrint):
    now = datetime.now()
    current_time = now.strftime("[%Y/%m/%d - %r]")
    print(current_time, textToPrint)

def isMessageFromAGroup(typeOfMessage):
    return "group" in typeOfMessage or "channel" in typeOfMessage

def isEmptyDict(pDict):
    return bool(pDict)

def getMentions(entitiesDict, typeToSearch):
    mentions = None
    for entity, text in entitiesDict.items():
        print (entity.type, text)
        if(entity.type == typeToSearch):
            return text
    return mentions

def userIDFromUsername(username, userDict):
    for usr, telegramId in userDict.items():
        if(username == usr):
            return telegramId
    return None

def addUserIDToDict(username, userID, userDict):
    userDict[username] = userID
    return userDict

def processImage(mention, chatData):
    userId = userIDFromUsername(mention, chatData["userDict"])
    return userId

if __name__ == "__main__":
    printTime("test")
    users = {"@cawolf": 1, "@test": 2 }
    cawolf = userIDFromUsername("@cawolf", users)
    none = userIDFromUsername("lel, nada", users)
    print("cawolf: {} none: {}".format(cawolf, none))
    addedDict = addUserIDToDict("test", 1, {"a": 2})
    print("The dictionary: {}" .format(addedDict))