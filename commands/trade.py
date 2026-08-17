import discord

from discord.ext import commands
from discord import app_commands

from data.cards import ELIXIR, DARK_ELIXIR, BUILDER_BASE, SUPER_TROOP
from data.database import get_guild
from views.trade_setup import TradeSetupView


class Trade(commands.GroupCog, group_name="trade", group_description="Wissel kaarten uit voor het Clash of Cards evenement"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="elixir",
        description="Wissel elixirkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_elixir(self, interaction: discord.Interaction):
        await self.setup_trade(
            interaction,
            discord.Color.pink(),
            ELIXIR
        )

    @app_commands.command(
        name="dark-elixir",
        description="Wissel duister-elixirkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_dark_elixir(self, interaction: discord.Interaction):
        await self.setup_trade(
            interaction,
            discord.Color.dark_purple(),
            DARK_ELIXIR
        )

    @app_commands.command(
        name="builder-base",
        description="Wissel bouwersbasiskaarten uit voor het Clash of Cards evenement"
    )
    async def trade_builder_base(self, interaction: discord.Interaction):
        await self.setup_trade(
            interaction,
            discord.Color.blue(),
            BUILDER_BASE
        )

    @app_commands.command(
        name="super-troop",
        description="Wissel supertroepkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_super_troop(self, interaction: discord.Interaction):
        await self.setup_trade(
            interaction,
            discord.Color.orange(),
            SUPER_TROOP
        )

    async def setup_trade(
        self,
        interaction: discord.Interaction,
        color: discord.Color,
        cards: list[str]
    ):

        guild = get_guild(interaction.guild.id)
        guild_clans = guild.get_clans()
        
        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                "Kaarten op overschot en dringend op zoek naar die laatste kaarten "
                "om je set te voltooien? Kijk snel hieronder!\n\n"
                "• Kies de kaarten die je wilt weggeven\n"
                "• Kies de kaarten die je wilt ontvangen\n"
            ),
            color=color
        )

        if guild_clans:
            embed.description += "• Kies de clan waar je de kaarten wilt ruilen\n"

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
            view=TradeSetupView(color, cards, guild_clans)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Trade(bot))