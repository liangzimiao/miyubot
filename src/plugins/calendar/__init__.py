# import nonebot

import re
import traceback

from nonebot import get_driver
from nonebot import logger
from nonebot import require
from nonebot.adapters.cqhttp import Bot, Message
from nonebot.plugin import on_regex, on_command
from nonebot.typing import T_State
from src.plugins.nonebot_guild_patch import GuildMessageEvent
from utils import send_guild_message
from .config import Config
from .generate import *

guild_data = {}

global_config = get_driver().config
config = Config(**global_config.dict())
matcher = on_regex(pattern=r'^([国台日])?服?日[历程](.*)')
# matcher = on_command('asdf')

scheduler = require("nonebot_plugin_apscheduler").scheduler


@matcher.handle()
async def _(bot: Bot, event: GuildMessageEvent, state: T_State):
    server_name = state['_matched_groups'][0]
    guild_id = event.guild_id
    channel_id = event.channel_id
    gc_id = f'{guild_id}_{channel_id}'
    if server_name == '台':
        server = 'tw'
    elif server_name == '日':
        server = 'jp'
    elif server_name == '国':
        server = 'cn'
    elif gc_id in guild_data and len(guild_data[gc_id]['server_list']) > 0:
        server = guild_data[gc_id]['server_list'][0]
    else:
        server = 'cn'
    cmd = state['_matched_groups'][1]
    if not cmd:
        im = await generate_day_schedule(server)
        base64_str = im2base64str(im)
        if gc_id not in guild_data or 'cardimage' not in guild_data[gc_id] or not guild_data[gc_id]['cardimage']:
            msg = f'[CQ:image,file={base64_str}]'
        else:
            msg = f'[CQ:cardimage,file={base64_str}]'
    else:
        if gc_id not in guild_data:
            guild_data[gc_id] = {
                'server_list': [],
                'hour': 8,
                'minute': 0,
                'cardimage': False,
            }
        if 'on' in cmd:
            if server not in guild_data[gc_id]['server_list']:
                guild_data[gc_id]['server_list'].append(server)
            save_data()
            msg = f'{server}日程推送已开启'
        elif 'off' in cmd:
            if server in guild_data[gc_id]['server_list']:
                guild_data[gc_id]['server_list'].remove(server)
            save_data()
            msg = f'{server}日程推送已关闭'
        elif 'time' in cmd:
            match = re.search(r'(\d*):(\d*)', cmd)
            if not match or len(match.groups()) < 2:
                msg = '请指定推送时间'
            else:
                guild_data[gc_id]['hour'] = int(match.group(1))
                guild_data[gc_id]['minute'] = int(match.group(2))
                msg = f"推送时间已设置为: {guild_data[gc_id]['hour']}:{guild_data[gc_id]['minute']:02d}"
        elif 'status' in cmd:
            msg = f"订阅日历: {guild_data[gc_id]['server_list']}"
            msg += f"\n推送时间: {guild_data[gc_id]['hour']}:{guild_data[gc_id]['minute']:02d}"
        elif 'cardimage' in cmd:
            if 'cardimage' not in guild_data[gc_id] or not guild_data[gc_id]['cardimage']:
                guild_data[gc_id]['cardimage'] = True
                msg = f'已切换为cardimage模式'
            else:
                guild_data[gc_id]['cardimage'] = False
                msg = f'已切换为标准image模式'
            save_data()
        else:
            msg = '指令错误'
        update_guild_schedule(gc_id)
        save_data()
    await matcher.send(Message(msg))


def load_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(path):
        return
    try:
        with open(path, encoding='utf8') as f:
            data = json.load(f)
            for k, v in data.items():
                guild_data[k] = v
    except:
        traceback.print_exc()


def save_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(guild_data, f, ensure_ascii=False, indent=2)
    except:
        traceback.print_exc()


async def send_calendar(gc_id):
    if str(gc_id) not in guild_data:
        return
    splits = gc_id.split('_')  # guild_id_channel_id
    for server in guild_data[str(gc_id)]['server_list']:
        im = await generate_day_schedule(server)
        base64_str = im2base64str(im)
        if 'cardimage' not in guild_data[gc_id] or not guild_data[gc_id]['cardimage']:
            msg = f'[CQ:image,file={base64_str}]'
        else:
            msg = f'[CQ:cardimage,file={base64_str}]'
        for _ in range(5):  # 失败重试5次
            try:
                await send_guild_message(splits[0], splits[1], msg)
                logger.info(f'群{splits[0]}推送{server}日历成功')
                break
            except:
                logger.info(f'群{splits[0]}推送{server}日历失败')
            await asyncio.sleep(60)


def update_guild_schedule(gc_id):
    if gc_id not in guild_data:
        return
    scheduler.add_job(
        send_calendar,
        'cron',
        args=(gc_id,),
        id=f'calendar_{gc_id}',
        replace_existing=True,
        hour=guild_data[gc_id]['hour'],
        minute=guild_data[gc_id]['minute']
    )


def startup():
    load_data()
    for gc_id in guild_data:
        update_guild_schedule(gc_id)


startup()
