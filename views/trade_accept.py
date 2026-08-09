import discord

class TradeAcceptView(discord.ui.View):
    def __init__(
        self,
        clan: str | None,
        initiator: discord.Member,
        acceptor: discord.Member,
        thread: discord.Thread
    ):
        super().__init__(timeout=None)

        self.clan = clan
        self.initiator = initiator
        self.acceptor = acceptor
        self.thread = thread

        self.finish_button = discord.ui.Button(label="Afronden",style=discord.ButtonStyle.primary)
        self.finish_button.callback = self.finish_button_callback
        self.add_item(self.finish_button)

        self.cancel_button = discord.ui.Button(label="Annuleren", style=discord.ButtonStyle.secondary, emoji="🗑️")
        self.cancel_button.callback = self.cancel_button_callback
        self.add_item(self.cancel_button)

        if self.clan:
            self.add_item(
                discord.ui.Button(
                    label="Bekijk de ruil",
                    style=discord.ButtonStyle.link,
                    url=f"https://clashofclans.com/clans/{self.clan}"
                )
            )

    # Callbacks

    async def finish_button_callback(self, interaction: discord.Interaction):
        if interaction.user == self.initiator or interaction.user == self.acceptor:
            embed = discord.Embed(
                title="Clash of Cards",
                description=(
                    f"{interaction.user.mention} heeft de ruil tussen "
                    f"{self.initiator.mention} en {self.acceptor.mention} afgerond!\n"
                ),
                color=discord.Color.green()
            )   

            await interaction.response.edit_message(embed=embed, view=None)
            await self.thread.edit(archived=True, locked=True)

        else:
            await interaction.response.send_message(
                f"Alleen {self.initiator.display_name} of "
                f"{self.acceptor.display_name} kan deze afronden.",
                ephemeral=True
            )

    async def cancel_button_callback(self, interaction: discord.Interaction):
        if interaction.user == self.initiator or interaction.user == self.acceptor:
            embed = discord.Embed(
                title="Clash of Cards",
                description=(f"Deze ruil is geannuleerd door {interaction.user.mention}.\n" ),
                color=discord.Color.red()
            )

            await interaction.response.edit_message(embed=embed, view=None)
            await self.thread.edit(archived=True, locked=True)

        else:
            await interaction.response.send_message(
                f"Alleen {self.initiator.display_name} of "
                f"{self.acceptor.display_name} kan deze afsluiten.",
                ephemeral=True
            )