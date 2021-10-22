from datetime import datetime
from telegram import base, messageentity, userprofilephotos
import imageText
from io import BytesIO
import random

userKey = "userDict"
'''
This is the key needed to access the 
user dictionary on the cotext.bot_data 
dictionary.
'''

randomKey = "randomMsg"
'''
This is the key needed to access the 
random # of messages on the cotext.chat_data 
dictionary.
'''

rndLowerBound = 1
'''
The smallest possible number the
random number generation will
generate when called.
'''

rndUpperBound = 7
'''
The biggest possible number the
random number generation will
generate when called.
'''

def printTime(textToPrint):
    now = datetime.now()
    current_time = now.strftime("[%Y/%m/%d - %r]")
    print(current_time, textToPrint)

def isMessageFromAGroup(typeOfMessage):
    return "group" in typeOfMessage or "channel" in typeOfMessage

def DictHasElems(pDict):
    """checks if a dictionary is
    not empty"""
    return not not pDict

def getMentions(entitiesDict: dict[str, str], typeToSearch: messageentity):
    for entity, text in entitiesDict.items():
        if(entity.type == typeToSearch):
            return text
    return None

def validMessageLength(message: str, mention: str):
    message = removeMention(message, mention)
    msgLen = len(message)
    return (0 < msgLen) and (msgLen < 500)

def userIDFromUsername(username: str, userDict: dict):
    validUsername = username[1:]                    #The username on the dictionary does not contain 
                                                    #the "@" at the begining. It needs to be removed
                                                    #to be a valid key for the dictionary.
    if(validUsername in userDict):
        return userDict[validUsername]
    else:
        return None

def generateRandom():
    return random.randint(rndLowerBound, rndUpperBound)  

def getUserIdFromBotData(mention: str, bot_data:dict):
    if userKey in bot_data:
        return userIDFromUsername(mention, bot_data[userKey]) 
    else:
        return None

def shouldProcessImage(mention, bot_data, chat_data):
    msgsToNextPicture = 0
    if (randomKey not in chat_data):
        msgsToNextPicture = generateRandom()
    else:
        msgsToNextPicture = chat_data[randomKey] - 1

    if (msgsToNextPicture < 1 and userKey in bot_data):
        userId = userIDFromUsername(mention, bot_data[userKey])
        if (userId):
            chat_data[randomKey] = generateRandom()
        return userId
    else:
        chat_data[randomKey] = msgsToNextPicture
        return None

def addUserIDToDict(messageUser, userDict):
    userDict[messageUser.username] = messageUser.id
    return userDict

def processUser(messageUser, bot_data):
    if(not messageUser.is_bot):
        if(userKey not in bot_data):
            newUserDict = {}
            bot_data[userKey] = addUserIDToDict(messageUser, newUserDict)
        elif(messageUser.username not in bot_data[userKey]):
            bot_data[userKey] = addUserIDToDict(messageUser, bot_data[userKey])

def removeMention(textMessage: str, mention: str):
    baseText = textMessage.replace(mention, "").replace("\n", "").strip()
    return baseText.replace("  ", " ")          #This makes sure no extra whitespaces are in the message


def processImage(userProfilePic: userprofilephotos, textMessage: str, mention: str, invert=False, name=""):
    if(userProfilePic.total_count > 0):
        profilePicture = userProfilePic.photos[0][-1].get_file()        #This is the Highest resolution of the users profile picture.
        photoByteArr = profilePicture.download_as_bytearray()

        oldImageBArr = BytesIO(photoByteArr)
        img = imageText.createImage(oldImageBArr)

        if not invert:
            imageText.addTextToProfilePicture(img, removeMention(textMessage, mention))
        else:
            img = imageText.addTextToInverseProfilePicture(img, textMessage, name)

        newImageBArr = BytesIO()
        newImageBArr.name = "response.jpg"
        img.save(newImageBArr, "PNG")
        newImageBArr.seek(0)
        return newImageBArr
    return None

if __name__ == "__main__":
    pass
