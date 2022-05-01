# ref: https://github.com/GWYOG/GWYOG-Hoshino-plugins/blob/master/pcravatarguess
# Originally written by @GWYOG
# Reflacted by @Ice-Cirno
# GPL-3.0 Licensed
# Thanks to @GWYOG for his great contribution!

import asyncio
import json
import os
import random
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from plugins.uma.uma_data.resources import uma_res
import utils
from .data_source import UmaGuess
from nonebot.params import  CommandArg
from . import  GameMaster, get_guild_member_info
from PIL import Image
from plugins.uma.chara import  guess_id
PIC_SIDE_LENGTH = 50

BLACKLIST_ID = []  # 黑名单ID

ONE_TURN_TIME = 20

DB_PATH = os.sep.join(['plugins', 'uma', 'data', 'uma_card_guess.db'])
gm = GameMaster(DB_PATH)



matcher = UmaGuess().on_command("猜支援卡卡面排行榜", "猜支援卡卡面排行榜", aliases={"猜支援卡卡面排名", "猜支援卡卡面群排行"}, priority=5)


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


matcher = UmaGuess().on_command("猜支援卡卡面", "猜支援卡卡面",aliases={"猜支援卡", "猜支援卡面","uma guess support card"}, priority=5)


@matcher.handle()
async def avatar_guess(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    if gm.is_playing(get_gid):
        await matcher.finish("游戏仍在进行中…")
    with gm.start_game(get_gid) as game:
        card_info_path=os.path.abspath(os.sep.join(['plugins', 'uma', 'uma_data', 'card_info_dict.json']))
        with open (card_info_path,"r",encoding="utf-8")as f:
            card_info_dict=json.load(f)
        #print(card_info_dict)
        #ids = list(uma_data.CHARA_NAME.keys())
        ids = list(card_info_dict)

        game.answer = random.choice(ids)#str

        while int(game.answer) in BLACKLIST_ID:
            game.answer = random.choice(ids)

        c = card_info_dict[game.answer]["chara"]
        uma_res.support_card_download(game.answer)
        card_dir = f'resources\\uma\\img\\support_card\\Support_thumb_{game.answer}.png'

        img = Image.open(card_dir)

        w, h = img.size
        l = random.randint(0, w - PIC_SIDE_LENGTH)
        u = random.randint(0, h - PIC_SIDE_LENGTH)
        cropped = img.crop((l, u, l + PIC_SIDE_LENGTH, u + PIC_SIDE_LENGTH))
        cropped = utils.pic2b64(cropped)
        await matcher.send(
            f'猜猜这个支援卡的相关角色是哪位角色?({ONE_TURN_TIME}s后公布答案)' + MessageSegment.image(cropped, cache=False))
        await asyncio.sleep(ONE_TURN_TIME)
        
        if game.winner:
            return

    meg = utils.pic2b64(img)

    await matcher.send(
        f"正确答案是：{c}" + MessageSegment.image(meg, cache=False) + f"\n很遗憾，没有人答对~\n(别名库还有待补充，目前支持wiki以及部分别名)")


sv = UmaGuess().on_message(priority=5)


@sv.handle()
async def on_input_card_name(bot: Bot, event: MessageEvent):

    get_gid=get_id(event)[1]
    game = gm.get_game(get_gid)
    if not game or game.winner:
        return
    
    c = event.message.extract_plain_text()

    card_info_path=os.path.abspath(os.sep.join(['plugins', 'uma', 'uma_data', 'card_info_dict.json']))
    with open (card_info_path,"r",encoding="utf-8")as f:
        card_info_dict=json.load(f)
    answer = card_info_dict[game.answer]["chara"]   

    flag = guess_id(c)[0]==guess_id(answer)[0] and guess_id(c)[2]>=90 and guess_id(answer)[2]>=90
    if (c == answer) or  flag:

        game.winner = event.user_id

        n = game.record()

        card_dir = f'resources\\uma\\img\\support_card\\Support_thumb_{game.answer}.png'
        img = Image.open(card_dir)
        meg = utils.pic2b64(img)

        await sv.send(
        f"猜对了，真厉害！TA已经猜对{n}次了~\n正确答案是{answer}"
        + MessageSegment.image(meg, cache=False) 
        + f"\n(此轮游戏将在几秒后自动结束，请耐心等待)", at_sender=True)


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
    