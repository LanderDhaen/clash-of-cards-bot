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

# Lists

elixir = [
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

dark_elixir = [
    "Minion",
    "Hog Rider",
    "Valkyrie",
    "Golem",
    "Witch",
    "Lava Hound",
    "Bowler",
    "Ice Golem",
    "Head Hunter",
    "Apprentice Warden",
    "Druid",
    "Furnace",
    "Ruin Witch"
]

builder_base = [
    "Raged Barbarian",
    "Sneaky Archer",
    "Boxer Giant",
    "Beta Minion",
    "Bomber",
    "Raged Baby Dragon",
    "Cannon Cart",
    "Night Witch",
    "Drop Ship",
    "Power P.E.K.K.A.",
    "Hog Glider"
]

super_troop = [
    "Super Barbarian",
    "Super Archer",
    "Super Giant",
    "Sneaky Goblin",
    "Super Wall Breaker",
    "Rocket Balloon",
    "Super Wizard",
    "Super Dragon",
    "Inferno Dragon",
    "Super Miner",
    "Super Yeti",
    "Super Minion",
    "Super Hog Rider",
    "Super Valkyrie",
    "Super Witch",
    "Ice Hound",
    "Super Bowler"
]

clans = [
    {"name": "Dutch Legion 3", "tag": "28UYR0CVU"},
    {"name": "Dutch Legion CW", "tag": "29RPVGYU8"},
    {"name": "Dutch Legion 4", "tag": "2J0C28R2J"},
    {"name": "DL Gold", "tag": "2RV80YRPY"},
    {"name": "DL Azure", "tag": "2JJ22CPUV"},
    {"name": "DL Silver", "tag": "2RPQRYRUY"},
    {"name": "DL Mini", "tag": "2JY9C0L0P"},
    {"name": "DL Ruby", "tag": "2RCQPJGQY"},
    {"name": "DL eSports", "tag": "2R0GUP2Q8"},
    {"name": "DL eSports X", "tag": "2CYCCVQLL"},
]

# Views 

class TradeView(discord.ui.View):

    def __init__(self, color, cards):
        super().__init__(timeout=300)
        self.give = None
        self.receive = None
        self.clan_tag = None
        self.clan_name = None

        self.color = color
        self.cards = cards

        # Selects

        self.give_select = discord.ui.Select(
            placeholder="Kies de kaart die je wilt weggeven",
            options=[discord.SelectOption(label=card) for card in cards],
            min_values=1,
            max_values=1
        )

        self.give_select.callback = self.give_select_callback
        self.add_item(self.give_select)

        self.receive_select = discord.ui.Select(
            placeholder="Kies de kaart die je wilt ontvangen",
            options=[discord.SelectOption(label=card) for card in cards],
            min_values=1,
            max_values=1
        )

        self.receive_select.callback = self.receive_select_callback
        self.add_item(self.receive_select)

        self.clan_select = discord.ui.Select(
            placeholder="Kies de clan waar je de kaarten wilt ruilen",
            options=[discord.SelectOption(label=clan["name"], value=clan["tag"]) for clan in clans],
            min_values=1,
            max_values=1
        )

        self.clan_select.callback = self.clan_select_callback
        self.add_item(self.clan_select)

        # Buttons

        self.accept_button = discord.ui.Button(
            label="Bevestigen",
            style=discord.ButtonStyle.success
        )

        self.accept_button.callback = self.accept_button_callback
        self.add_item(self.accept_button)

        self.cancel_button = discord.ui.Button(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )   

        self.cancel_button.callback = self.cancel_button_callback
        self.add_item(self.cancel_button)

    # Callbacks

    async def give_select_callback(self, interaction: discord.Interaction):
        self.give = self.give_select.values[0]
        await interaction.response.defer()

    async def receive_select_callback(self, interaction: discord.Interaction):
        self.receive = self.receive_select.values[0] 
        await interaction.response.defer()

    async def clan_select_callback(self, interaction: discord.Interaction):
        self.clan_tag = self.clan_select.values[0]
        self.clan_name = next((clan["name"] for clan in clans if clan["tag"] == self.clan_tag)) 
        await interaction.response.defer()

    async def accept_button_callback(self, interaction: discord.Interaction):

        await interaction.response.edit_message(content="Je ruilvoorstel is verzonden!", embed=None, view=None)

        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{interaction.user.mention} wil kaarten ruilen in **{self.clan_name}**:\n"
                ),
            color=self.color
        )

        visit_clan_button = discord.ui.Button(label="Bekijk de ruil", style=discord.ButtonStyle.link, url=f"https://link.clashofclans.com/en?action=OpenClanProfile&tag={self.clan_tag}")

        embed.add_field(name="Weggeven", value=f'• {self.give}', inline=True)
        embed.add_field(name="Ontvangen", value=f'• {self.receive}', inline=True)

        await interaction.channel.send(embed=embed, view=discord.ui.View().add_item(visit_clan_button))

    async def cancel_button_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None)

# Functions

async def build_trade(interaction: discord.Interaction, color, cards):
    embed = discord.Embed(
        title="Clash of Cards",
        description=(
            "Kaarten op overschot en dringend op zoek naar die laatste kaarten om je set te voltooien? Kijk snel hieronder!\n\n"
            "• Kies de kaart die je wilt weggeven\n"
            "• Kies de kaart die je wilt ontvangen\n"
            "• Kies de clan waar je wilt ruilen\n"
        ),
        color=color
    )

    await interaction.response.send_message(embed=embed, ephemeral=True, view=TradeView(color, cards))

# Commands

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=GUILD)
    await ctx.send('Synced!')

trade = app_commands.Group(name="trade", description="Wissel kaarten uit voor het Clash of Cards evenement")

@trade.command(name="elixir", description="Wissel elixirkaarten uit voor het Clash of Cards evenement")
async def trade_elixir(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.pink(), elixir)

@trade.command(name="dark-elixir", description="Wissel duister-elixirkaarten uit voor het Clash of Cards evenement")
async def trade_dark_elixir(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.dark_purple(), dark_elixir)

@trade.command(name="builder-base", description="Wissel bouwersbasiskaarten uit voor het Clash of Cards evenement")
async def trade_builder_base(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.blue(), builder_base)

@trade.command(name="super-troop", description="Wissel supertroepkaarten uit voor het Clash of Cards evenement")
async def trade_super_troop(interaction: discord.Interaction):
    await build_trade(interaction, discord.Color.orange(), super_troop)

bot.tree.add_command(trade, guild=GUILD)

bot.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)