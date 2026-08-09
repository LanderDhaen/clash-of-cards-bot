from peewee import *


db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db

class Guild(BaseModel):
    guild_id = IntegerField(primary_key=True)
    trader_role_id = IntegerField(null=True)
    trader_channel_id = IntegerField(null=True)

    def get_trader_role_id(guild_id: int) -> int | None:

        guild = Guild.get_or_none(Guild.guild_id == guild_id)
        return guild.trader_role_id 

    def get_trader_channel_id(guild_id: int) -> int | None:
        guild = Guild.get_or_none(Guild.guild_id == guild_id)
        return guild.trader_channel_id
      
def create_tables() -> None:
    with db:
        db.create_tables([Guild], safe=True)