import discord
from discord import app_commands
from discord.ext import commands
import logging

from config import (TOKEN, GUILD)
from data.cards import ELIXIR, DARK_ELIXIR, BUILDER_BASE, SUPER_TROOP
from views.trade_setup import TradeSetupView

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


# Functions

async def build_trade(interaction: discord.Interaction, color, cards):

    embed = discord.Embed(
        title="Clash of Cards",
        description=(
            "Kaarten op overschot en dringend op zoek naar die laatste kaarten om je set te voltooien? Kijk snel hieronder!\n\n"
            "• Kies de kaarten die je wilt weggeven\n"
            "• Kies de kaarten die je wilt ontvangen\n"
            "• Kies de clan waar je de kaarten wilt ruilen\n"
        ),
        color=color
    )

    await interaction.response.send_message(embed=embed, ephemeral=True, view=TradeSetupView(color, cards))

# Commands

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=GUILD)
    await ctx.send('Synced!')

trade = app_commands.Group(name="trade", description="Wissel kaarten uit voor het Clash of Cards evenement")

@trade.command(name="elixir", description="Wissel elixirkaarten uit voor het Clash of Cards evenement")
async def trade_elixir(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.pink(), ELIXIR)

@trade.command(name="dark-elixir", description="Wissel duister-elixirkaarten uit voor het Clash of Cards evenement")
async def trade_dark_elixir(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.dark_purple(), DARK_ELIXIR)

@trade.command(name="builder-base", description="Wissel bouwersbasiskaarten uit voor het Clash of Cards evenement")
async def trade_builder_base(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.blue(), BUILDER_BASE)

@trade.command(name="super-troop", description="Wissel supertroepkaarten uit voor het Clash of Cards evenement")
async def trade_super_troop(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.orange(), SUPER_TROOP)

bot.tree.add_command(trade, guild=GUILD)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)