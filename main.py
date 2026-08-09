import logging
import discord

from typing import Literal
from discord.ext import commands
from config import TOKEN, IS_DEVELOPMENT
from data.database import create_tables

LOG_LEVEL = logging.DEBUG if IS_DEVELOPMENT else logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

START_TIME = discord.utils.utcnow()

# Initialize logging

handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
handler.setFormatter(formatter)

logger = logging.getLogger("trade_bot.main")
logger.addHandler(handler)
logger.setLevel(LOG_LEVEL)

# Initialize bot

class TradeBot(commands.Bot):

    async def setup_hook(self):

        create_tables()
        logger.info("Database tables created successfully.")
        await self.load_extension("commands.trade")
        await self.load_extension("commands.setup")
        count = await self.get_command_count()
        logger.info("%s command(s) loaded successfully.", count)

    async def on_ready(self):
        logger.info("%s is online and ready to be used!", self.user.name)

    async def get_uptime(self):
        return discord.utils.utcnow() - START_TIME

    async def get_latency(self):
        return round(self.latency * 1000, 2)

    async def get_server_count(self):
        return len(self.guilds)

    async def get_command_count(self):
        return len(self.tree.get_commands())


intents = discord.Intents.default()
intents.message_content = True

bot = TradeBot(command_prefix="dev!" if IS_DEVELOPMENT else "!", intents=intents)

# Text commands

@bot.command(name="sync")
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, scope: Literal["global", "guild"] = "guild"):
    if scope == "guild":
        bot.tree.copy_global_to(guild=ctx.guild)
        synced  = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"{len(synced)} command(s) synced for {ctx.guild.name}.")
    elif scope == "global":
        synced = await bot.tree.sync()
        await ctx.send(f"{len(synced)} command(s) synced globally.")

@bot.command(name="health")
async def health(ctx: commands.Context):

    embed = discord.Embed(title=bot.user.name, description="Currently running smoothly with the following statistics: ", color=discord.Color.green())

    uptime = await bot.get_uptime()
    uptime_str = str(uptime).split('.')[0]
    embed.add_field(name="Uptime", value=uptime_str, inline=False)

    latency = await bot.get_latency()
    latency_str = f"{latency} ms"
    embed.add_field(name="Latency", value=latency_str, inline=False)

    servers = await bot.get_server_count()
    embed.add_field(name="Servers", value=servers, inline=False)

    commands = await bot.get_command_count()
    embed.add_field(name="Commands", value=commands, inline=False)

    if ctx.author:
        requested_by_str = f"Requested by {ctx.author.display_name}"
        embed.set_footer(text=requested_by_str, icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

# Run the bot

bot.run(TOKEN, log_handler=handler, log_level=LOG_LEVEL)