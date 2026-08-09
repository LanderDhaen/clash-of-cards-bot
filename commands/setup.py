import discord

from discord.ext import commands
from discord import app_commands

class Setup(commands.GroupCog, group_name="setup", group_description="Stel Clash of Cards Trader in"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="trader-role",
        description="Stel de rol in die vermeld wordt wanneer een gebruiker een ruil plaatst"
    )
    @app_commands.default_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.guild_only()
    async def trader_role(self, interaction: discord.Interaction, role: discord.Role):

        await interaction.response.send_message(
            f"{role.mention} is ingesteld als de trader-rol voor deze Discord-server.",
            ephemeral=True
        )

        

async def setup(bot: commands.Bot):
    await bot.add_cog(Setup(bot))