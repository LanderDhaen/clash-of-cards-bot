import discord
from discord import app_commands
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Load environment variables

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = discord.Object(id=os.getenv("GUILD_ID"))

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

# Commands

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=GUILD)
    await ctx.send('Synced!')

@bot.tree.command(name="trade", description="Wissel kaarten uit met een andere speler", guild=GUILD)
@app_commands.describe(give="De kaart die je wilt geven", receive="De kaart die je wilt ontvangen")
async def trade(interaction: discord.Interaction , give: str, receive: str):
    await interaction.response.send_message(f'{interaction.user.mention} wilt een {give} geven en een {receive} ontvangen.')


bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)