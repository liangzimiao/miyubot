
from nonebot import  logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
import nonebot
from utils.json_Manager import readJson, removeJson, writeJson
from nonebot.matcher import Matcher
from typing import Type


async def check_cd(matcher:Type[Matcher],event:MessageEvent,name:str,cdTime=60,displayCD=False,reply=True):

    data = readJson(name)
    try:
        cd = event.time - data[event.get_user_id()][0]
    except:
        cd = cdTime + 1
    try:
        num =  data[event.get_user_id()][2]
    except:
        num = 0

    if cd > cdTime :#or event.get_user_id() in nonebot.get_driver().config.superusers:
        writeJson(event.get_user_id(), event.time, event.message_id, data,name)
        try:
            return 
        except Exception as e:
                logger.warning(e)
                removeJson(event.get_user_id(),name)
    else:
        num = num + 1
        writeJson(event.get_user_id(), data[event.get_user_id()][0], event.message_id, data,name,num)
        if num == 4:
            time = event.time + 600
            writeJson(event.get_user_id(), time, event.message_id, data,name,num)
            await matcher.finish(f"检测到刷屏行为,禁用{cdTime - cd + 600}秒", at_sender=True)
        if  num > 4:
            reply=False
        if reply:
            if displayCD:
                await matcher.finish(f"别急~  CD还有{cdTime - cd}秒", at_sender=True)
            else:
                await matcher.finish(f"别急~  还在CD中", at_sender=True)
        else:
            await matcher.finish()