

from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.plugin import on_endswith, on_startswith
from nonebot.typing import T_State
from src.plugins.pcrgames import  chara
from nonebot.adapters.onebot.v11 import Bot, Message
matcher =on_endswith({'是谁','是谁?','是谁？'},priority=5)
@matcher.handle()
async def whois(bot: Bot, event: MessageEvent,state: T_State):
    name = event.message.extract_plain_text().strip()
    name = name.split("是", 1)[0]
    print(name)
    if not name:
        return
    id_ = chara.name2id(name)
    confi = 100
    guess = False
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
        guess = True
    c = chara.fromid(id_)

    if confi < 60:
        return
    if guess:
        name = name
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice-Cirno/HoshinoBot/issues/5'
        await matcher.send(Message(msg))
        msg = f'您有{confi}%的可能在找{guess_name} {c.icon.cqcode} {c.name}'
        await matcher.send(Message(msg))
    else:
        msg = f'{c.icon.cqcode} {c.name}'
        await matcher.send(Message(msg), at_sender=True)
matcher =on_startswith('谁是',priority=5)
@matcher.handle()
async def whois(bot: Bot, event: MessageEvent,state: T_State):
    name = event.message.extract_plain_text().strip()
    name = name.split("是", 1)[1]
    name = name.split("?", 1)[0]
    name = name.split("？", 1)[0]
    print(name)
    if not name:
        return
    id_ = chara.name2id(name)
    confi = 100
    guess = False
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
        guess = True
    c = chara.fromid(id_)

    if confi < 60:
        return
    if guess:
        name = name
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice-Cirno/HoshinoBot/issues/5'
        await matcher.send(Message(msg))
        msg = f'您有{confi}%的可能在找{guess_name} {c.icon.cqcode} {c.name}'
        await matcher.send(Message(msg))
    else:
        msg = f'{c.icon.cqcode} {c.name}'
        await matcher.send(Message(msg), at_sender=True)