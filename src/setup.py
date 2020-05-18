import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API = os.getenv("TELEGRAM_API")
ISPRODUCTION = os.getenv("ISPRODUCTION") == "TRUE"
APPNAME = os.getenv("APPNAME")
PORT = 1
if (ISPRODUCTION):
    PORT = int(os.environ.get("PORT", "8443"))

if __name__ == "__main__":
    print("The telegram token is: {}".format(TELEGRAM_API))