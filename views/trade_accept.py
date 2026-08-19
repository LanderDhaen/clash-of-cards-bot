import discord

from data.database import Trade

class TradeAcceptView(discord.ui.View):

    def __init__(self, trade: Trade):
        super().__init__(timeout=None)

        self.trade = trade

        self.add_item(FinishButton())


class FinishButton(discord.ui.Button):

    def __init__(self):
        super().__init__(
            label="Afronden",
            style=discord.ButtonStyle.primary
        )

    async def callback(self, interaction: discord.Interaction):

        assert isinstance(self.view, TradeAcceptView), "This button can only be used within a TradeAcceptView."

        ## Get the trade parameters

        trade = self.view.trade
        finisher = interaction.user

        if not trade.is_participant(finisher.id):

            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Je kunt een ruilvoorstel waar je niet aan deelneemt niet afronden.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        ## Update the trade message embed

        trade_channel = interaction.guild.get_channel(trade.guild.trade_channel_id)

        if not trade_channel and not isinstance(trade_channel, discord.TextChannel):
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description=f"**{interaction.guild.name}** is niet correct ingesteld. Contacteer een beheerder.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)

        trade_message = await trade_channel.fetch_message(trade.message_id)

        if not trade_message:
            trade_error_embed = discord.Embed(
                title="Clash of Cards",
                description="Het ruilvoorstel kon niet worden gevonden.",
                color=discord.Color.red()
            )

            return await interaction.response.send_message(embed=trade_error_embed, ephemeral=True)
    
        trade_message_embed = trade_message.embeds[0]
        trade_message_embed.color = discord.Color.green()
        trade_message_embed.set_footer(text=f"Ruilvoorstel afgerond door {finisher.display_name}!", icon_url=finisher.display_avatar.url)

        await trade_message.edit(embed=trade_message_embed, view=None, delete_after=60)
        await trade_message.thread.delete()

        ## Delete the trade

        trade.delete_instance()



