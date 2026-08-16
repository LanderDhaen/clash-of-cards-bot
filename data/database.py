from peewee import *

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trader_channel_id = IntegerField(null=True)


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

def create_tables() -> None:
    with db:
        db.create_tables([Guild], safe=True)