from dataclasses import dataclass

import discord

from data.cards import ELIXIR_CARDS, DARK_ELIXIR_CARDS, BUILDER_BASE_CARDS, SUPER_TROOP_CARDS
from data.database import Clan
from enum import Enum

class TradeType(Enum):
    ELIXIR = 0
    DARK_ELIXIR = 1
    BUILDER_BASE = 2
    SUPER_TROOP = 3

TRADE_TYPES = {
    TradeType.ELIXIR: ("Elixer", discord.Color.pink(), ELIXIR_CARDS),
    TradeType.DARK_ELIXIR: ("Dark Elixer", discord.Color.dark_purple(), DARK_ELIXIR_CARDS),
    TradeType.BUILDER_BASE: ("Builder Base", discord.Color.blue(), BUILDER_BASE_CARDS),
    TradeType.SUPER_TROOP: ("Super Troop", discord.Color.orange(), SUPER_TROOP_CARDS)
}

@dataclass()
class Trade:
    initiator: discord.Member 
    color: discord.Colour
    given: list[str]
    received: list[str]
    clan: Clan | None = None
    acceptor: discord.Member | None = None

    def validate(self) -> str | None:
        if not self.given:
            return "Je moet minstens één kaart kiezen die je wilt weggeven."

        if not self.received:
            return "Je moet minstens één kaart kiezen die je wilt ontvangen."

        if set(self.given) & set(self.received):
            return "Je kunt geen kaarten ontvangen die je zelf al hebt gekozen om weg te geven."

        return None

    def can_accept(self, user: discord.Member) -> bool:

        return self.initiator != user

    def is_participant(self, user: discord.Member) -> bool:

        return user in [self.initiator, self.acceptor]