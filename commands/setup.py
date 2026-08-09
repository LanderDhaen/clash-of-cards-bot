import discord

from discord.ext import commands
from discord import app_commands
from data.database import db, Guild

class Setup(commands.GroupCog, group_name="setup", group_description="Stel Clash of Cards Trader in"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="server",
        description="Stel de rol in die vermeld wordt wanneer een gebruiker een ruil plaatst"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def setup_server(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        channel: discord.TextChannel
    ):
        with db:
            guild, created = Guild.get_or_create(
                guild_id=interaction.guild.id
            )

            guild.trader_role_id = role.id
            guild.trader_channel_id = channel.id
            guild.save()

        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                           f"{interaction.user.mention} heeft de volgende instellingen gewijzigd in **{interaction.guild.name}**:\n\n"
                           f"• **Rol:** {role.mention}\n"
                           f"• **Kanaal:** {channel.mention}\n"
                       ),
            color=discord.Color.green()
        )

        await interaction.response.send_message(
            embed=embed,
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))