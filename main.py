import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents

intents = discord.Intents.default()
intents.message_content = True

# Bot

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready(): 
    print(f'Ready to roll, {bot.user.name}!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)