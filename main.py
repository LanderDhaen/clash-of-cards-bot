import logging
import discord

from discord.ext import commands
from commands.trade import trade
from config import TOKEN, IS_DEVELOPMENT

LOG_LEVEL = logging.DEBUG if IS_DEVELOPMENT else logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Initialize logging

handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
handler.setFormatter(formatter)

logger = logging.getLogger("trade_bot.main")
logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)

# Initialize bot with intents

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info("%s is online and ready to be used!", bot.user.name)

# Commands

@bot.command(name="sync", help="Sync the bot commands within the guild.")
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context):
    synced = await bot.tree.sync(guild=ctx.guild)
    await ctx.send(f"Synced {len(synced)} command(s) to {ctx.guild.name}!")

@bot.command(name="release", help="Release the commands globally.")
@commands.guild_only()
@commands.is_owner()
async def release(ctx: commands.Context):
    synced = await bot.tree.sync()
    await ctx.send(f"Released {len(synced)} command(s) globally!")


bot.tree.add_command(trade)

# Run the bot

bot.run(TOKEN, log_handler=handler, log_level=LOG_LEVEL)