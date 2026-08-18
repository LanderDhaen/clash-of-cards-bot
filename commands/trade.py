import discord

from discord.ext import commands
from discord import app_commands

from data.database import TradeType, get_guild, TRADE_TYPES


class Trade(commands.GroupCog, group_name="trade", group_description="Wissel kaarten uit voor het Clash of Cards evenement"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="elixir",
        description="Wissel elixirkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_elixir(self, interaction: discord.Interaction):
        await self.setup_trade(interaction, TradeType.ELIXIR)

    @app_commands.command(
        name="dark-elixir",
        description="Wissel duister-elixirkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_dark_elixir(self, interaction: discord.Interaction):
        await self.setup_trade(interaction, TradeType.DARK_ELIXIR)

    @app_commands.command(
        name="builder-base",
        description="Wissel bouwersbasiskaarten uit voor het Clash of Cards evenement"
    )
    async def trade_builder_base(self, interaction: discord.Interaction):
        await self.setup_trade(interaction, TradeType.BUILDER_BASE)


    @app_commands.command(
        name="super-troop",
        description="Wissel supertroepkaarten uit voor het Clash of Cards evenement"
    )
    async def trade_super_troop(self, interaction: discord.Interaction):
        await self.setup_trade(interaction, TradeType.SUPER_TROOP)


    async def setup_trade(
        self,
        interaction: discord.Interaction,
        trade_type: TradeType
    ):

        guild = get_guild(interaction.guild.id)

        ## TODO: Check if the guild exists and return error message if not

        guild_clans = guild.get_clans()
        name, color, cards = TRADE_TYPES[trade_type]

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
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Trade(bot))