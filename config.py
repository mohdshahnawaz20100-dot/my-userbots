# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "my_userbot"
OWNER_ID = int(os.getenv("OWNER_ID", 0))
BOT_NAME = "My Userbot"
