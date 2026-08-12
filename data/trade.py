from dataclasses import dataclass

import discord

from data.clans import Clan

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