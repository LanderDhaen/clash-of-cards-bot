import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=os.getenv("GUILD_ID"))
ROLE_ID = os.getenv("ROLE_ID")