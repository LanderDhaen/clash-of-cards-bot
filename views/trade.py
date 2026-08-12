import discord

from data.trade import Trade
from views.trade_accept import TradeAcceptView

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

        ## Update the trade object

        if not trade.can_accept(interaction.user):
            return await interaction.response.send_message("Je kunt je eigen ruilvoorstel niet accepteren.", ephemeral=True)

        trade.acceptor = interaction.user
        
        ## Update the trade message embed

        trade_message_embed = interaction.message.embeds[0]
        trade_message_embed.color = trade.color
        trade_message_embed.set_footer(text=f"Ruilvoorstel geaccepteerd door {trade.acceptor.mention}.", icon_url=trade.acceptor.display_avatar.url)

        await interaction.response.edit_message(embed=trade_message_embed, view=None)

        ## Build the thread message

        thread = await interaction.message.create_thread(
            name=f"{trade.initiator.display_name} & {trade.acceptor.display_name}"
        )

        thread_message_content = f"{trade.initiator.mention} & {trade.acceptor.mention}"

        thread_message_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Deze thread is aangemaakt om de ruil tussen {trade.initiator.mention} en {trade.acceptor.mention} verder te bespreken.\n "
            ),
            color=trade.color
        )

        thread_message_embed.add_field(
            name="Afronden",
            value="Wanneer de kaarten uitgewisseld zijn, kan de ruil worden afgerond.",
            inline=False
        )

        thread_message_embed.add_field(
            name="Annuleren",
            value="Als een van de partijen niet langer geïnteresseerd is in de ruil, kan deze worden geannuleerd.",
            inline=False
        )

        if trade.clan:
            thread_message_embed.add_field(
                name="Bekijk de ruil",
                value="Link naar de clan waar de ruil zal plaatsvinden.",
                inline=False
            )

        thread_message_view = TradeAcceptView(trade)

        ## Send the thread message to the thread

        await thread.send(content=thread_message_content, embed=thread_message_embed, view=thread_message_view)

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



      


        


