from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trader_channel_id = IntegerField(null=True)

    def add_clan(self, clan_tag: str, clan_name: str) -> "Clan":
        return Clan.create(clan_tag=clan_tag, clan_name=clan_name, guild=self)

    def get_clans(self) -> list[str]:

        clans = Clan.select(Clan.clan_tag).where(Clan.guild == self) 

        return [clan.clan_tag for clan in clans]


def get_guild(guild_id: int) -> Guild | None:
    return Guild.get_or_none(Guild.guild_id == guild_id)

def update_settings(guild_id: int, trader_role_id: int, trader_channel_id: int) -> tuple[bool, Guild]:

    guild = get_guild(guild_id)

    if guild is None:
        guild = Guild.create(
            guild_id=guild_id,
            trader_role_id=trader_role_id,
            trader_channel_id=trader_channel_id
        )

        created = True

        return created, guild

    else:
        guild.trader_role_id = trader_role_id
        guild.trader_channel_id = trader_channel_id
        guild.save()

        created = False

        return created, guild

class Clan(BaseModel):
    clan_tag = CharField(primary_key=True)
    clan_name = CharField()
    guild = ForeignKeyField(Guild, backref="clans")

def add_clan_to_guild(clan_tag: str, clan_name: str, guild: Guild) -> Clan:
    return Clan.create(clan_tag=clan_tag, clan_name=clan_name, guild=guild)

def create_tables() -> None:
    with db:
        db.create_tables([Guild, Clan], safe=True)