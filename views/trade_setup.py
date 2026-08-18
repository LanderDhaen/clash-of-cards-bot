import discord

from data.database import TRADE_TYPES, TradeType, Guild

class TradeSetupView(discord.ui.View):

    def __init__(self, trade_type: TradeType, guild: Guild):
        super().__init__(timeout=300)

        self.trade_type = trade_type
        self.guild = guild

        ## Card Selects

        self.color, cards = TRADE_TYPES[trade_type]
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