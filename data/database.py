from __future__ import annotations
from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db

class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trade_channel_id = IntegerField(null=True)

    def has_clan(self, clan_tag: str) -> bool:
        return Clan.select().where((Clan.guild == self) & (Clan.tag == clan_tag)).exists()

    def add_clan(self, clan_tag: str, clan_name: str) -> "Clan":
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

def create_tables() -> None:
    with db:
        db.create_tables([Guild, Clan], safe=True)