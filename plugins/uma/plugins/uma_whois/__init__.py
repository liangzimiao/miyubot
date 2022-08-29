from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Message
from plugins.uma.plugins.uma_whois.data_source import UmaWhois
from plugins.uma import chara

#matcher =on_endswith({'是谁','是谁?','是谁？'},priority=5)
matcher =UmaWhois().on_regex(r'^(.*)是谁([?？ ])?',"whois")

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
        #msg = f'特雷森似乎没有叫"{name}"的人...\n角色别称补全计划:https://github.com/chieri-bot/umamusume-alias'
        #await matcher.send(Message(msg))
        msg = f'您有{confi}%的可能在找{guess_name} {c.icon} {c.name}'
        await matcher.send(Message(msg), at_sender=True)
    else:
        msg = f'{c.icon}{c.name}'
        await matcher.send(Message(msg), at_sender=True)


#matcher =on_startswith('谁是',priority=5)
matcher =UmaWhois().on_regex(r'^谁是(.*)([?？ ])?',"whois")

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
        #msg = f'特雷森似乎没有叫"{name}"的人...\n角色别称补全计划:https://github.com/chieri-bot/umamusume-alias'
        #await matcher.send(Message(msg))
        msg = f'您有{confi}%的可能在找{guess_name} {c.icon} {c.name}'
        await matcher.send(Message(msg))
    else:
        msg = f'{c.icon}{c.name}'
        await matcher.send(Message(msg), at_sender=True)