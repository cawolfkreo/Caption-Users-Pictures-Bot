from setup import APPNAME, ISPRODUCTION, PORT, TELEGRAM_API
from telegram import MessageEntity, ChatAction, Update, update
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    PicklePersistence,
    Updater,
    callbackcontext)
import logging
from textManager import (
    getMentions,
    DictHasElems,
    isMessageFromAGroup,
    printTime,
    processImage,
    processUser,
    shouldProcessImage,
    validMessageLength)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("Meme captions bot!")

def start(update: Update, context: callbackcontext):
    '''
    This is the function called by the bot
    when the "/start" command is executed.
    '''
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I am a bot made to add messages to profiles pictures of "+
        "people on group chats! just add me to a groupchat and wait for the "+
        "magic to happen!")

def about(update: Update, context: callbackcontext):
    '''
    This is the function called by the bot
    when the "/about" command is executed.
    '''
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hello! I am a bot 🤖 made by **@Cawolf** to randomly "+
        "caption people's profile pictures. You can find my source "+
        "code [on this github repository]"+
        "(https://github.com/cawolfkreo/Caption-Users-Picures-Bot)",
        parse_mode="Markdown")

def text(update: Update, context: callbackcontext):
    '''
    This is the function called by the bot
    when the bot sees a text message.
    '''
    chat = update.effective_chat
    entities = update.message.parse_entities([MessageEntity.MENTION])
    if not (chat and isMessageFromAGroup(chat.type) and DictHasElems(entities)):
        return

    mention = getMentions(entities, MessageEntity.MENTION)
    telegramUserId = shouldProcessImage(mention, context.bot_data, context.chat_data)
    message = update.effective_message

    if not(telegramUserId and message and validMessageLength(message.text)):
        return
    
    context.bot.sendChatAction(
        chat_id = update.effective_chat.id,
        action = ChatAction.UPLOAD_PHOTO)

    userProfilePic = context.bot.getUserProfilePhotos(telegramUserId, limit = 1)
    resultImage = processImage(userProfilePic, message.text, mention)
    
    if(resultImage):
        update.message.reply_photo(photo=resultImage,)
        
        """ context.bot.sendPhoto(
            chat_id = update.effective_chat.id, 
            photo=resultImage,
            reply_to_message_id = message.message_id) """
    else:
        #if the user has no profile picture the bot will
        #default to this message as a reply.
        context.bot.sendMessage(
            chat_id = update.effective_chat.id, 
            text = ("Imagine this is the profile " +
                    f"picture of {mention} with the text " +
                    "from the message I replied (?) Sorry" +
                    "but that user privacy settings " +
                    "doesn't allow me to use his " +
                    "profile picture 😅"),
            reply_to_message_id = message.message_id)
        


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

def startBot():
    '''
    This is the starting function for the bot.
    When it's called the bot is given the handlers
    and it's execution starts.
    '''
    botPersistent = PicklePersistence(filename='sav.almcn')
    updater = Updater(token=TELEGRAM_API, persistence=botPersistent, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start, run_async=True)
    about_handler = CommandHandler('about', about, run_async=True)
    text_handler = MessageHandler(Filters.text & (~Filters.command), text, run_async=True)
    everything_handler = MessageHandler(Filters.all, everything, run_async=True)

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