import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_API = os.getenv("TELEGRAM_API")

if __name__ == "__main__":
    print("The telegram token is: {}".format(TELEGRAM_API))