# ref: https://github.com/GWYOG/GWYOG-Hoshino-plugins/blob/master/pcravatarguess
# Originally written by @GWYOG
# Reflacted by @Ice-Cirno
# GPL-3.0 Licensed
# Thanks to @GWYOG for his great contribution!

import asyncio
import os
import random

import shutil
from nonebot import on_keyword
from nonebot.adapters.cqhttp.event import File, MessageEvent
from nonebot.plugin import on_command, on_message
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, message,Message
from pydantic.errors import TupleError
from src.plugins.nonebot_guild_patch import GuildMessageEvent
from configs.path_config import IMAGE_PATH
from configs.path_config import GIF_PATH
from utils.message_builder import image
from pathlib import Path
from nonebot.permission import MESSAGE, SUPERUSER
from typing import Union, List
from nonebot.adapters.cqhttp.permission import GROUP, GROUP_OWNER, PRIVATE,GROUP_ADMIN
import os
import random
import os
import random
import asyncio
from nonebot import require
from src.plugins.pcrgames import GameMaster, chara , _pcr_data, get_guild_member_info 

PREPARE_TIME = 5
ONE_TURN_TIME = 12
TURN_NUMBER = 5
DB_PATH =f'src\plugins\pcrgames\data\pcr_desc_guess.db'
gm = GameMaster(DB_PATH)


matcher = on_command("猜角色排行", aliases={"猜角色排名", "猜角色排行榜", "猜角色群排行"},priority=5)
@matcher.handle()
async def description_guess_group_ranking(bot: Bot, event: MessageEvent,state: T_State):
    args = str(event.get_message()).strip() 
    type = str(event.message_type)
    print(type)
    print(event)
    print(args)
    if args:
        return
    else:
        if type=='group':
                user_id = event.user_id
                group_id = event.group_id
                self_id=event.self_id
                get_gid=group_id
        elif type=='private':
                user_id = event.user_id
                get_gid=user_id
        elif type=='guild':
                guild_id = event.guild_id
                gc_id = f'{guild_id}'
                user_id = event.user_id
                self_id=event.self_tiny_id
                get_gid=gc_id  
        else:
            return
        ranking = gm.db.get_ranking(get_gid)
        msg = ["【猜角色小游戏排行榜】"]
        for i, item in enumerate(ranking):
            uid, count = item
            if type=='guild':
                m=get_guild_member_info(get_gid,uid) or uid
            if type=='group':
                user = await bot.get_group_member_info(group_id=event.group_id, user_id=uid)
                m= user['card'] if user['card'] else user['nickname']
                print(m)
            name =str(m)
            msg.append(f"第{i + 1}名：{name} 猜对{count}次")
        await matcher.send("\n".join(msg))

matcher = on_command("猜角色",aliases={"猜人物"}, priority=5)
@matcher.handle()
async def avatar_guess(bot: Bot, event: MessageEvent,state: T_State):
    args = str(event.get_message()).strip() 
    type = str(event.message_type)
    print(type)
    print(event)
    print(args)
    if args:
        return
    else:
        if type=='group':
                user_id = event.user_id
                group_id = event.group_id
                self_id=event.self_id
                get_gid=group_id
        elif type=='private':
                user_id = event.user_id
                get_gid=user_id
        elif type=='guild':
                guild_id = event.guild_id
                gc_id = f'{guild_id}'
                user_id = event.user_id
                self_id=event.self_tiny_id
                get_gid=gc_id  
        else:
            return
        if gm.is_playing(get_gid):
            await matcher.finish("游戏仍在进行中…")
        with gm.start_game(get_gid) as game:
            game.answer = random.choice(list(_pcr_data.CHARA_PROFILE.keys()))
            profile = _pcr_data.CHARA_PROFILE[game.answer]
            kws = list(profile.keys())
            kws.remove('名字')
            random.shuffle(kws)
            kws = kws[:TURN_NUMBER]
            await matcher.send( f"{PREPARE_TIME}秒后每隔{ONE_TURN_TIME}秒我会给出某位角色的一个描述，根据这些描述猜猜她是谁~")
            await asyncio.sleep(PREPARE_TIME)
            for i, k in enumerate(kws):
                await matcher.send( f"提示{i + 1}/{len(kws)}:\n她的{k}是 {profile[k]}")
                await asyncio.sleep(ONE_TURN_TIME)
                if game.winner:
                    return
            c = chara.fromid(game.answer)
        txt=f"正确答案是：{c.name}"
        meg=c.icon.cqcode
        await matcher.send(Message(txt + meg)+f"\n很遗憾，没有人答对~")

sv = on_message(priority=5)
@sv.handle()
async def on_input_chara_name(bot:Bot, event: MessageEvent):
    type = str(event.message_type)
    if type=='group':
                user_id = event.user_id
                group_id = event.group_id
                self_id=event.self_id
                get_gid=group_id
    elif type=='private':
                user_id = event.user_id
                get_gid=user_id
    elif type=='guild':
                guild_id = event.guild_id
                gc_id = f'{guild_id}'
                user_id = event.user_id
                self_id=event.self_tiny_id
                get_gid=gc_id  
    else:
        return
    game = gm.get_game(get_gid)
    if not game or game.winner:
        return
    c = chara.fromname(event.message.extract_plain_text())
    if c.id != chara.UNKNOWN and c.id == game.answer:
        game.winner = event.user_id
        n = game.record()
        txt=f"猜对了，真厉害！TA已经猜对{n}次了~\n正确答案是{c.name}"
        msg =c.icon.cqcode
        await sv.send(Message(txt + msg)+f"\n(此轮游戏将在几秒后自动结束，请耐心等待)",at_sender=True)
        

    