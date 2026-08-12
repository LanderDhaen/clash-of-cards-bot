import discord

from data.trade import Trade
from data.cards import Card
from data.clans import CLANS
from data.database import get_guild
from views.trade import TradeView

class TradeSetupView(discord.ui.View):

    def __init__(self, color: discord.Colour, cards: list[Card]):
        super().__init__(timeout=300)

        self.color = color

        card_options = [discord.SelectOption(label=card.name) for card in cards]
        clan_options = [discord.SelectOption(label=clan.name, value=clan.tag) for clan in CLANS]

        max_values = len(card_options)

        self.given_select = TradeSetupSelect(
            options=card_options,
            placeholder="Kies de kaarten die je wilt weggeven",
            max_values=max_values,
        )

        self.received_select = TradeSetupSelect(
            options=card_options,
            placeholder="Kies de kaarten die je wilt ontvangen",
            max_values=max_values,
        )

        self.clan_select = TradeSetupSelect(
            options=clan_options,
            placeholder="Kies de clan waar je de kaarten wilt ruilen",
            required=False,
        )

        self.add_item(self.given_select)
        self.add_item(self.received_select)
        self.add_item(self.clan_select)

        self.add_item(ConfirmButton())
        self.add_item(CancelButton())

class TradeSetupSelect(discord.ui.Select):

    def __init__(self, options: list[discord.SelectOption], placeholder: str, min_values: int = 1, max_values: int = 1, required: bool = True):

        super().__init__(
            placeholder=placeholder,
            options=options,
            min_values=min_values,
            max_values=max_values,
            required=required
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class ConfirmButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Bevestigen",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeSetupView)

        ## Building the trade object

        initiator = interaction.user
        given = self.view.given_select.values
        received = self.view.received_select.values
        clan_tag = self.view.clan_select.values[0] if self.view.clan_select.values else None
        clan = next((clan for clan in CLANS if clan.tag == clan_tag), None)

        trade = Trade(
            initiator=initiator,
            color=self.view.color,
            given=given,
            received=received,
            clan=clan
        )

        ## Validating the trade object

        validation_error = trade.validate()

        if validation_error:
            return await interaction.response.send_message(validation_error, ephemeral=True)

        ## Retrieving the guild's trader role and channel

        guild = get_guild(interaction.guild.id)

        trader_role = interaction.guild.get_role(guild.trader_role_id)
        trader_channel = interaction.guild.get_channel(guild.trader_channel_id)

        ## Build the trade message

        trade_message_content = trader_role.mention if trader_role else None

        trade_message_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{initiator.mention} wilt kaarten ruilen in **{clan.name}**:\n"
                if clan
                else f"{initiator.mention} wilt kaarten ruilen:\n"
            ),
            color=trade.color
        )

        trade_message_embed.add_field(
            name="Weggeven",
            value="\n".join(f"• {card}" for card in trade.given),
            inline=True
        )

        trade_message_embed.add_field(
            name="Ontvangen",
            value="\n".join(f"• {card}" for card in trade.received),
            inline=True
        )

        trade_message_view = TradeView(trade)

        ## Send the trade message to the trader channel

        if not isinstance(trader_channel, discord.TextChannel):
            trader_channel = interaction.channel

        trade_message = await trader_channel.send(content=trade_message_content, embed=trade_message_embed, view=trade_message_view)
        await interaction.response.edit_message(content=f"Je ruilvoorstel is verzonden naar {trade_message.jump_url}.", embed=None, view=None)

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None)




