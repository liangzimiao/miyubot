# -*- coding: utf-8 -*-
"""
@Time    : 2021/11/29 8:54
@Author  : 物述有栖
@File    : __init__.py.py
@DES     : 
"""
from io import BytesIO
import time
from nonebot.adapters.cqhttp import Message, MessageSegment
from nonebot.adapters.cqhttp.event import Sender
from src.plugins.nonebot_guild_patch import GuildMessageEvent, patched_send
from pydantic import BaseSettings
from nonebot import get_driver
import base64
import unicodedata
import zhconv
from PIL import Image
class Config(BaseSettings):
    bot_id: str
    bot_guild_id: str

    class Config:
        extra = "ignore"


global_config = get_driver().config
config = Config(**global_config.dict())

bot_id = config.dict().get("bot_id")
bot_guild_id = config.dict().get("bot_guild_id")


async def send_guild_message(guild_id, channel_id, message_str):
    bot = get_driver().bots[str(bot_id)]
    sender = Sender(user_id=bot_id)
    event = GuildMessageEvent(time=int(time.time()), self_id=bot_id,
                              post_type='message', sub_type='channel', user_id=bot_guild_id,
                              message_type='guild', message_id='133-38101123160', guild_id=guild_id,
                              channel_id=channel_id, message="0",
                              sender=sender, self_tiny_id=int(bot_guild_id))
    await patched_send(bot, event, Message(message_str))


def pic2b64(pic: Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str

def normalize_str(string) -> str:
    """
    规范化unicode字符串 并 转为小写 并 转为简体
    """
    string = unicodedata.normalize('NFKC', string)
    string = string.lower()
    string = zhconv.convert(string, 'zh-hans')
    return string