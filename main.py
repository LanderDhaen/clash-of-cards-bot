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

# Lists

cards = [
    "Barbarian",
    "Archer",
    "Giant",
    "Goblin",
    "Wall Breaker",
    "Balloon",
    "Wizard",
    "Healer",
    "Dragon",
    "P.E.K.K.A.",
    "Baby Dragon",
    "Miner",
    "Electro Dragon",
    "Yeti",
    "Dragon Rider",
    "Electro Titan",
    "Root Rider",
    "Thrower",
    "Meteor Golem"
]

clans = [
    {"name": "Dutch Legion 3", "tag": "#28UYR0CVU"},
    {"name": "Dutch Legion CW", "tag": "#29RPVGYU8"},
    {"name": "Dutch Legion 4", "tag": "#2J0C28R2J"},
    {"name": "DL Gold", "tag": "#2RV80YRPY"},
    {"name": "DL Azure", "tag": "#2JJ22CPUV"},
    {"name": "DL Silver", "tag": "#2RPQRYRUY"},
    {"name": "DL Mini", "tag": "#2JY9C0L0P"},
    {"name": "DL Ruby", "tag": "#2RCQPJGQY"},
    {"name": "DL eSports", "tag": "#2R0GUP2Q8"},
    {"name": "DL eSports X", "tag": "#2CYCCVQLL"},
]

# Views

class TradeEmbed(discord.ui.View):
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
    

class TradeView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)
        self.give = None
        self.receive = None
        self.clan = None

    @discord.ui.select(placeholder="Kies de kaart die je wilt weggeven", options=[discord.SelectOption(label=card) for card in cards], min_values=1, max_values=1)
    async def give_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.give = select.values[0]
        await interaction.response.defer()


    @discord.ui.select(placeholder="Kies de kaart die je wilt ontvangen", options=[discord.SelectOption(label=card) for card in cards], min_values=1, max_values=1)
    async def receive_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.receive = select.values[0] 
        await interaction.response.defer()

    @discord.ui.select(placeholder="Kies de clan waar je de kaarten wilt ruilen", options=[discord.SelectOption(label=clan["name"], value=clan["tag"]) for clan in clans], min_values=1, max_values=1)
    async def clan_select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.clan = select.values[0] 
        await interaction.response.defer()

    @discord.ui.button(label="Bevestigen", style=discord.ButtonStyle.success)
    async def accept_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(content=f'{interaction.user.mention} wilt **{self.give}** weggeven en **{self.receive}** ontvangen in **{self.clan }**.', embed=None, view=None)
        await interaction.response.defer()

    @discord.ui.button(label="Annuleren", style=discord.ButtonStyle.secondary, emoji="🗑️")
    async def cancel_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
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