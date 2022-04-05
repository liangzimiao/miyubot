# ref: https://github.com/GWYOG/GWYOG-Hoshino-plugins/blob/master/pcravatarguess
# Originally written by @GWYOG
# Reflacted by @Ice-Cirno
# GPL-3.0 Licensed
# Thanks to @GWYOG for his great contribution!

import asyncio
import os
import random
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.plugin import on_command, on_message
from nonebot.typing import T_State
from nonebot.params import  CommandArg
from .data_source import  Guess
import utils
from plugins.pcr import  chara, pcr_data
from . import  GameMaster, get_guild_member_info

PATCH_SIZE = 32
ONE_TURN_TIME = 20
DB_PATH = os.sep.join(['plugins', 'pcr', 'data', 'pcr_avatar_guess.db'])
BLACKLIST_ID = [1072, 1908, 4031, 9000]
gm = GameMaster(DB_PATH)


matcher = Guess().on_command("猜头像排行","猜头像排行", aliases={"猜头像排名", "猜头像排行榜"}, priority=5)


@matcher.handle()
async def description_guess_group_ranking(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    type=get_id(event)[2]
    ranking = gm.db.get_ranking(get_gid)
    msg = ["【猜头像小游戏排行榜】"]
    for i, item in enumerate(ranking):
        uid, count = item
        if type == 'guild':
            m = get_guild_member_info(get_gid, uid) or uid
        if type == 'group':
            user = await bot.get_group_member_info(group_id=event.group_id, user_id=uid)
            m = user['card'] if user['card'] else user['nickname']
        name = str(m)
        msg.append(f"第{i + 1}名：{name} 猜对{count}次")
    await matcher.send("\n".join(msg))


matcher = Guess().on_command("猜头像","猜头像", priority=5)


@matcher.handle()
async def avatar_guess(bot: Bot, event: MessageEvent, state: T_State,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    if gm.is_playing(get_gid):
        await matcher.finish("游戏仍在进行中…")
    with gm.start_game(get_gid) as game:
        ids = list(pcr_data.CHARA_NAME.keys())
        game.answer = random.choice(ids), random.choice((3, 6))
        while chara.is_npc(game.answer[0]):
            game.answer = random.choice(ids), random.choice((3, 6))

        c = chara.fromid(game.answer[0], game.answer[1])
        img = c.icon.open()
        print(str(img))
        w, h = img.size
        l = random.randint(0, w - PATCH_SIZE)
        u = random.randint(0, h - PATCH_SIZE)
        cropped = img.crop((l, u, l + PATCH_SIZE, u + PATCH_SIZE))
        cropped = utils.pic2b64(cropped)
        await matcher.send(
                f"猜猜这个图片是哪位角色头像的一部分?({ONE_TURN_TIME}s后公布答案)" + MessageSegment.image(cropped, cache=False))
        await asyncio.sleep(ONE_TURN_TIME)
        if game.winner:
            return
    txt = f"正确答案是：{c.name}"
    meg = c.icon.cqcode
    await matcher.send(Message(txt + meg) + f"\n很遗憾，没有人答对~")


sv = Guess().on_message(priority=5)


@sv.handle()
async def on_input_chara_name(bot: Bot, event: MessageEvent):
    get_gid=get_id(event)[1]
    game = gm.get_game(get_gid)
    if not game or game.winner:
        return
    c = chara.fromname(event.message.extract_plain_text(), game.answer[1])
    if c.id != chara.UNKNOWN and c.id == game.answer[0]:
        game.winner = event.user_id
        n = game.record()
        txt = f"猜对了，真厉害！TA已经猜对{n}次了~\n正确答案是{c.name}"
        msg = c.icon.cqcode
        await sv.send(Message(txt + msg) + f"\n(此轮游戏将在几秒后自动结束，请耐心等待)", at_sender=True)



def get_id(event: MessageEvent):
    type = str(event.message_type)
    if type == 'group':
        group_id = event.group_id
        user_id = event.user_id
        get_gid = group_id
    elif type == 'private':
        user_id = event.user_id
        get_gid = user_id
    elif type == 'guild':
        guild_id = event.guild_id
        gc_id = f'{guild_id}'
        user_id = event.user_id
        get_gid = gc_id
    else:
        return 
    return user_id,get_gid,type
    
