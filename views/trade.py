import discord

class TradeView(discord.ui.View):
    def __init__(self, clan_tag: str, give: list, receive: list):
        super().__init__(timeout=None)

        self.give = give
        self.receive = receive

        self.visit_clan_button = discord.ui.Button(label="Bekijk de ruil", style=discord.ButtonStyle.link, url=f"https://link.clashofclans.com/en?action=OpenClanProfile&tag={clan_tag}")
        self.add_item(self.visit_clan_button) if clan_tag else None

        self.close_button = discord.ui.Button(label="Afsluiten", style=discord.ButtonStyle.secondary, emoji="🗑️")
        self.close_button.callback = self.close_button_callback
        self.add_item(self.close_button)

    # Callbacks

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