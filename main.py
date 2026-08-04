import discord
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

# Views

class TradeView(discord.ui.View):
    @discord.ui.button(label="Annuleren", style=discord.ButtonStyle.secondary, emoji="🗑️")

    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None)

# Commands

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=GUILD)
    await ctx.send('Synced!')



@bot.tree.command(name="trade", description="Wissel kaarten uit voor het Clash of Cards evenement", guild=GUILD)
async def trade(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Kaarten ruilen voor het Clash of Cards evenement",
        description=(
            "Kaarten op overschot en dringend op zoek naar die laatste kaarten om je set te voltooien? Kijk snel hieronder!\n\n"
            "• Kies de kaart die je wilt weggeven\n"
            "• Kies de kaart die je wilt ontvangen\n"
            "• Kies de clan waar je de kaarten wilt ruilen\n"
        ),
        color=discord.Color.orange()
    )

    await interaction.response.send_message(embed=embed, ephemeral=True, view=TradeView())


bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)