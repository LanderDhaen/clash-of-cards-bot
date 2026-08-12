import discord

from config import AUTO_DELETE_SECONDS
from data.clans import Clan
from views.trade_accept import TradeAcceptView

class AcceptButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Accepteren", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if not isinstance(view, TradeView):
            return await interaction.response.send_message("Er is iets misgegaan. Probeer het opnieuw.", ephemeral=True)

        if interaction.user == view.initiator:
            return await interaction.response.send_message(
                f"Je kan je eigen ruilvoorstel niet accepteren.",
                ephemeral=True
            )

        trade_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"{interaction.user.mention} heeft het voorstel van "
                f"{view.initiator.mention} geaccepteerd!\n"
            ),
            color=discord.Color.green()
        )

        trade_embed.add_field(
            name="Weggeven",
            value="\n".join(f"• {card}" for card in view.give),
            inline=True
        )

        trade_embed.add_field(
            name="Ontvangen",
            value="\n".join(f"• {card}" for card in view.receive),
            inline=True
        )

        await interaction.response.edit_message(
            embed=trade_embed,
            view=None
        )

        thread = await interaction.message.create_thread(
            name=f"{view.initiator.display_name} & {interaction.user.display_name}"
        )

        thread_embed = discord.Embed(
            title="Clash of Cards",
            description=(
                f"Deze thread is aangemaakt om de ruil tussen {view.initiator.mention} en {interaction.user.mention} verder te bespreken.\n "
            ),
            color=discord.Color.light_grey()
        )

        thread_embed.add_field(
            name="Afronden",
            value="Wanneer de kaarten uitgewisseld zijn, kan de ruil worden afgerond.",
            inline=False
        )

        thread_embed.add_field(
            name="Annuleren",
            value="Als een van de partijen niet langer geïnteresseerd is in de ruil, kan deze worden geannuleerd.",
            inline=False
        )

        if view.clan:
            thread_embed.add_field(
                name="Bekijk de ruil",
                value="Link naar de clan waar de ruil zal plaatsvinden.",
                inline=False
            )

        await thread.send(
            content=(
                f"{view.initiator.mention} & {interaction.user.mention}"
            ),
            embed=thread_embed,
            view=TradeAcceptView(
                clan=view.clan,
                initiator=view.initiator,
                acceptor=interaction.user,
                thread=thread
            )
        )

class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Annuleren", style=discord.ButtonStyle.secondary, emoji="🗑️")

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if not isinstance(view, TradeView):
            return await interaction.response.send_message("Er is iets misgegaan. Probeer het opnieuw.", ephemeral=True)

        if interaction.user != view.initiator:
            return await interaction.response.send_message(
                f"Alleen {view.initiator.mention} kan deze ruil annuleren.",
                ephemeral=True
            )

        embed = discord.Embed(
            title="Clash of Cards",
            description=f"Deze ruil is geannuleerd door {interaction.user.mention}.",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(embed=embed, view=None, delete_after=AUTO_DELETE_SECONDS)

class TradeView(discord.ui.View):
    def __init__(self, clan: Clan | None, give: list[str], receive: list[str], initiator: discord.Member):
        super().__init__(timeout=None)

        self.clan = clan
        self.give = give
        self.receive = receive
        self.initiator = initiator

       
        self.add_item(AcceptButton())
        self.add_item(CancelButton())