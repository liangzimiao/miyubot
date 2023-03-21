from nonebot import get_driver
from nonebot.config import Config

global_config:Config = get_driver().config
class  BotInfo:
    bot_id=global_config.bot_id
    bot_guild_id=global_config.bot_guild_id
    superusers=global_config.superusers





