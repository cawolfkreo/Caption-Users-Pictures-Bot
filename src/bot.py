import logging
from datetime import datetime
from pathlib import Path
from telegram import MessageEntity, Update, UserProfilePhotos
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    filters,
    MessageHandler,
    PicklePersistence,
    ContextTypes)
from textManager import (
    getMentions,
    DictHasElems,
    isMessageFromAGroup,
    printTime,
    processImage,
    processUser,
    shouldProcessImage,
    validMessageLength,
    getUserIdFromBotData)
from setup import URL, ISPRODUCTION, PORT, TELEGRAM_API

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger("Meme captions bot!")

STARTUP_TIME = datetime.now().timestamp()
'''
Constant for the current bot status
'''

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    This is the function called by the bot
    when the "/start" command is executed.
    '''
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I am a bot made to add messages to profiles pictures of "+
        "people on group chats! just add me to a group chat and wait for the "+
        "magic to happen!")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    This is the function called by the bot
    when the "/about" command is executed.
    '''
    await context.bot.send_message(
        chat_id= update.effective_chat.id, 
        text=f"Hello! I am a bot 🤖 made by **@Cawolf** to randomly "+
        "caption people's profile pictures. You can find my source "+
        "code [on this github repository.]"+
        "(https://github.com/cawolfkreo/Caption-Users-Picures-Bot)",
        parse_mode="Markdown")

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    This function is called by the bot
    when it sees a text message.
    '''

    chat = update.effective_chat

    if not update.message:
        return
    
    if update.message.date.timestamp() < STARTUP_TIME:
        return

    entities = update.message.parse_entities([MessageEntity.MENTION])
    if not (chat and isMessageFromAGroup(chat.type) and DictHasElems(entities)):
        return

    mention = getMentions(entities, MessageEntity.MENTION)
    telegramUserId = shouldProcessImage(mention, context.bot_data, context.chat_data)
    message = update.effective_message

    if not(telegramUserId and message and validMessageLength(message.text, mention)):
        return
    
    await context.bot.sendChatAction(
        chat_id = update.effective_chat.id,
        action = ChatAction.UPLOAD_PHOTO)

    userProfilePic = await context.bot.getUserProfilePhotos(telegramUserId, limit = 1)
    resultImage = await processImage(userProfilePic, message.text, mention)
    
    if(resultImage):
        await update.message.reply_photo(photo=resultImage,)
    else:
        #if the user has no profile picture the bot will
        #default to this message as a reply.
        await context.bot.sendMessage(
            chat_id = update.effective_chat.id, 
            text = ("Imagine this is the profile " +
                    f"picture of {mention} with the text " +
                    "from the message I replied (?) Sorry " +
                    "but that user privacy settings " +
                    "doesn't allow me to use his " +
                    "profile picture 😅"),
            reply_to_message_id = message.message_id)
        
async def evilMeme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    This is the function called by the bot
    when the bot sees the /evil command.
    '''
    chat = update.effective_chat    
    if not (chat and isMessageFromAGroup(chat.type)):
        # We are not on a group
        await update.message.reply_text("Sorry you can only " +
                            "use this command in groups 😅")
        return

    if not update.message:
        return

    entities = update.message.parse_entities([MessageEntity.MENTION])
    if not entities:
        # the user didn't mentioned another user by their alias
        await update.message.reply_text("Sorry to use this command " +
                            "you need to provide a username alias " +
                            "after the /evil 😅\nExample: " +
                            "/evil @someUserAlias name any bottom text here")
        return    

    mention = getMentions(entities, MessageEntity.MENTION)
    del context.args[0]
    if mention == context.bot.name:
        #sorry but I cannot use this on myself 
        await update.message.reply_text("sorry but I cannot use this on myself " +
                            "Try somebody else, I appreciate the gesture btw 🤖👍")
        return

    telegramUserId = getUserIdFromBotData(mention, context.bot_data)
    if not telegramUserId:
        # We couldn't find the userId
        await update.message.reply_text("Sorry for some reason I am not able " +
                            "to find that user. Telegram is not allowing " +
                            "me to look it up at the moment 😓")
        return
    
    if (len(context.args) == 0 or not context.args[0]):
        # the user didn't provide the name
        await update.message.reply_text("Sorry to use this command " +
                            "you need to provide the name of the " +
                            "user after the alias 😢.\n" 
                            "Example:\n " +
                            "/evil @someUserAlias name any bottom text here")
        return
    name = context.args[0]
    del context.args[0]

    message = update.effective_message
    textToDisplay = " ".join(context.args).strip()
    if not(message and textToDisplay and validMessageLength(textToDisplay, mention)):
        # the user didn't provide the text
        await update.message.reply_text("Sorry to use this command " +
                            "you need to provide the text " +
                            "to display at the bottom after " +
                            "the image 😢.\nExample:\n" +
                            "/evil @someUserAlias name any bottom text here")
        return
    
    await context.bot.sendChatAction(
        chat_id = update.effective_chat.id,
        action = ChatAction.UPLOAD_PHOTO)

    userProfilePic: UserProfilePhotos = await context.bot.getUserProfilePhotos(telegramUserId, limit = 1)
    resultImage = await processImage(userProfilePic, textToDisplay, mention, True, name)
    
    if resultImage:
        await update.message.reply_photo(photo=resultImage)
    else:
        #if the user has no profile picture the bot will
        #default to this message as a reply.
        await context.bot.sendMessage(
            chat_id = update.effective_chat.id, 
            text = ("Imagine this is the profile " +
                    f"picture of {mention} with the text " +
                    "from the message I replied (?) " +
                    "Sorry but that user privacy settings " +
                    "doesn't allow me to use his " +
                    "profile picture 😅"),
            reply_to_message_id = message.message_id)

'''
This is the function called by the bot
when the bot sees any message. The idea
is that the bot will store the userIDs
of every group message it sees.
'''
async def everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if(chat and isMessageFromAGroup(chat.type)):
        messageUser = update.effective_user
        processUser(messageUser, context.bot_data)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Logs the error and prevents bot from crashing... I hope'''
    printTime(logger, "The bot has found an error!")
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def startBot():
    '''
    This is the starting function for the bot.
    When it's called the bot is given the handlers
    and it's execution starts.
    '''
    Path("data").mkdir(parents=True, exist_ok=True)
    botPersistent = PicklePersistence(filepath="data/sav.almcn")

    application = (
        Application.builder()
        .token(TELEGRAM_API)
        .persistence(botPersistent)
        .build()
    )

    start_handler = CommandHandler('start', start)
    about_handler = CommandHandler('about', about)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), text)
    evil_handler = CommandHandler("evil", evilMeme)
    everything_handler = MessageHandler(filters.ALL, everything)

    application.add_handler(start_handler)                   #The start handler is given to the bot
    application.add_handler(about_handler)                   #The about handler is given to the bot
    application.add_handler(text_handler)                    #The text handler is given to the bot
    application.add_handler(evil_handler)                    #The evil meme handler is given to the bot
    application.add_handler(everything_handler, group = 1)   #The default handler is given to the bot

    application.add_error_handler(error_handler)

    printTime(logger, "The bot is starting... :)")
    
    if(ISPRODUCTION):
        webhook = f"https://{URL}/{TELEGRAM_API}"
        application.run_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TELEGRAM_API,
                                webhook_url=webhook)
    else:
        application.run_polling()                             #Starts the bot 
    printTime(logger, "The bot stopped :C")

'''
This makes sure the bot run even if it's launched
from the file itself and not as a module.
'''
if __name__ == "__main__":
    startBot()