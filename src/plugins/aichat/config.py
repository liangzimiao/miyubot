from pydantic import BaseSettings


class Config(BaseSettings):
    tuling_url: str
    tuling_apikey: str

    class Config:
        extra = "ignore"
