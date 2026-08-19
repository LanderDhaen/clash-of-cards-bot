import discord

from discord.ext import commands
from discord import app_commands

from data.database import TradeType, get_guild, TRADE_TYPES
from views.trade_setup import TradeSetupView


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

        ## Check if the server is set up

        guild = get_guild(interaction.guild.id)

        if not guild:

            embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is nog niet ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)


        guild_clans = guild.get_clans()
        color, cards = TRADE_TYPES[trade_type]
        
        trade_setup_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                "Kaarten op overschot en dringend op zoek naar die laatste kaarten om je set te voltooien? Kijk snel hieronder!\n\n"
                f"• Kies de kaarten die je wilt weggeven\n"
                f"• Kies de kaarten die je wilt ontvangen\n\n"
            ),
            color=color
        )

        if guild_clans:
            trade_setup_embed.description += "• Kies de clan waar je de kaarten wilt ruilen\n"                                

        trade_setup_view = TradeSetupView(trade_type, guild)

        await interaction.response.send_message(
            embed=trade_setup_embed,
            view=trade_setup_view,
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Trade(bot))