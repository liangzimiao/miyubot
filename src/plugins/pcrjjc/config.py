from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    bot_id: str
    bot_guild_id: str

    class Config:
        extra = "ignore"


global_config = get_driver().config
config = Config(**global_config.dict())

bot_id = config.dict().get("bot_id")
bot_guild_id = config.dict().get("bot_guild_id")
