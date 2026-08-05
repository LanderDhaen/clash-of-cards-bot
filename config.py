import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_ID = os.getenv("ROLE_ID")
IS_DEVELOPMENT = os.getenv("ENV") == "development"