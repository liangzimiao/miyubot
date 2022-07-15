
from nonebot import  logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
import nonebot
from utils.json_Manager import readJson, removeJson, writeJson
from nonebot.matcher import Matcher
from typing import Type

cdTime = (
    nonebot.get_driver().config.cd if nonebot.get_driver().config.cd else 60
)

async def check_cd(matcher:Type[Matcher],event:MessageEvent,name:str):
    print(name)
    data = readJson(name)
    try:
        cd = event.time - data[event.get_user_id()][0]
    except:
        cd = cdTime + 1

    if cd > cdTime: #or event.get_user_id() in nonebot.get_driver().config.superusers:
        writeJson(event.get_user_id(), event.time, event.message_id, data,name)
        try:
            return 
        except Exception as e:
                logger.warning(e)
                removeJson(event.get_user_id(),name)
    else:
        await matcher.finish(f"别急~  CD还有{cdTime - cd}秒", at_sender=True)
        #return False