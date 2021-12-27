from pydantic import BaseSettings


class Config(BaseSettings):
    tuling_url: str
    tuling_apikey: str
    bot_id: str
    bot_guild_id: str

    class Config:
        extra = "ignore"
