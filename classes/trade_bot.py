from discord.ext import commands

from commands.trade import trade
from config import GUILD, IS_DEVELOPMENT

class TradeBot(commands.Bot):
    async def setup_hook(self):
        if IS_DEVELOPMENT and GUILD is not None:
            self.tree.add_command(trade, guild=GUILD)
            self.tree.clear_commands(guild=None)

            await self.tree.sync(guild = GUILD)
        else:
            self.tree.add_command(trade)
            await self.tree.sync()
           