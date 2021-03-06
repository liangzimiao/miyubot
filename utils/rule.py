from nonebot import get_driver
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent
from .base_config import Config
from .service import ServiceTools
from nonebot.typing import T_State


def is_in_service(service: str) -> Rule:
    async def _is_in_service(bot, event, state) -> bool:
        result = ServiceTools().auth_service(service)
        if not result:
            return False

        if isinstance(event, PrivateMessageEvent):
            user_id = event.get_user_id()
            result = ServiceTools().auth_service(service, user_id)
            return result
        elif isinstance(event, GroupMessageEvent):
            user_id = event.get_user_id()
            group_id = str(event.group_id)
            result = ServiceTools().auth_service(service, user_id, group_id)
            return result
        elif isinstance(event, GuildMessageEvent):
            user_id = event.get_user_id()
            gc_id = f'{event.guild_id}_{event.channel_id}'
            result = ServiceTools().auth_service(service, user_id, gc_id)
            return result
        else:
            return True

    return Rule(_is_in_service)


global_config = get_driver().config
config = Config(**global_config.dict())
bot_id = config.dict().get("bot_id")
bot_guild_id = config.dict().get("bot_guild_id")


def to_bot() -> Rule:
    return Rule(_to_bot)


async def _to_bot(bot: Bot, event: MessageEvent, state: T_State) -> bool:
    jud = f"[CQ:at,qq={bot_guild_id}" in str(event.raw_message)
    #print(f"[CQ:at,qq={bot_guild_id}" in str(event.raw_message))
    #print(event.is_tome() or jud)
    
    return event.is_tome() or jud
