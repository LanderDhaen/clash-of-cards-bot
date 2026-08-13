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


def create_tables() -> None:
    with db:
        db.create_tables([Guild], safe=True)