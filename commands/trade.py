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
        name, color, cards = TRADE_TYPES[trade_type]
        
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

    @app_commands.command(
        name="matches",
        description="Vind mogelijke voorstellen die je kan accepteren"
    )
    async def trade_matches(self, interaction: discord.Interaction):
        
        ## Check if the server is set up

        guild = get_guild(interaction.guild.id)

        if not guild:

            embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is nog niet ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        open_user_trades = guild.open_user_trades(interaction.user.id)

        if not open_user_trades:

            embed = discord.Embed(
                title="Clash of Cards",
                description=f"Je hebt geen openstaande ruilvoorstellen in **{interaction.guild.name}**.\n\n"
                            f"Maak een voorstel aan met `/trade`!",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        matching_trades_message_embed = discord.Embed(
            title="Clash of Cards",
            description="Hieronder vind je de mogelijke voorstellen die je kan accepteren:\n\n",
            color=discord.Color.green()
        )           

 

        for index, open_trade in enumerate(open_user_trades, start=1):

            possible_trades = open_trade.matching_trades()

            value = ""

            if possible_trades:

                for possible_trade in possible_trades:
                    initiator = interaction.guild.get_member(possible_trade.initiator_id)

                    value += f"• [Bekijk de ruil](https://discord.com/channels/{possible_trade.guild.guild_id}/{possible_trade.guild.trade_channel_id}/{possible_trade.message_id}) van {initiator.mention}\n"
            else:
                value = "-# • *Geen mogelijke voorstellen gevonden*"

            name, color, cards = TRADE_TYPES[TradeType(open_trade.type)]

            matching_trades_message_embed.add_field(
                name=f"{index}. {name}",
                value=value,
                inline=False
            )

        await interaction.response.send_message(
            embed=matching_trades_message_embed,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Trade(bot))