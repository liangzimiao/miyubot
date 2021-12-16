# import nonebot
import os
import random
import re
import traceback

import requests
from ..nonebot_guild_patch import GuildMessageEvent
from nonebot import get_driver
from nonebot.adapters.cqhttp import Bot
from nonebot.plugin import on_command

from .config import Config
from .data_source import Request

global_config = get_driver().config
config = Config(**global_config.dict())
black_word = ['色图', '来一井', '贵族签到']  # 如果有不想触发的词可以填在这里

SecretId = ''  # 填你的SecretId
SecretKey = ''  # 填你的SecretKey

try:
    import ujson as json
except ImportError:
    import json

cq_code_pattern = re.compile(r'\[CQ:\w+,.+]')
salt = None
# CONFIG_PATH = 'data.json'
ai_chance = {}
DEFAULT_AI_CHANCE = 1  # 默认的AI回复概率

# 定义无法获取回复时的「表达（Expression）」
EXPR_DONT_UNDERSTAND = (
    '我现在还不太明白你在说什么呢，但没关系，以后的我会变得更强呢！',
    '我有点看不懂你的意思呀，可以跟我聊些简单的话题嘛',
    '其实我不太明白你的意思……',
    '抱歉哦，我现在的能力还不能够明白你在说什么，但我会加油的～',
    '唔……等会再告诉你'
)


def save_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(ai_chance, f, ensure_ascii=False, indent=2)
    except:
        traceback.print_exc()


def load_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(path):
        save_data()
        return
    try:
        with open(path, encoding='utf8') as f:
            global ai_chance
            ai_chance = json.load(f)
    except:
        traceback.print_exc()


enable = on_command('调整AI概率')


@enable.handle()
async def enable_aichat(bot: Bot, event: GuildMessageEvent):
    gc_id = f'{event.guild_id}_{event.channel_id}'
    s = str(event.get_plaintext())
    if s:
        if s.isdigit() and 0 < int(s) < 51:
            chance = int(s)
        else:
            await enable.finish('参数错误: 请输入1-50之间的整数.')
    else:
        chance = DEFAULT_AI_CHANCE  # 后面不接数字时调整为默认概率
    ai_chance[gc_id] = chance
    save_data()
    await enable.finish(f'人工智障已启用, 当前bot回复概率为{chance}%.')


close = on_command('关闭人工智障')


@close.handle()
async def disable_aichat(bot: Bot, event: GuildMessageEvent):
    ai_chance.pop(str(f'{event.channel_id}_{event.guild_id}'))
    await close.finish(f'人工智障已禁用')


reply = on_command('')


@reply.handle()
async def ai_reply(bot: Bot, event: GuildMessageEvent):
    msg = str(event.get_plaintext())
    gc_id = f'{event.guild_id}_{event.channel_id}'
    if msg.startswith(f'[CQ:at,qq={event.get_user_id()}]'):
        text = re.sub(cq_code_pattern, '', msg).strip()
    else:
        text = msg
    if text == '' or text in black_word or len(text) > 100 or gc_id not in ai_chance:
        return
    if random.randint(1, 100) <= ai_chance[gc_id]:
        req = Request()
        req.userInfo.apiKey = config.dict().get("tuling_apikey")
        req.userInfo.userId = '114514'
        req.perception.inputText.text = text
        res = requests.post(url=config.dict().get("tuling_url"), data=req.to_json(), timeout=5)
        if res.status_code == 200:
            result = json.loads(res.content)['results'][0]['values']['text']
            await reply.finish(result)


load_data()
