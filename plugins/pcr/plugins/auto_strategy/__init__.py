
from nonebot_plugin_apscheduler import scheduler
from .download import update_data,load_config,local_path

import os
from nonebot.adapters.onebot.v11 import Bot, Message,MessageSegment,MessageEvent
from nonebot.plugin import on_command,on_regex
from nonebot.permission import SUPERUSER
type_list = ['rank','activity','equipment','half_month','gocha','dragon','strength']

'''
指令：
rank
活动攻略/sp/vh
刷图推荐
半月刊
千里眼
地下城
屯体
更新攻略缓存
'''


def general_info(config,type_set):
    msg = ''
    for strategy in config:
        if strategy['text']:
            msg += strategy['text']
        for image in strategy['image']:
            image_path = os.path.abspath(os.path.join(local_path,f'{type_set}',image))
            msg += MessageSegment.image(f'file:///{image_path}')
    return msg

matcher = on_regex(r"^((活动(攻略|图)?)|(?i)sp|(?i)vh)$", priority=5)

@matcher.handle()
async def activity(bot: Bot, event: MessageEvent):
    type = 'activity'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")

matcher = on_regex(r"^(刷图|装备)(推荐|攻略)?$", priority=5)
@matcher.handle()
async def equipment(bot: Bot, event: MessageEvent):
    type = 'equipment'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")

matcher = on_regex(r"^半月刊|大记事$", priority=5)
@matcher.handle()
async def half_month(bot: Bot, event: MessageEvent):
    type = 'half_month'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")

matcher = on_regex(r"^(千|万)里眼$", priority=5)
@matcher.handle()
async def gocha(bot: Bot, event: MessageEvent):
    type = 'gocha'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")

matcher = on_regex(r"^地下城|ex(\d{1})?$", priority=5)
@matcher.handle()
async def dragon(bot: Bot, event: MessageEvent):
    type = 'dragon'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")

matcher = on_regex(r"^(屯|存|囤)体$", priority=5)
@matcher.handle()
async def save_strength(bot: Bot, event: MessageEvent):
    type = 'strength'
    config = load_config(os.path.join(local_path,type,'route.json'))
    if config:
        msg = general_info(config,type)
        await matcher.send(msg)
    else:
        await matcher.send("请先发送【更新攻略缓存】")
matcher = on_command("更新攻略缓存", priority=5, permission=SUPERUSER)
@matcher.handle()
async def update_cache(bot: Bot, event: MessageEvent):
    for type in type_list:
        try:
            await update_data(type,True)
        except:
            await matcher.send(f"{type}更新失败")
    await matcher.send("更新完成")

@scheduler.scheduled_job('cron', hour='17', minute='06')
async def schedule_update_rank_cache():
    for type in type_list:
        try:
            await update_data(type,False)
        except:
            pass
