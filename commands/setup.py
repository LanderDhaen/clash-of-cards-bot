import discord

from discord.ext import commands
from discord import app_commands
from data.database import Guild, update_settings

class Setup(commands.GroupCog, group_name="setup", group_description="Stel Clash of Cards Trader in"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="server",
        description="Stel de rol in die vermeld wordt wanneer een gebruiker een ruil plaatst"
    )
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
                f"Volgende instellingen {'aangemaakt' if created else 'gewijzigd'} in **{interaction.guild.name}**:\n\n"
                f"• **Rol:** {updated_role.mention}\n"
                f"• **Kanaal:** {updated_channel.mention}"
            ),
            color=discord.Color.green()
        )

        embed.set_footer(text=f"{"Aangemaakt" if created else "Gewijzigd"} door {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(
            embed=embed,
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))