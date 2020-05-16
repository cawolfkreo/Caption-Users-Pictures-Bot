from setup import TELEGRAM_API
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Meme captions bot!')

'''
This is the function called by the bot
when the "/start" command is executed.
The handler is created bellow the function
and will be given to the bot on the
startBot function
'''
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hi! I am a bot made to add messages to profiles pictures of "+
        "people on group chats! just add me to a groupchat and wait for the magic to happen!"
    )
start_handler = CommandHandler('start', start)

def startBot():
    updater = Updater(token=TELEGRAM_API, use_context=True)
    
    dispatcher = updater.dispatcher             #The start handler is given to the bot
    dispatcher.add_handler(start_handler)

    updater.start_polling()                     #Starts the bot 
    print("The bot is up!")
    updater.idle()                              #Makes sure the bot stops when ctrl+c signal is sent
    print("The bot stopped :C")
    

'''
This makes sure the bot runs even if it's launched
from the file itself and not as a module.
'''
if __name__ == "__main__":
    startBot()