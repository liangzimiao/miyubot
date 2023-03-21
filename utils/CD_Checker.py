
from nonebot import  logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
import nonebot
from nonebot.matcher import Matcher
from typing import Type
import json

data_dir = "./data/CD/"

def readJson(name:str):
    try:
        with open(data_dir + f"{name}usercd.json", "r") as f_in:
            data = json.load(f_in)
            f_in.close()
            return data
    except FileNotFoundError:
        try:
            import os
            os.makedirs(data_dir)
        except FileExistsError:
            pass
        with open(data_dir + f"{name}usercd.json", mode="w") as f_out:
            json.dump({}, f_out)


def writeJson(qid: str, time: int, mid: int, data: dict, name: str, num=0):
    try:
        data[qid] = [time, mid,num]
    except:    
        data = {}
        with open(data_dir + f"{name}usercd.json", "w") as f_out:
            json.dump(data, f_out)
        f_out.close()
        data[qid] = [time, mid, num]
    with open(data_dir + f"{name}usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()


def removeJson(qid: str, name:str):
    with open(data_dir + f"{name}usercd.json", "r") as f_in:
        data = json.load(f_in)
        f_in.close()
    data.pop(qid)
    with open(data_dir + f"{name}usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()


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

    if cd > cdTime or event.get_user_id() in nonebot.get_driver().config.superusers:
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