import discord
from discord import app_commands
from discord.ext import commands
import logging

from config import (TOKEN, GUILD, ROLE_ID)
from data.clans import CLANS
from data.cards import ELIXIR, DARK_ELIXIR, BUILDER_BASE, SUPER_TROOP
from views.trade_result import TradeResultView

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

# Views

class TradeView(discord.ui.View):

    def __init__(self, color, cards):
        super().__init__(timeout=300)
        self.give = []
        self.receive = []
        self.clan_tag = None
        self.clan_name = None

        self.color = color
        self.cards = cards

        max_values = len(cards)

        # Selects

        self.give_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt weggeven",
            options=[discord.SelectOption(label=card) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.give_select.callback = self.give_select_callback
        self.add_item(self.give_select)

        self.receive_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt ontvangen",
            options=[discord.SelectOption(label=card) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.receive_select.callback = self.receive_select_callback
        self.add_item(self.receive_select)

        self.clan_select = discord.ui.Select(
            placeholder="Kies de clan waar je de kaarten wilt ruilen",
            options=[discord.SelectOption(label=clan["name"], value=clan["tag"]) for clan in CLANS],
            min_values=1,
            max_values=1
        )

        self.clan_select.callback = self.clan_select_callback
        self.add_item(self.clan_select)

        # Buttons

        self.accept_button = discord.ui.Button(
            label="Bevestigen",
            style=discord.ButtonStyle.primary
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
        self.give = self.give_select.values
        await interaction.response.defer()

    async def receive_select_callback(self, interaction: discord.Interaction):
        self.receive = self.receive_select.values
        await interaction.response.defer()

    async def clan_select_callback(self, interaction: discord.Interaction):
        self.clan_tag = self.clan_select.values[0]
        self.clan_name = next((clan["name"] for clan in CLANS if clan["tag"] == self.clan_tag))
        await interaction.response.defer()

    async def accept_button_callback(self, interaction: discord.Interaction):

        await interaction.response.edit_message(content="Je ruilvoorstel is verzonden!", embed=None, view=None, delete_after=60)
            
        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{interaction.user.mention} wilt kaarten ruilen in **{self.clan_name}**:\n"
                ),
            color=self.color
        )

        embed.add_field(name="Weggeven", value="\n".join(f"• {card}" for card in self.give), inline=True)
        embed.add_field(name="Ontvangen", value="\n".join(f"• {card}" for card in self.receive), inline=True)

        await interaction.channel.send(content=f'<@&{ROLE_ID}>', embed=embed, view=TradeResultView(self.clan_tag, self.give, self.receive))

    async def cancel_button_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None, delete_after=60)

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

    await interaction.response.send_message(embed=embed, ephemeral=True, view=TradeView(color, cards))

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