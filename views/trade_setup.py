import discord

from data.clans import CLANS
from views.trade import TradeView
from data.database import Guild

class TradeSetupView(discord.ui.View):

    def __init__(self, color, cards):
        super().__init__(timeout=300)
        self.give = []
        self.receive = []
        self.clan_tag = None

        self.color = color
        self.cards = cards

        max_values = len(cards)

        # Selects

        self.give_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt weggeven",
            options=[discord.SelectOption(label=card.name) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.give_select.callback = self.give_select_callback
        self.add_item(self.give_select)

        self.receive_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt ontvangen",
            options=[discord.SelectOption(label=card.name, value=card.name) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.receive_select.callback = self.receive_select_callback
        self.add_item(self.receive_select)

        self.clan_select = discord.ui.Select(
            placeholder="Kies de clan waar je de kaarten wilt ruilen",
            options=[discord.SelectOption(label=clan.name, value=clan.tag) for clan in CLANS],
            min_values=1,
            max_values=1
        )

        self.clan_select.callback = self.clan_select_callback
        self.add_item(self.clan_select)

        # Buttons

        self.accept_button = discord.ui.Button(
            label="Bevestigen",
            style=discord.ButtonStyle.primary
        )

        self.accept_button.callback = self.accept_button_callback
        self.add_item(self.accept_button)

        self.cancel_button = discord.ui.Button(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )

        self.cancel_button.callback = self.cancel_button_callback
        self.add_item(self.cancel_button)

    # Callbacks

    async def give_select_callback(self, interaction: discord.Interaction):
        self.give = self.give_select.values
        await interaction.response.defer()

    async def receive_select_callback(self, interaction: discord.Interaction):
        self.receive = self.receive_select.values
        await interaction.response.defer()

    async def clan_select_callback(self, interaction: discord.Interaction):
        self.clan_tag = self.clan_select.values[0]
        await interaction.response.defer()


    async def accept_button_callback(self, interaction: discord.Interaction):

        if not self.give:
            await interaction.response.send_message(
                "Je moet minstens één kaart kiezen die je wilt weggeven.",
                ephemeral=True
            )

        elif not self.receive:
            await interaction.response.send_message(
                "Je moet minstens één kaart kiezen die je wilt ontvangen.",
                ephemeral=True
            )

        else:
            await interaction.response.edit_message(
                content="Je ruilvoorstel is verzonden!",
                embed=None,
                view=None,
                delete_after=60
            )

            clan = next(
                (clan for clan in CLANS if clan.tag == self.clan_tag),
                None
            )

            role = interaction.guild.get_role(Guild.get_trader_role_id(interaction.guild.id))

            embed_description = (
                f"{interaction.user.mention} wilt kaarten ruilen in **{clan.name}**:\n"
                if clan
                else f"{interaction.user.mention} wilt kaarten ruilen:\n"
            )

            embed = discord.Embed(
                title="Clash of Cards",
                description=embed_description,
                color=self.color
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

            await interaction.channel.send(
                content=f"{role.mention if role else None}",
                embed=embed,
                view=TradeView(
                    self.clan_tag,
                    self.give,
                    self.receive,
                    initiator=interaction.user
                )
            )


    async def cancel_button_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None, delete_after=60)