import discord
from discord import app_commands

from data.cards import ELIXIR, DARK_ELIXIR, BUILDER_BASE, SUPER_TROOP
from views.trade_setup import TradeSetupView


trade = app_commands.Group(
    name="trade",
    description="Wissel kaarten uit voor het Clash of Cards evenement"
)

@trade.command(name="elixir", description="Wissel elixirkaarten uit voor het Clash of Cards evenement")
async def trade_elixir(interaction: discord.Interaction):
    await setup_trade(interaction, discord.Color.pink(), ELIXIR)

@trade.command(name="dark-elixir", description="Wissel duister-elixirkaarten uit voor het Clash of Cards evenement")
async def trade_dark_elixir(interaction: discord.Interaction):
    await setup_trade(interaction, discord.Color.dark_purple(), DARK_ELIXIR)

@trade.command(name="builder-base", description="Wissel bouwersbasiskaarten uit voor het Clash of Cards evenement")
async def trade_builder_base(interaction: discord.Interaction):
    await setup_trade(interaction, discord.Color.blue(), BUILDER_BASE)

@trade.command(name="super-troop", description="Wissel supertroepkaarten uit voor het Clash of Cards evenement")
async def trade_super_troop(interaction: discord.Interaction):
    await setup_trade(interaction, discord.Color.orange(), SUPER_TROOP)


async def setup_trade(interaction: discord.Interaction, color: discord.Color, cards: list[str]):
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