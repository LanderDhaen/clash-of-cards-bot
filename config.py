import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
IS_DEVELOPMENT = os.getenv("ENV") == "development"