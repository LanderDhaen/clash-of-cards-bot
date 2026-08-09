import discord

class TradeAcceptView(discord.ui.View):
    def __init__(
        self,
        clan: str | None,
        initiator: discord.Member,
        acceptor: discord.Member
    ):
        super().__init__(timeout=None)

        self.clan = clan
        self.initiator = initiator
        self.acceptor = acceptor

        self.finish_button = discord.ui.Button(label="Afronden",style=discord.ButtonStyle.primary)
        self.finish_button.callback = self.finish_button_callback
        self.add_item(self.finish_button)

        if self.clan:
            self.add_item(
                discord.ui.Button(
                    label="Bekijk de ruil",
                    style=discord.ButtonStyle.link,
                    url=f"https://clashofclans.com/clans/{self.clan}"
                )
            )

    async def finish_button_callback(self, interaction: discord.Interaction):
        pass