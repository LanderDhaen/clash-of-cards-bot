import logging
import discord

from classes.trade_bot import TradeBot
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

bot = TradeBot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    logger.info("%s is online and ready to be used!", bot.user.name)

# Run the bot

bot.run(TOKEN, log_handler=handler, log_level=LOG_LEVEL)