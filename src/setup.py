import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API = os.getenv("TELEGRAM_API")
ISPRODUCTION = os.getenv("ISPRODUCTION")
APPNAME = os.getenv("APPNAME")
PORT = 1
if (ISPRODUCTION):
    PORT = int(os.environ.get("PORT", os.getenv("PORT")))

if __name__ == "__main__":
    print("The telegram token is: {}".format(TELEGRAM_API))