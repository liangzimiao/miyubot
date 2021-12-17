from pydantic import BaseSettings


class Config(BaseSettings):
    bot_id: str
    bot_guild_id: str
    superusers: list

    class Config:
        extra = "ignore"
