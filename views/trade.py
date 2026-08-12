import discord

from data.trade import Trade

class TradeView(discord.ui.View):

    def __init__(self, trade: Trade):

        super().__init__(timeout=None)

        self.trade = trade

        self.add_item(AcceptButton())
        self.add_item(CancelButton())

class AcceptButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Accepteren",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeView)

        trade = self.view.trade
        trade.acceptor = interaction.user

        if not trade.can_accept():
            return await interaction.response.send_message("Je kunt je eigen ruilvoorstel niet accepteren.", ephemeral=True)

        trade_message_embed = interaction.message.embeds[0]
        trade_message_embed.color = trade.color
        trade_message_embed.set_footer(text=f"Ruilvoorstel geaccepteerd door {trade.acceptor.mention}.", icon_url=trade.acceptor.display_avatar.url)

        await interaction.response.edit_message(embed=trade_message_embed, view=None)

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeView)

        trade_message_embed = interaction.message.embeds[0]
        trade_message_embed.color = discord.Color.red()
        trade_message_embed.set_footer(text=f"Ruilvoorstel geannuleerd door {interaction.user.mention}.", icon_url=interaction.user.display_avatar.url)

        await interaction.response.edit_message(embed=trade_message_embed, view=None, delete_after=60)



      


        


