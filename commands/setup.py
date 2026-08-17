import re
import aiohttp
import discord

from discord.ext import commands
from discord import app_commands
from config import CLAN_TAG_REGEX
from data.database import create_guild, get_guild

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

        ## Update (or create) the settings in the database

        guild = get_guild(interaction.guild.id)

        if guild is None:
            guild = create_guild(interaction.guild.id, trader_role.id, trade_channel.id)
        else:
            guild.update_settings(trader_role.id, trade_channel.id)

        ## Check if the role and channel still exist in the server

        updated_role = interaction.guild.get_role(guild.trader_role_id)
        updated_channel = interaction.guild.get_channel(guild.trade_channel_id)

        if updated_role is None or updated_channel is None:

            embed = discord.Embed(
                title="Clash of Cards",
                description="De rol of het kanaal bestaat niet meer in deze server. Gebruik `/setup server` om de instellingen opnieuw in te stellen.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        ## Send a confirmation message to the user

        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Volgende instellingen zijn gewijzigd in **{interaction.guild.name}**:\n\n"
                f"• **Rol:** {updated_role.mention}\n"
                f"• **Kanaal:** {updated_channel.mention}"
            ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="add-clan",
        description="Voeg een clan toe aan de server waar gebruikers hun ruilen kunnen plaatsen"
    )
    @app_commands.describe(clan_tag="De tag van de clan die je wilt toevoegen")
    @app_commands.rename(clan_tag="tag")
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

            embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{clan_tag}** is geen geldige clan tag.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        ## Check if the server is set up

        guild = get_guild(interaction.guild.id)

        if guild is None:

            embed = discord.Embed(
                title="Clash of Cards",
                description="De server is nog niet ingesteld. Gebruik eerst `/setup server` om de server in te stellen.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Check if the clan exists in the Clash of Cards API

        encoded_clan_tag = clan_tag.upper().replace("#", "%23")
        clan_name = await get_clan(encoded_clan_tag)

        if clan_name is None:

            embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{clan_tag}** is geen geldige clan tag.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)
    
        ## Check if the clan is already added to the server

        if clan_tag in guild.get_clans():
            embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{clan_name}** ({clan_tag}) is al toegevoegd aan deze server.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=embed, ephemeral=True)

        ## Add the clan to the server

        clan = guild.add_clan(clan_tag=clan_tag, clan_name=clan_name)

        ## Send a confirmation message to the user

        embed = discord.Embed(
            title="Clash of Cards",
            description=f"**{clan.name}** ({clan.tag}) is succesvol toegevoegd aan deze server.",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="remove-clan",
        description="Voeg een clan toe aan de server waar gebruikers hun ruilen kunnen plaatsen"
    )
    @app_commands.describe(clan_tag="De tag van de clan die je wilt verwijderen")
    @app_commands.rename(clan_tag="tag")
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def remove_clan(
        self,
        interaction: discord.Interaction,
        clan_tag: str
    ):

        guild = get_guild(interaction.guild.id)

        if not guild.has_clan(clan_tag):
           await interaction.response.send_message(content="Deze clan is niet gelinkt aan deze server")

        else:
            guild.remove_clan(clan_tag)
            await interaction.response.send_message(content="Deze clan is verwijderd")

   

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))

async def get_clan(clan_tag: str) -> str | None:
    url = f"https://api.clashk.ing/clan/{clan_tag}/basic"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:

            if response.status != 200:
                return None

            data = await response.json()

            if not data or "name" not in data:
                return None

            return data["name"]