from setup import TELEGRAM_API
from textManager import (
    getMentions,
    isNoEmptyDict,
    isMessageFromAGroup,
    printTime,
    processImage,
    processUser,
    shouldProcessImage)
from telegram import MessageEntity, ChatAction
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater)
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Meme captions bot!')

'''
This is the function called by the bot
when the "/start" command is executed.
The handler is created bellow the function
and will be given to the bot on the
startBot function.
'''
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I am a bot made to add messages to profiles pictures of "+
        "people on group chats! just add me to a groupchat and wait for the magic to happen!")
start_handler = CommandHandler('start', start)

'''
This is the function called by the bot
when the bot sees a text message. The
handler is created bellow the function
and will be given to the bot on the 
startBot function.
'''
def text(update, context):
    chat = update.effective_chat
    entities = update.message.parse_entities()
    if(chat and isMessageFromAGroup(chat.type) and isNoEmptyDict(entities)):
        mention = getMentions(entities, MessageEntity.MENTION)
        telegramUserId = shouldProcessImage(mention, context.bot_data, context.chat_data)
        if(telegramUserId and update.effective_message):
            context.bot.sendChatAction(
                chat_id = update.effective_chat.id,
                action = ChatAction.UPLOAD_PHOTO)

            message = update.effective_message
            userProfilePic = context.bot.getUserProfilePhotos(telegramUserId, limit = 1)
            resultImage = processImage(userProfilePic, message.text, mention)
            
            if(resultImage):
                context.bot.sendPhoto(chat_id = update.effective_chat.id, photo=resultImage)
            else:
                context.bot.send_message(
                    chat_id = update.effective_chat.id, 
                    text = ("Imagine this is the profile picture of {} " +
                            "with the text from the message I replied (?) " + 
                            "😅").format(mention),
                    reply_to_message_id = message.message_id)
text_handler = MessageHandler(Filters.text & (~Filters.command), text)

'''
This is the function called by the bot
when the bot sees any message. The idea
is that the bot will store the userIDs
of every group message it sees.
'''
def everything(update, context):
    chat = update.effective_chat
    if(chat and isMessageFromAGroup(chat.type)):
        messageUser = update.effective_user
        processUser(messageUser, context.bot_data)
everything_handler = MessageHandler(Filters.all, everything)

'''
This is the starting function for the bot.
When it's called the bot is given the handlers
and it's execution starts.
'''
def startBot():
    updater = Updater(token=TELEGRAM_API, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)                   #The start handler is given to the bot
    dispatcher.add_handler(text_handler)                    #The text handler is given to the bot
    dispatcher.add_handler(everything_handler, group = 1)   #The default handler is given to the bot

    updater.start_polling()                                 #Starts the bot 
    printTime("The bot is up! :)")
    updater.idle()                                          #Makes sure the bot stops when the ctrl+c signal is sent
    printTime("The bot stopped :C")


'''
This makes sure the bot runs even if it's launched
from the file itself and not as a module.
'''
if __name__ == "__main__":
    startBot()