import re
from datetime import datetime

#This expression helps matching any text message that starts with @.
# A.k.a. contains a mention at the begining
startsAtRegEx = r'^@[\w\_]+(\s|$)'

def startsWithAt(textMessage):
    return re.search(startsAtRegEx, textMessage)

def messageWithoutAt(textMessage):
    return re.split(startsAtRegEx, textMessage)[-1]

def printTime(textToPrint):
    now = datetime.now()
    current_time = now.strftime("[%Y/%M/%D - %H:%M:%S]")
    print(current_time, textToPrint)
