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
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
import utils
from .data_source import Guess
from nonebot.params import  CommandArg
from plugins.pcr import  chara, pcr_data
from . import  GameMaster, get_guild_member_info

PIC_SIDE_LENGTH = 180
ONE_TURN_TIME = 20
BASE_WIN_COIN = 175
RANK_WIN_COIN = 50
GET_COIN_CD = 60 * 60
DB_PATH = os.sep.join(['plugins', 'pcr', 'data', 'pcr_card_guess.db'])
BLACKLIST_ID = [1000, 1072, 1908, 4031, 9000, 1069, 1073, 1701, 1702, 1067, 1907, 1909, 1910, 1911, 1913, 1914, 1915,
                1916, 1917, 1918, 1919, 1920, 9601, 9602, 9603, 9604]  # 黑名单ID
gm = GameMaster(DB_PATH)



matcher = Guess().on_command("猜卡面排行榜", "猜卡面排行榜", aliases={"猜卡面排名", "猜卡面群排行"}, priority=5)


@matcher.handle()
async def description_guess_group_ranking(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    type=get_id(event)[2]
    ranking = gm.db.get_ranking(get_gid)
    msg = ["【猜卡面小游戏排行榜】"]
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


matcher = Guess().on_command("猜卡面", "猜卡面", priority=5)


@matcher.handle()
async def avatar_guess(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
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
        img = c.card.open()
        w, h = img.size
        l = random.randint(0, w - PIC_SIDE_LENGTH)
        u = random.randint(0, h - PIC_SIDE_LENGTH)
        cropped = img.crop((l, u, l + PIC_SIDE_LENGTH, u + PIC_SIDE_LENGTH))

        cropped = utils.pic2b64(cropped)
        await matcher.send(
            f'猜猜这个图片是哪位角色卡面的一部分?({ONE_TURN_TIME}s后公布答案)' + MessageSegment.image(cropped, cache=False))
        await asyncio.sleep(ONE_TURN_TIME)
        if game.winner:
            return
    txt = f"正确答案是：{c.name}"
    meg = c.card.cqcode
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
        msg = c.card.cqcode
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
    