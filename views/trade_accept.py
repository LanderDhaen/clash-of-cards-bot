import discord

from data.database import TRADE_TYPES, Trade, TradeType

class TradeAcceptView(discord.ui.View):

    def __init__(self, trade: Trade):
        super().__init__(timeout=None)

        self.trade = trade

        self.add_item(FinishButton())
        self.add_item(CancelButton())

        if trade.clan:
            self.add_item(discord.ui.Button(
                label="Bekijk de ruil", 
                url=f"https://link.clashofclans.com/en?action=OpenClanProfile&tag={trade.clan.tag}", 
                style=discord.ButtonStyle.link,
                custom_id="view_clan",
                )
            )


class FinishButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Afronden",
            style=discord.ButtonStyle.primary,
            custom_id="finish_trade_accept"
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeAcceptView), "This button can only be used within a TradeAcceptView."

        ## Get the trade parameters

        trade = self.view.trade
        finisher = interaction.user

        ## Validate the interaction

        if not trade.is_participant(finisher.id):

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Je kunt een ruilvoorstel waar je niet aan deelneemt niet afronden.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Update the trade message embed

        trade_channel = interaction.guild.get_channel(trade.guild.trade_channel_id)

        if not isinstance(trade_channel, discord.TextChannel):
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is niet correct ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        trade_message = await trade_channel.fetch_message(trade.message_id)
    
        trade_message_embed = trade_message.embeds[0]
        trade_message_embed.color = discord.Color.green()
        trade_message_embed.set_footer(text=f"Ruilvoorstel afgerond door {finisher.display_name}!", icon_url=finisher.display_avatar.url)

        await trade_message.edit(embed=trade_message_embed, view=None, delete_after=60)
        await trade_message.thread.delete()

        ## Delete the trade

        trade.delete_instance()

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id="cancel_trade_accept"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.trade import TradeView

        assert isinstance(self.view, TradeAcceptView), "This button can only be used within a TradeAcceptView."

        ## Get the trade parameters

        trade = self.view.trade
        color, cards = TRADE_TYPES[TradeType(trade.type)]

        canceler = interaction.user

        ## Validate the interaction

        if not trade.is_participant(canceler.id):

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Je kunt een ruilvoorstel waar je niet aan deelneemt niet annuleren.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Update the trade message embed

        trade_channel = interaction.guild.get_channel(trade.guild.trade_channel_id)

        if not isinstance(trade_channel, discord.TextChannel):
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is niet correct ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        trade_message = await trade_channel.fetch_message(trade.message_id)

        trade_message_embed = trade_message.embeds[0]
        trade_message_embed.color = color
        trade_message_embed.set_footer(text=None, icon_url=None)

        trade_message_view = TradeView(trade)

        await trade_message.edit(embed=trade_message_embed, view=trade_message_view)
        await trade_message.thread.delete()

        ## Save the trade to the database

        trade.acceptor_id = None
        trade.thread_id = None
        trade.save()

