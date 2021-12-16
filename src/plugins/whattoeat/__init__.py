# -*- coding: utf-8 -*-
"""
@Time    : 2021/12/3 9:25
@Author  : 物述有栖
@File    : __init__.py
@DES     : 
"""
import os
import random
import re

import filetype
import requests
from nonebot import get_driver
from nonebot import logger
from nonebot.adapters.cqhttp import Bot, Message, MessageSegment
from nonebot.plugin import on_command, on_regex
from nonebot.typing import T_State

from alicebot.plugins.nonebot_guild_patch import GuildMessageEvent
from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())
foodsPath = os.path.join(os.path.dirname(__file__), 'foods')

chi = on_regex(pattern=r'^(今天|[早中午晚][上饭餐午]|夜宵)吃(什么|啥|点啥)')


@chi.handle()
async def net_ease_cloud_word(bot: Bot, event: GuildMessageEvent, state: T_State):
    uid = event.get_user_id()
    time = state['_matched_groups'][0]
    food = random.choice(os.listdir(foodsPath))
    name = food.split('.')
    to_eat = f'{time}去吃{name[0]}吧~\n'
    try:
        with open(foodsPath + os.sep + food, 'rb') as f:
            data = f.read()
            f.close()
            to_eat += f'{MessageSegment.image(data)}'
    except Exception as e:
        logger.error(f'读取食物图片时发生错误{type(e)}')
    await chi.finish(Message(to_eat), at_sender=True)


async def download_async(url: str, name: str):
    resp = requests.get(url, stream=True)
    if resp.status_code == 404:
        raise ValueError('文件不存在')
    content = resp.content
    try:
        extension = filetype.guess_mime(content).split('/')[1]
    except:
        raise ValueError('不是有效文件类型')
    abs_path = os.path.join(foodsPath, f'{name}.{extension}')
    with open(abs_path, 'wb') as f:
        f.write(content)


add_f = on_command("加菜")


@add_f.handle()
async def add_food(bot: Bot, event: GuildMessageEvent):
    food = event.get_plaintext().strip()
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(event.message))
    if not ret:
        await add_f.finish('请附带美食图片~')
        return
    url = ret.group(2)
    await download_async(url, food)
    await add_f.finish('食谱已增加~')
