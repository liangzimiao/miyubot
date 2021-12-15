from pydantic import BaseSettings


class Config(BaseSettings):
    bot_id: str
    bot_guild_id: str

    class Config:
        extra = "ignore"
