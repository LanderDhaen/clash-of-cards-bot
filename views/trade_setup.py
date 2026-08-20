import discord

from data.database import TRADE_TYPES, Trade, TradeType, Guild, validate_given_and_received
from views.trade import TradeView

class TradeSetupView(discord.ui.View):

    def __init__(self, trade_type: TradeType, guild: Guild):
        super().__init__(timeout=300)

        self.trade_type = trade_type
        self.guild = guild

        ## Card Selects

        name, self.color, cards = TRADE_TYPES[trade_type]
        max_values = len(cards)

        self.card_options = [
            discord.SelectOption(
                label=card,
                value=card,
            )
            for card in cards
        ]

        
        self.given_select = TradeSetupSelect(
            options=self.card_options,
            placeholder="Kies de kaarten die je wilt weggeven",
            min_values=1,
            max_values=max_values,
            required=True
        )

        self.received_select = TradeSetupSelect(
            options=self.card_options,
            placeholder="Kies de kaarten die je wilt ontvangen",
            min_values=1,
            max_values=max_values,
            required=True
        )

        self.add_item(self.given_select)
        self.add_item(self.received_select)

        ## Clan Select (if the guild has clans)

        self.clan_options = []
        self.clan_select = None

        guild_clans = self.guild.get_clans()

        if guild_clans:
            self.clan_options = [
                discord.SelectOption(
                    label=clan.name,
                    value=clan.tag,
                )
                for clan in guild_clans
            ]

            self.clan_select = TradeSetupSelect(
                options=self.clan_options,
                placeholder="Kies de clan waar je de kaarten wilt ruilen",
                min_values=0,
                max_values=1,
                required=False
            )

            self.add_item(self.clan_select)

        ## Buttons

        self.add_item(ConfirmButton())
        self.add_item(CancelButton())

class TradeSetupSelect(discord.ui.Select):

    def __init__(self, options: list[discord.SelectOption], placeholder: str, min_values: int, max_values: int, required: bool):

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
            style=discord.ButtonStyle.primary,
            custom_id="confirm_trade_setup"
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeSetupView), "This button can only be used within a TradeSetupView."

        ## Get the trade parameters

        guild = self.view.guild

        initiator = interaction.user
        given = self.view.given_select.values 
        received = self.view.received_select.values

        clan_tag = self.view.clan_select.values[0] if self.view.clan_select and self.view.clan_select.values else None
        clan = guild.get_clan(clan_tag) if clan_tag else None

        ## Validating the raw data

        validation_error = validate_given_and_received(given, received)

        if validation_error:

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=validation_error,
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Build the trade object

        trade = Trade(
            type = self.view.trade_type.value,
            given = given,
            received = received,
            message_id = None,
            thread_id = None,
            initiator_id = initiator.id,
            acceptor_id = None,
            guild = guild,
            clan = clan
        )

        ## Build the trade message

        trader_role = interaction.guild.get_role(guild.trader_role_id)
        trade_channel = interaction.guild.get_channel(guild.trade_channel_id)

        trade_message_content = trader_role.mention if trader_role else None

        trade_message_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{initiator.mention} wilt kaarten ruilen in **{trade.clan.name}**:\n"
                if trade.clan
                else f"{initiator.mention} wilt kaarten ruilen:\n"
            ),
            color=self.view.color
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

        ## Send the trade message to the trade channel

        if not trade_channel and not isinstance(trade_channel, discord.TextChannel):
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is niet correct ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        trade_message_view = TradeView(trade)

        trade_message = await trade_channel.send(
            content=trade_message_content,
            embed=trade_message_embed,
            view=trade_message_view
        )

        ## Build the confirmation message

        confirmation_message_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Jouw nieuw voorstel is zonet verzonden naar {trade_message.jump_url}.\n\n"
            ),
            color=discord.Color.green()
        )

        possible_trades = trade.matching_trades()

        if possible_trades:

            confirmation_message_embed.description += "Jij kan één van de volgende voorstellen accepteren door op de link te klikken:\n\n"
            
            for possible_trade in possible_trades:

                initiator = interaction.guild.get_member(possible_trade.initiator_id)
                confirmation_message_embed.description += (
                    f"• [Bekijk de ruil](https://discord.com/channels/{possible_trade.guild.guild_id}/{trade_channel.id}/{possible_trade.message_id}) van {initiator.mention}\n"
                )

        await interaction.response.edit_message(embed=confirmation_message_embed, view=None)

        ## Save the trade to the database

        trade.message_id = trade_message.id
        trade.save()

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id="cancel_trade_setup"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None)
        

        
            


