from setup import APPNAME, ISPRODUCTION, PORT, TELEGRAM_API
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
    PicklePersistence,
    Updater)
import logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("Meme captions bot!")

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
        "people on group chats! just add me to a groupchat and wait for the "+
        "magic to happen!")
start_handler = CommandHandler('start', start)

'''
This is the function called by the bot
when the "/about" command is executed.
The handler is created bellow the function
and will be given to the bot on the
startBot function.
'''
def about(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! I am a bot 🤖 made by **@Cawolf** to randomly "+
        "caption people's profile pictures. You can find my source "+
        "code [on this github repository]"+
        "(https://github.com/cawolfkreo/Caption-Users-Picures-Bot)",
        parse_mode="Markdown")
about_handler = CommandHandler('about', about)

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
        if(telegramUserId and update.effective_message and len(update.effective_message.text) < 500):
            context.bot.sendChatAction(
                chat_id = update.effective_chat.id,
                action = ChatAction.UPLOAD_PHOTO)

            message = update.effective_message
            userProfilePic = context.bot.getUserProfilePhotos(telegramUserId, limit = 1)
            resultImage = processImage(userProfilePic, message.text, mention)
            
            if(resultImage):
                context.bot.sendPhoto(
                    chat_id = update.effective_chat.id, 
                    photo=resultImage,
                    reply_to_message_id = message.message_id)
            else:
                #if the user has no profile picture the bot will
                #default to this message as a reply.
                context.bot.sendMessage(
                    chat_id = update.effective_chat.id, 
                    text = ("Imagine this is the non existant profile " +
                            "picture of {} with the text from the " + 
                            "message I replied (?) 😅").format(mention),
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
    botPersistent = PicklePersistence(filename='sav.almcn')
    updater = Updater(token=TELEGRAM_API, persistence=botPersistent, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)                   #The start handler is given to the bot
    dispatcher.add_handler(about_handler)                   #The about handler is given to the bot
    dispatcher.add_handler(text_handler)                    #The text handler is given to the bot
    dispatcher.add_handler(everything_handler, group = 1)   #The default handler is given to the bot

    if(ISPRODUCTION):
        updater.start_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TELEGRAM_API)
        webhook = "https://{}.herokuapp.com/{}".format(APPNAME, TELEGRAM_API)
        updater.bot.set_webhook(webhook)                    #starts the bot if it is hosted on Heroku
    else:
        updater.start_polling()                             #Starts the bot 
    printTime("The bot is up! :)")
    updater.idle()                                          #Makes sure the bot stops when the ctrl+c signal is sent
    printTime("The bot stopped :C")


'''
This makes sure the bot runs even if it's launched
from the file itself and not as a module.
'''
if __name__ == "__main__":
    startBot()