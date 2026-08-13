import discord

from data.trade import Trade

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
                style=discord.ButtonStyle.link
                )
            )


class FinishButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Afronden",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeAcceptView)

        trade = self.view.trade

        if not trade.is_participant(interaction.user):
            return await interaction.response.send_message(f"Alleen {trade.initiator.mention} of {trade.acceptor.mention} kan deze ruil afronden.", ephemeral=True)

        ## Update the trade message embed & delete the thread

        thread = interaction.channel
        trade_message = await thread.parent.fetch_message(interaction.channel.id)
        trade_message_embed = trade_message.embeds[0]

        trade_message_embed.color = discord.Color.green()
        trade_message_embed.set_footer(text=f"Ruil afgerond door {interaction.user.display_name}!", icon_url=interaction.user.display_avatar.url)

        await trade_message.edit(embed=trade_message_embed, view=None, delete_after=60)
        await thread.delete()

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )

    async def callback(self, interaction: discord.Interaction):

        from views.trade import TradeView

        assert isinstance(self.view, TradeAcceptView)

        trade = self.view.trade

        if not trade.is_participant(interaction.user):
            return await interaction.response.send_message(f"Alleen {trade.initiator.mention} of {trade.acceptor.mention} kan deze ruil annuleren.", ephemeral=True)

        ## Update the trade object

        trade.acceptor = None

        ## Update the trade message embed & delete the thread

        thread = interaction.channel
        trade_message = await thread.parent.fetch_message(interaction.channel.id)
        trade_message_embed = trade_message.embeds[0]

        trade_message_embed.description = (
                    f"{trade.initiator.mention} wilt kaarten ruilen in **{trade.clan.name}**:\n"
                    if trade.clan
                    else f"{trade.initiator.mention} wilt kaarten ruilen:\n")
        trade_message_embed.color = trade.color

        trade_message_embed.set_footer(text=None, icon_url=None)

        trade_message_view = TradeView(trade)

        await trade_message.edit(embed=trade_message_embed, view=trade_message_view)
        await thread.delete()
