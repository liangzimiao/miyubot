# import nonebot
import os
import random
import re
import traceback

import requests
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.permission import SUPERUSER

from utils import get_event_gid
from utils.base_config import BotInfo,Tuling
from .data_source import AiChat
from .data_source import Request

black_word = ['色图', '来一井', '贵族签到', '关于']  # 如果有不想触发的词可以填在这里

SecretId = ''  # 填你的SecretIdR
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


enable = AiChat().on_command('调整AI概率', '调整AI概率',permission=SUPERUSER)


@enable.handle()
async def enable_aichat(bot: Bot, event: MessageEvent):
    g_id=get_event_gid(event)
    s = str(event.get_plaintext())
    if s:
        if s.isdigit() and 0 < int(s) < 51:
            chance = int(s)
        else:
            await enable.finish('参数错误: 请输入1-50之间的整数.')
    else:
        chance = DEFAULT_AI_CHANCE  # 后面不接数字时调整为默认概率
    ai_chance[g_id] = chance
    save_data()
    await enable.finish(f'人工智障已启用, 当前bot回复概率为{chance}%.')


close = AiChat().on_command('关闭人工智障', '关闭人工智障',permission=SUPERUSER)


@close.handle()
async def disable_aichat(bot: Bot, event: MessageEvent):
    g_id = get_event_gid(event)
    ai_chance.pop(g_id)
    await close.finish(f'人工智障已禁用')


reply = AiChat().on_message(block=False)


@reply.handle()
async def ai_reply(bot: Bot, event: MessageEvent):
    msg = str(event.get_plaintext())
    g_id = get_event_gid(event)
    tag = False
    if f'[CQ:at,qq={BotInfo.bot_guild_id}]' in str(event.raw_message) or f'[CQ:at,qq={event.self_id }]'in str(event.raw_message):
        tag = True
    if msg == '' or msg in black_word or len(msg) > 100 or g_id not in ai_chance:
        return
    if random.randint(1, 100) <= ai_chance[g_id] or tag:
        req = Request()
        req.userInfo.apiKey = Tuling.tuling_apikey
        req.userInfo.userId = '114514'
        req.perception.inputText.text = msg
        res = requests.post(url=Tuling.tuling_url, data=req.to_json(), timeout=5)
        if res.status_code == 200:
            result = json.loads(res.content)['results'][0]['values']['text']
            await reply.finish(result)
load_data()
