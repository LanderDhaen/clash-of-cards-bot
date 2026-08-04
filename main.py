import discord
from discord.ext import commands
import logging

from commands import trade
from config import (TOKEN, GUILD)

# Logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Intents

intents = discord.Intents.default()
intents.message_content = True
intents

# Bot

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready(): 
    print(f'Ready to roll, {bot.user.name}!')

# Commands

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=GUILD)
    await ctx.send('Synced!')

bot.tree.add_command(trade, guild=GUILD)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)