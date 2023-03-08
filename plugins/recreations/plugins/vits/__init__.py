from nonebot import on_message, get_driver,on_command
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

from nonebot.log import logger
import os
import json
from nonebot.exception import ActionFailed, NetworkError
from nonebot.plugin import PluginMetadata
from .config import *
from utils import regex,RegexArg
from utils import aiorequests
import requests
import traceback
from plugins.uma import chara
import asyncio

__plugin_meta__ = PluginMetadata(
    name="gal角色语音",
    description="部分gal角色文本转语音",
    usage="触发方式：@机器人 [角色名][发送|说][文本内容]",
    extra={
        "example": "@机器人 宁宁说おはようございます.",
        "author": "dpm12345 <1006975692@qq.com>",
        "version": "0.3.6",
    },
)

tts_gal = config.tts_gal
auto_delete_voice = True

driver = get_driver()
__valid_names__ = []

@driver.on_startup
def _():
    logger.info("正在检测可以使用的角色语音...")
    asyncio.ensure_future(checkFile( tts_gal, __plugin_meta__, __valid_names__))

voice = on_message(
    regex(r"(?P<name>\S+?)(?:说|发送)(?P<text>.*?)$"), block=True, priority=5)

@voice.handle()
async def voicHandler(
    bot: Bot, event: MessageEvent,
    name: str = RegexArg("name"),
    text: str = RegexArg("text")
):
    # 预处理
    print(name)
    print(text)
    id_ = chara.name2id(name)
    confi = 100
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
    c = chara.fromid(id_)
    if confi < 80:
        name = name
    else:
        name = c.name

    model, index = check_character(name, __valid_names__, tts_gal)
    if model == "":
        return
        #await voice.finish(MessageSegment.at(event.get_user_id()) + "暂时还未有该角色")
    if len(text)>100:
        await voice.finish(MessageSegment.at(event.get_user_id()) + "要说的话太长了哦~") 
    try:
        logger.info("正在生成中...")
        new_voice = ""
        info_dict = {
        "index":index,
        "model":model,
        "text":text,
        } 
        url = "http://127.0.0.1:9998/text2voice"
        headers = {'Content-Type': 'application/json'}
        response = await aiorequests.request("POST", url, headers=headers, data=json.dumps(info_dict), timeout=40)
        if response.status_code != 200:
            logger.error(f'获取语音时发生错误{response.status_code}')
            return 
        result = await response.json()
        new_voice = result ["path"]
        #import aiohttp
        #async with aiohttp.ClientSession() as session:
        #    async with session.post(url, headers=headers, data=json.dumps(info_dict), timeout=30) as response:
        #        result = await response.json()
        #        print (result)
        #        new_voice = result ["path"]
    except:
        traceback.print_exc()
        await voice.finish('生成失败')

    try:
        await voice.send(MessageSegment.record(f'file:///{os.path.abspath(new_voice)}'))
    except ActionFailed:
        traceback.print_exc()
        await voice.send("发送失败,请重试")
    except NetworkError:
        traceback.print_exc()
        await voice.send("发送超时,也许等等就好了")
    finally:
        if auto_delete_voice:
            logger.info("发送完成...已删除")
            os.remove(new_voice)


matcher = on_command("vits角色", block=True, priority=5)

@matcher.handle()
async def load_valid_names_list(bot: Bot,event:MessageEvent):
    valid_names_list = []
    try:
        valid_character_names_list = [name[0] for name,model in tts_gal.items()]
        valid_names_list += valid_character_names_list
        meg = ""
        for name in valid_names_list:
            meg += f'{MessageSegment.text( f"{name},")}'
        await matcher.send(f"vits可用角色列表：\n{meg}")
    except:
        await matcher.send(f'获取vits角色列表失败')