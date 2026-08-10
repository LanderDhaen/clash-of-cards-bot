import discord

from data.clans import CLANS, Clan
from views.trade import TradeView
from data.database import Guild

class TradeSetupView(discord.ui.View):

    def __init__(self, color, cards):
        super().__init__(timeout=300)
        self.give = []
        self.receive = []
        self.clan_tag = None

        self.color = color
        self.cards = cards

        max_values = len(cards)

        # Selects

        self.give_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt weggeven",
            options=[discord.SelectOption(label=card.name) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.give_select.callback = self.give_select_callback
        self.add_item(self.give_select)

        self.receive_select = discord.ui.Select(
            placeholder="Kies de kaarten die je wilt ontvangen",
            options=[discord.SelectOption(label=card.name, value=card.name) for card in cards],
            min_values=1,
            max_values=max_values
        )

        self.receive_select.callback = self.receive_select_callback
        self.add_item(self.receive_select)

        self.clan_select = discord.ui.Select(
            placeholder="Kies de clan waar je de kaarten wilt ruilen",
            options=[discord.SelectOption(label=clan.name, value=clan.tag) for clan in CLANS],
            min_values=1,
            max_values=1
        )

        self.clan_select.callback = self.clan_select_callback
        self.add_item(self.clan_select)

        # Buttons

        self.accept_button = discord.ui.Button(
            label="Bevestigen",
            style=discord.ButtonStyle.primary
        )

        self.accept_button.callback = self.accept_button_callback
        self.add_item(self.accept_button)

        self.cancel_button = discord.ui.Button(
            label="Annuleren",
            style=discord.ButtonStyle.secondary,
            emoji="🗑️"
        )

        self.cancel_button.callback = self.cancel_button_callback
        self.add_item(self.cancel_button)

    # Callbacks

    async def give_select_callback(self, interaction: discord.Interaction):
        self.give = self.give_select.values
        await interaction.response.defer()

    async def receive_select_callback(self, interaction: discord.Interaction):
        self.receive = self.receive_select.values
        await interaction.response.defer()

    async def clan_select_callback(self, interaction: discord.Interaction):
        self.clan_tag = self.clan_select.values[0]
        await interaction.response.defer()


    async def accept_button_callback(self, interaction: discord.Interaction):

        validation_error = validate_trade_setup(self.give, self.receive, self.clan_tag)

        if validation_error:
            return await interaction.response.send_message(validation_error, ephemeral=True)


        clan = get_clan_by_tag(self.clan_tag)
        trader_role, trade_channel = get_settings_by_guild(interaction.guild)

        if not trade_channel:
            return await interaction.response.send_message(
                "Er is geen kanaal ingesteld voor ruilvoorstellen. Neem contact op met een beheerder.",
                ephemeral=True
            )

        trade_content = trader_role.mention if trader_role else None
        trade_embed = create_trade_setup_embed(interaction.user, self.color, clan, self.give, self.receive)
        trade_view = TradeView(self.clan_tag, self.give, self.receive, initiator=interaction.user)

        trade_message = await trade_channel.send(content=trade_content, embed=trade_embed, view=trade_view)

        await interaction.response.edit_message(content=f"Je ruilvoorstel is verzonden naar {trade_message.jump_url}.", embed=None, view=None, delete_after=60)



    async def cancel_button_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="Je hebt deze ruil geannuleerd.", embed=None, view=None, delete_after=60)

# Helper functions

def validate_trade_setup(give: list[str], receive: list[str], clan_tag: str) -> str | None:
    if not give:
        return "Je moet minstens één kaart kiezen die je wilt weggeven."

    if not receive:
        return "Je moet minstens één kaart kiezen die je wilt ontvangen."

    if set(give) & set(receive):
        return "Je kunt geen kaarten ontvangen die je zelf al hebt gekozen om weg te geven."

    if not clan_tag:
        return "Je moet een clan selecteren waar je de kaarten wilt ruilen."

    return None

def get_clan_by_tag(clan_tag: str) -> Clan | None:
    return next((clan for clan in CLANS if clan.tag == clan_tag), None)

def get_settings_by_guild(guild: discord.Guild) -> tuple[discord.Role | None, discord.TextChannel | None]:

    role_id = Guild.get_trader_role_id(guild.id)
    channel_id = Guild.get_trader_channel_id(guild.id)

    role = guild.get_role(role_id)
    channel = guild.get_channel(channel_id)

    if not isinstance(channel, discord.TextChannel):
        channel = None

    return role, channel

def create_trade_setup_embed(initiator: discord.Member, color: discord.Colour, clan: Clan | None, give: list[str], receive: list[str]) -> discord.Embed:

    embed = discord.Embed(
        title="Clash of Cards",
        description=(
            f"{initiator.mention} wilt kaarten ruilen in **{clan.name}**:\n"
            if clan
            else f"{initiator.mention} wilt kaarten ruilen:\n"
        ),
        color=color
    )

    embed.add_field(
        name="Weggeven",
        value="\n".join(f"• {card}" for card in give),
        inline=True
    )

    embed.add_field(
        name="Ontvangen",
        value="\n".join(f"• {card}" for card in receive),
        inline=True
    )

    return embed