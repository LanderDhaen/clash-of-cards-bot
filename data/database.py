from __future__ import annotations
from enum import Enum
import discord
from peewee import *

from config import IS_DEVELOPMENT
from data.cards import BUILDER_BASE_CARDS, DARK_ELIXIR_CARDS, ELIXIR_CARDS, SUPER_TROOP_CARDS


db = SqliteDatabase("db/database.db" if IS_DEVELOPMENT else "/db/database.db")

class BaseModel(Model):
    class Meta:
        database = db

## Guild

class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trade_channel_id = IntegerField(null=True)

    def has_clan(self, clan_tag: str) -> bool:
        return Clan.select().where((Clan.guild == self) & (Clan.tag == clan_tag)).exists()

    def add_clan(self, clan_tag: str, clan_name: str) -> Clan:
        return Clan.create(tag = clan_tag, name = clan_name, guild = self)

    def remove_clan(self, clan_tag: str) -> Clan:
        clan = Clan.get(tag = clan_tag, guild = self)
        clan.delete_instance()

        return clan

    def get_clan(self, clan_tag: str) -> Clan | None:
        return Clan.get_or_none((Clan.tag == clan_tag) & (Clan.guild == self))

    def get_clans(self):
        return Clan.select().where(Clan.guild == self) 

    def update_settings(self, trader_role_id: int, trade_channel_id: int) -> None:
        self.trader_role_id = trader_role_id
        self.trade_channel_id = trade_channel_id
        self.save()
        


def get_guild(guild_id: int) -> Guild | None:
    return Guild.get_or_none(Guild.guild_id == guild_id)

def create_guild(guild_id: int, trader_role_id: int, trade_channel_id: int) -> Guild:
    return Guild.create(
        guild_id=guild_id,
        trader_role_id=trader_role_id,
        trade_channel_id=trade_channel_id
    )

## Clan

class Clan(BaseModel):
    tag = CharField(primary_key=True)
    name = CharField()
    guild = ForeignKeyField(Guild, backref="clans")

## Trade

class TradeType(Enum):
    ELIXIR = 0
    DARK_ELIXIR = 1
    BUILDER_BASE = 2
    SUPER_TROOP = 3

TRADE_TYPES = {
    TradeType.ELIXIR: (discord.Color.pink(), ELIXIR_CARDS),
    TradeType.DARK_ELIXIR: (discord.Color.dark_purple(), DARK_ELIXIR_CARDS),
    TradeType.BUILDER_BASE: (discord.Color.blue(), BUILDER_BASE_CARDS),
    TradeType.SUPER_TROOP: (discord.Color.orange(), SUPER_TROOP_CARDS)
}


class Trade(BaseModel):
    trade_id = IntegerField(primary_key=True)
    type = IntegerField(choices=TRADE_TYPES)
    given = JSONField()
    received = JSONField()
    message_id = IntegerField(null=True)
    thread_id = IntegerField(null=True)
    initiator_id = IntegerField()
    acceptor_id = IntegerField(null=True)
    guild = ForeignKeyField(Guild, backref="trades")
    clan = ForeignKeyField(Clan, null=True)

    def can_accept(self, user_id: int) -> bool:

        return self.initiator_id != user_id

    def can_cancel(self, user_id: int) -> bool:

        return self.initiator_id == user_id

    def is_participant(self, user_id: int) -> bool:

        return user_id in [self.initiator_id, self.acceptor_id]

    def matching_trades(self) -> list[Trade]:

        trades = Trade.select().where(
            (Trade.type == self.type) &
            (Trade.guild == self.guild) &
            (Trade.acceptor_id.is_null(True)) & 
            (Trade.initiator_id != self.initiator_id)
        )

        matching_trades = []

        ## Check if any given cards match with the received cards of other trades and vice versa

        for trade in trades:
            if set(self.given) & set(trade.received) and set(self.received) & set(trade.given):
                matching_trades.append(trade)

        return matching_trades

def get_trades() -> list[Trade]:
    return Trade.select()

def validate_given_and_received(given: list[str], received: list[str]) -> str | None:
    if not given:
        return "Je moet minstens één kaart kiezen die je wilt weggeven."

    if not received:
        return "Je moet minstens één kaart kiezen die je wilt ontvangen."

    if set(given) & set(received):
        return "Je kunt geen kaarten ontvangen die je zelf al hebt gekozen om weg te geven."

    return None


def create_tables() -> None:
    with db:
        db.create_tables([Guild, Clan, Trade], safe=True)