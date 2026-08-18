from __future__ import annotations
from enum import Enum
import discord
from peewee import *

from data.cards import BUILDER_BASE_CARDS, DARK_ELIXIR_CARDS, ELIXIR_CARDS, SUPER_TROOP_CARDS


db = SqliteDatabase("database.db")

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


class BaseModel(Model):
    class Meta:
        database = db

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

class Clan(BaseModel):
    tag = CharField(primary_key=True)
    name = CharField()
    guild = ForeignKeyField(Guild, backref="clans")

def get_clan(clan_tag: str, guild_id: int) -> Clan | None:
    return Clan.get_or_none((Clan.tag == clan_tag) & (Clan.guild == guild_id))

class Trade(BaseModel):
    trade_id = IntegerField(primary_key=True)
    type = IntegerField(choices=TRADE_TYPES)
    given = JSONField()
    received = JSONField()
    initiator_id = IntegerField()
    acceptor_id = IntegerField(null=True)
    message_id = IntegerField()
    guild = ForeignKeyField(Guild, backref="trades")
    clan = ForeignKeyField(Clan, null=True)

    def validate(self) -> str | None:
        if not self.given:
            return "Je moet minstens één kaart kiezen die je wilt weggeven."

        if not self.received:
            return "Je moet minstens één kaart kiezen die je wilt ontvangen."

        if set(self.given) & set(self.received):
            return "Je kunt geen kaarten ontvangen die je zelf al hebt gekozen om weg te geven."

        return None

    def can_accept(self, user_id: int) -> bool:

        return self.initiator_id != user_id

    def is_participant(self, user_id: int) -> bool:

        return user_id in [self.initiator_id, self.acceptor_id]


def create_tables() -> None:
    with db:
        db.create_tables([Guild, Clan, Trade], safe=True)