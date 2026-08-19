import discord

from data.database import TRADE_TYPES, Trade, TradeType
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
            style=discord.ButtonStyle.primary,
            custom_id="accept_trade"
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeView), "This button can only be used within a TradeView."

        ## Get the trade parameters

        trade = self.view.trade
        color, cards = TRADE_TYPES[TradeType(trade.type)]

        acceptor = interaction.user

        ## Validate the interaction

        if not trade.can_accept(acceptor.id):

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Je kunt je eigen ruilvoorstel niet accepteren.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Update the trade message embed

        trade_message_embed = interaction.message.embeds[0]
        trade_message_embed.color = discord.Color.green()
        trade_message_embed.set_footer(text=f"Ruilvoorstel geaccepteerd door {acceptor.display_name}!", icon_url=acceptor.display_avatar.url)

        await interaction.message.edit(embed=trade_message_embed, view=None)

        ## Build the trade thread

        trade_initiator = interaction.guild.get_member(trade.initiator_id)

        if not trade_initiator or not acceptor:
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=f"**Er is een fout opgetreden bij het ophalen van de gebruikersgegevens.**",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        trade_thread_name = f"{trade_initiator.display_name} & {acceptor.display_name}"

        ## Create the thread

        thread = await interaction.message.create_thread(name=trade_thread_name)

        ## Build the trade thread message

        thread_message_content = f"{trade_initiator.mention} & {acceptor.mention}"

        thread_message_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Deze thread is aangemaakt om de ruil tussen {trade_initiator.mention} en {acceptor.mention} verder te bespreken.\n "
            ),
            color=color
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

        ## Send the trade thread message to the thread

        thread_message = await thread.send(
            content=thread_message_content,
            embed=thread_message_embed,
            view=thread_message_view
        )

        ## Save the trade to the database

        trade.acceptor_id = acceptor.id
        trade.thread_id = thread_message.id
        trade.save()

class CancelButton(discord.ui.Button):

    def __init__(self):

        super().__init__(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️",
            custom_id="cancel_trade"
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeView), "This button can only be used within a TradeView."

        trade = self.view.trade

        ## Validating the interaction

        if not trade.can_cancel(interaction.user.id):

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Je kunt alleen je eigen ruilvoorstel annuleren.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Update the trade message embed

        trade_message_embed = interaction.message.embeds[0]
        trade_message_embed.color = discord.Color.green()
        trade_message_embed.set_footer(text=f"Ruilvoorstel geannuleerd door {interaction.user.display_name}!", icon_url=interaction.user.display_avatar.url)

        await interaction.response.edit_message(embed=trade_message_embed, view=None, delete_after=30)

        ## Delete the trade from the database

        trade.delete_instance()



        


    