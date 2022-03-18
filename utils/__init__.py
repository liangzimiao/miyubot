# -*- coding: utf-8 -*-
"""
@Time    : 2021/11/29 8:54
@Author  : 物述有栖
@File    : __init__.py.py
@DES     :
"""
import base64
import json
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from io import BytesIO

import pytz
import unicodedata
import zhconv
from PIL import Image
from nonebot import get_driver, logger
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11.event import Sender
from nonebot_plugin_guild_patch import GuildMessageEvent, patched_send
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


def load_config(inbuilt_file_var):
    """
    Just use `config = load_config(__file__)`,
    you can get the config.json as a dict.
    """
    filename = os.path.join(os.path.dirname(inbuilt_file_var), 'config.json')
    try:
        with open(filename, encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        logger.exception(e)
        return {}


class DailyNumberLimiter:
    tz = pytz.timezone('Asia/Shanghai')

    def __init__(self, max_num):
        self.today = -1
        self.count = defaultdict(int)
        self.max = max_num

    def check(self, key) -> bool:
        now = datetime.now(self.tz)
        day = (now - timedelta(hours=5)).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, num=1):
        self.count[key] += num

    def reset(self, key):
        self.count[key] = 0


def concat_pic(pics, border=5):
    num = len(pics)
    w, h = pics[0].size
    des = Image.new('RGBA', (w, num * h + (num - 1) * border), (255, 255, 255, 255))
    for i, pic in enumerate(pics):
        des.paste(pic, (0, i * (h + border)), pic)
    return des


def pic2b64(pic: Image) -> str:
    buf = BytesIO()
    pic.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()
    return 'base64://' + base64_str
