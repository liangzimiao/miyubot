# -*- coding: utf-8 -*-
from asyncio import events
import traceback
from typing import Dict
import json

from aiohttp.client_exceptions import ClientError

from nonebot import get_driver
from nonebot.params import State, ArgPlainText, Arg, CommandArg
from nonebot.plugin import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, PrivateMessageEvent, Message
from nonebot.typing import T_State
from nonebot.utils import DataclassEncoder
from nonebot_plugin_guild_patch import GuildMessageEvent

from .ex import get_des as get_des_ex
from .iqdb import get_des as get_des_iqdb
from .saucenao import get_des as get_des_sau
from .ascii2d import get_des as get_des_asc
from .trace import get_des as get_des_trace
from .yandex import get_des as get_des_yandex

from .utils import limiter

global_config = get_driver().config
record_priority = getattr(global_config, "record_priority", 99)

async def get_des(url: str, mode: str):
    """
    :param url: 图片链接
    :param mode: 图源
    :return:
    """
    if mode == "iqdb":
        async for msg in get_des_iqdb(url):
            yield msg
    elif mode == "ex":
        async for msg in get_des_ex(url):
            yield msg
    elif mode == "trace":
        async for msg in get_des_trace(url):
            yield msg
    elif mode == "yandex":
        async for msg in get_des_yandex(url):
            yield msg
    elif mode.startswith("asc"):
        async for msg in get_des_asc(url):
            yield msg
    else:
        async for msg in get_des_sau(url):
            yield msg


setu = on_command("搜图",aliases={"search"},# rule=to_me()
)


@setu.handle()
async def handle_first_receive(event: MessageEvent, state: T_State = State(), setu: Message = CommandArg()):

    if bool(event.reply):
        state["setu"] = "setu"
        return
    if setu:
        state["setu"] = setu
    
@setu.got("setu", prompt="图呢？")
async def get_setu(bot: Bot,
                   event: MessageEvent,
                   state: T_State = State(),
                   msg: Message = Arg("setu")):
    list=["1","asc"]
    if state["setu"]== "setu":
        return
    try:
        if msg[0].type == "image":
                await bot.send(event=event, message="正在处理图片")
                url = msg[0].data["url"]  # 图片链接
                
                if 1==1:
                    if not getattr(bot.config, "risk_control", None) or isinstance(event, PrivateMessageEvent) or isinstance(event, GuildMessageEvent):  # 安全模式
                        async for msg in limiter(get_des(url, "mod"), getattr(bot.config, "search_limit", None) or 2):
                            msg_info = await bot.send(event=event, message=msg)
                            add_withdraw_job(bot, **msg_info)
                    else:
                        msgss=[]
                        for mod in list:
                            async for msg in get_des(url, mod):
                                msgss.append(msg)
                        msgs: Message = sum(
                                [msg if isinstance(msg, Message) else Message(msg)  for msg in msgss] 
                                )
                        dict_data = json.loads(json.dumps(msgs, cls=DataclassEncoder))  
                                        
                        msg_info = await bot.send_group_forward_msg(group_id=event.group_id,
                                                        messages=[
                                                            {
                                                                "type": "node",
                                                                "data": {
                                                                    "name": event.sender.nickname,
                                                                    "uin": event.user_id,
                                                                    "content": 
                                                                        content
                                                                }
                                                            }
                                                            for content in dict_data
                                                        ]
                                                        
                                                        )
                        add_withdraw_job(bot, **msg_info)
        else:
                return
    except (IndexError, ClientError):
        await bot.send(event, "traceback.format_exc()")
        await setu.finish("参数错误")



setu = on_command("搜图",aliases={"search"}, #rule=to_me()
)
@setu.handle()
async def get_setu(bot: Bot,event: MessageEvent):
    list=["1","asc"]
    try:
        if event.reply:
            msg: Message = event.reply.message
            print(msg)
            if msg[0].type == "image":
                await bot.send(event=event, message="正在处理图片")
                url = msg[0].data["url"]  # 图片链接
                if 1==1:
                    if not getattr(bot.config, "risk_control", None) or isinstance(event, PrivateMessageEvent) or isinstance(event, GuildMessageEvent):  # 安全模式

                        async for msg in limiter(get_des(url, "mod"), getattr(bot.config, "search_limit", None) or 2):

                            msg_info = await bot.send(event=event, message=msg)
                            add_withdraw_job(bot, **msg_info)
                    else:
                        msgss=[]
                        for mod in list:
                            async for msg in get_des(url, mod):
                                msgss.append(msg)
                            msgs: Message = sum(
                                    [msg if isinstance(msg, Message) else Message(msg)  for msg in msgss] 
                                    )
                        dict_data = json.loads(json.dumps(msgs, cls=DataclassEncoder))                  
                        msg_info = await bot.send_group_forward_msg(group_id=event.group_id,
                                                        messages=[
                                                            {
                                                                "type": "node",
                                                                "data": {
                                                                    "name": event.sender.nickname,
                                                                    "uin": event.user_id,
                                                                    "content": 
                                                                        content
                                                                    
                                                                }
                                                            }
                                                            for content in dict_data
                                                        ]
                        
                                                        )
                        add_withdraw_job(bot, **msg_info)
            else:
                await setu.finish("这不是图,重来!")
    except (IndexError, ClientError):
        await bot.send(event, "traceback.format_exc()")

 
import time
import datetime
from nonebot import  get_driver
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot
from nonebot_plugin_apscheduler import scheduler


WITHDRAW_TIME = 60


def add_withdraw_job(bot: Bot, message_id: int):
    if WITHDRAW_TIME:
        logger.debug("添加撤回任务")
        scheduler.add_job(
            withdraw_msg,
            "date",
            args=[bot, message_id],
            run_date=datetime.datetime.fromtimestamp(time.time() + WITHDRAW_TIME),  # type: ignore
        )


async def withdraw_msg(bot: Bot, message_id: int):
    await bot.delete_msg(message_id=message_id)   