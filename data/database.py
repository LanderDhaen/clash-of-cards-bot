from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db

class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trade_channel_id = IntegerField(null=True)

    def add_clan(self, clan_tag: str, clan_name: str) -> "Clan":
        return Clan.create(clan_tag=clan_tag, clan_name=clan_name, guild=self)

    def get_clans(self) -> list[str]:

        clans = Clan.select(Clan.clan_tag).where(Clan.guild == self) 

        return [clan.clan_tag for clan in clans]

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
    clan_tag = CharField(primary_key=True)
    clan_name = CharField()
    guild = ForeignKeyField(Guild, backref="clans")

def create_tables() -> None:
    with db:
        db.create_tables([Guild, Clan], safe=True)