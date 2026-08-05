import logging
import discord

from discord.ext import commands
from commands.trade import trade
from config import TOKEN, IS_DEVELOPMENT

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

# Initialize bot with intents

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info("%s is online and ready to be used!", bot.user.name)

# Commands

@bot.command(name="sync")
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, scope: str = "guild"):
    if scope == "guild":
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(synced)} command(s) to {ctx.guild.name}!")
    elif scope == "global":
        synced = await bot.tree.sync()
        await ctx.send(f"Released {len(synced)} command(s) globally!")
    else:
        await ctx.send("Invalid scope! Use 'guild' or 'global'.")

@bot.command(name="health")
async def health(ctx: commands.Context):

    embed = discord.Embed(title="Health Check", description=f"{bot.user.name} is running smoothly with the following statistics!\n\n", color=discord.Color.green())

    uptime = discord.utils.utcnow() - START_TIME    
    uptime_str = str(uptime).split('.')[0]
    embed.add_field(name="Uptime", value=uptime_str, inline=False)

    latency = round(bot.latency * 1000, 2)
    latency_str = f"{latency} ms"  
    embed.add_field(name="Latency", value=latency_str, inline=False)

    servers = len(bot.guilds)
    embed.add_field(name="Servers", value=servers, inline=False)

    if ctx.author:
        requested_by_str = f"Requested by {ctx.author.display_name}"
        embed.set_footer(text=requested_by_str, icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

bot.tree.add_command(trade)

# Run the bot

bot.run(TOKEN, log_handler=handler, log_level=LOG_LEVEL)