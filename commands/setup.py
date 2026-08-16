import re
import aiohttp
import discord

from discord.ext import commands
from discord import app_commands
from config import CLAN_TAG_REGEX
from data.database import Guild, get_guild, update_settings

class Setup(commands.GroupCog, group_name="setup", group_description="Stel Clash of Cards Trader in"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="server",
        description="Voeg de rol en kanaal toe  aan de server waarmee de bot ruilen kan plaatsen"
    )
    @app_commands.describe(trader_role="De rol die gepinged wordt bij het aanmaken van een ruil", trade_channel="Het kanaal waar de ruilen geplaatst worden")
    @app_commands.rename(trader_role="trader-role", trade_channel="trade-channel")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def setup_server(
        self,
        interaction: discord.Interaction,
        trader_role: discord.Role,
        trade_channel: discord.TextChannel
    ):

        created, updated_guild = update_settings(
            guild_id=interaction.guild.id,
            trader_role_id=trader_role.id,
            trader_channel_id=trade_channel.id
        )

        updated_role = interaction.guild.get_role(updated_guild.trader_role_id)
        updated_channel = interaction.guild.get_channel(updated_guild.trader_channel_id)

        if updated_role is None or updated_channel is None:
            return await interaction.response.send_message(
                "Controleer of de rol en het kanaal nog bestaan in deze server.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Volgende instellingen zijn {'aangemaakt' if created else 'gewijzigd'} in **{interaction.guild.name}**:\n\n"
                f"• **Rol:** {updated_role.mention}\n"
                f"• **Kanaal:** {updated_channel.mention}"
            ),
            color=discord.Color.green()
        )

        embed.set_footer(text=f"Angevraagd door {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(
            embed=embed,
        )

    @app_commands.command(
        name="add-clan",
        description="Voeg een clan toe aan de server waar gebruikers hun ruilen kunnen plaatsen"
    )
    @app_commands.describe(clan_tag="De tag van de clan die je wilt toevoegen")
    @app_commands.rename(clan_tag="clan")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def add_clan(
        self,
        interaction: discord.Interaction,
        clan_tag: str
    ):

        ## Validate the format

        if not re.match(CLAN_TAG_REGEX, clan_tag):
            return await interaction.response.send_message(
                f"`{clan_tag}` is geen geldige clan tag. Probeer het opnieuw!",
                ephemeral=True
            )

        ## Check if the server is set up

        guild = get_guild(interaction.guild.id)

        if guild is None:
            return await interaction.response.send_message(
                "De server is nog niet ingesteld. Gebruik eerst `/setup server` om de server in te stellen.",
                ephemeral=True
            )

        # Check if the clan exists in the Clash of Cards API

        encoded_clan_tag = clan_tag.upper().replace("#", "%23")
        clan_name = await get_clan(encoded_clan_tag)

        if clan_name is None:
            return await interaction.response.send_message(
                f"`{clan_tag}` is geen geldige clan tag. Probeer het opnieuw!",
                ephemeral=True
            )
    
        ## Check if the clan is already added to the server

        if clan_tag in guild.get_clans():
            return await interaction.response.send_message(
                f"{clan_name} is al toegevoegd aan deze server.",
                ephemeral=True
            )

        ## Add the clan to the server

        await interaction.response.send_message(
            f"{clan_name} is succesvol toegevoegd aan deze server.",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))

async def get_clan(clan_tag: str) -> str | None:
    url = f"https://api.clashk.ing/clan/{clan_tag}/basic"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None

            data = await response.json()

            return data["name"]