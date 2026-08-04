import logging
import discord

from classes.trade_bot import TradeBot

from config import TOKEN, GUILD, IS_DEVELOPMENT

# Create an instance of the bot

intents = discord.Intents.default()
intents.message_content = True


bot = TradeBot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online and ready to be used!")

# Create an instance of the logger

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

if IS_DEVELOPMENT:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
handler.setFormatter(formatter)

# Run the bot

bot.run(TOKEN, log_handler=handler)