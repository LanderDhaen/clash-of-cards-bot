import discord

class TradeSetupView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)