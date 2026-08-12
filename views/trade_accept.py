import discord

from config import AUTO_DELETE_SECONDS
from data.clans import Clan

class FinishButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Afronden", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view = self.view

        assert isinstance(view, TradeAcceptView)

        ## Validation

        if interaction.user != view.initiator and interaction.user != view.acceptor:
            return await interaction.response.send_message(
                f"Alleen {view.initiator.mention} of {view.acceptor.mention} kan deze ruil afronden.",
                ephemeral=True
            )

        ## Send a success message to the thread

        embed = discord.Embed(
            title="Clash of Cards",
            description=(f"{interaction.user.mention} heeft de ruil tussen {view.initiator.mention} en {view.acceptor.mention} afgerond!\n"),
            color=discord.Color.green()
        )

        embed.set_footer(text="Deze thread wordt nu gesloten en gearchiveerd.")

        ## Close the thread and remove the buttons from the original embed

        await interaction.response.edit_message(view=None)
        await view.thread.send(embed=embed)
        await view.thread.edit(archived=True, locked=True)

        ## Edit the trade post to show that the trade has been completed and schedule the post & thread for deletion

        starter_message = await view.thread.parent.fetch_message(view.thread.id)
        starter_embed = starter_message.embeds[0]
   
        await starter_message.edit(embed=starter_embed, view=None, delete_after=AUTO_DELETE_SECONDS)
        await starter_message.thread.delete()

class CancelButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Annuleren", style=discord.ButtonStyle.secondary, emoji="🗑️")

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if not isinstance(view, TradeAcceptView):
            return await interaction.response.send_message("Er is iets misgegaan. Probeer het opnieuw.", ephemeral=True)

        if interaction.user != view.initiator and interaction.user != view.acceptor:
            return await interaction.response.send_message(
                f"Alleen {view.initiator.mention} of {view.acceptor.mention} kan deze ruil annuleren.",
                ephemeral=True
            )

        thread_embed = discord.Embed(
            title="Clash of Cards",
            description=f"Deze ruil is geannuleerd door {interaction.user.mention}.",
            color=discord.Color.red()
        )

        await interaction.response.edit_message(embed=thread_embed, view=None, delete_after=60)
        await view.thread.edit(archived=True, locked=True)

class VisitClanButton(discord.ui.Button):
    def __init__(self, clan: Clan):
        super().__init__(
            label="Bekijk de ruil",
            style=discord.ButtonStyle.link,
            url=f"https://clashofclans.com/clans/{clan.tag}"
        )

class TradeAcceptView(discord.ui.View):
    def __init__(
        self,
        clan: Clan | None,
        initiator: discord.Member,
        acceptor: discord.Member,
        thread: discord.Thread
    ):
        super().__init__(timeout=None)

        self.clan = clan
        self.initiator = initiator
        self.acceptor = acceptor
        self.thread = thread

        

        self.add_item(FinishButton())    
        self.add_item(CancelButton())

        if self.clan:
            self.add_item(VisitClanButton(self.clan))