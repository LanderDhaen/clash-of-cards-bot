import discord

from views.trade_accept import TradeAcceptView

class TradeView(discord.ui.View):
    def __init__(self, clan: str | None, give: list[str], receive: list[str], initiator: discord.Member):
        super().__init__(timeout=None)

        self.clan = clan
        self.give = give
        self.receive = receive
        self.initiator = initiator

        self.accept_button = discord.ui.Button(label="Accepteren", style=discord.ButtonStyle.primary)
        self.accept_button.callback = self.accept_button_callback
        self.add_item(self.accept_button)

        self.close_button = discord.ui.Button(label="Afsluiten", style=discord.ButtonStyle.secondary, emoji="🗑️")
        self.close_button.callback = self.close_button_callback
        self.add_item(self.close_button)

    # Callbacks

    async def accept_button_callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{interaction.user.mention} heeft het voorstel van "
                f"{self.initiator.mention} geaccepteerd!\n"
            ),
            color=discord.Color.green()
        )

        embed.add_field(
            name="Weggeven",
            value="\n".join(f"• {card}" for card in self.give),
            inline=True
        )

        embed.add_field(
            name="Ontvangen",
            value="\n".join(f"• {card}" for card in self.receive),
            inline=True
        )

        await interaction.response.edit_message(
            embed=embed,
            view=None
        )

        thread = await interaction.message.create_thread(
            name=f"{self.initiator.display_name} & {interaction.user.display_name}"
        )

        message_view = TradeAcceptView(
            clan=self.clan,
            initiator=self.initiator,
            acceptor=interaction.user
        )

        await thread.send(
            content=(
                f"{self.initiator.mention} en {interaction.user.mention}"
            ),
            view=message_view
        )


    async def close_button_callback(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Dit voorstel van {interaction.user.mention} is niet langer beschikbaar:\n"
                ),
            color=discord.Color.red()
        )

        embed.add_field(name="Weggeven", value="\n".join(f"• {card}" for card in self.give), inline=True)
        embed.add_field(name="Ontvangen", value="\n".join(f"• {card}" for card in self.receive), inline=True)

        await interaction.response.edit_message(embed=embed, view=None, delete_after=60)