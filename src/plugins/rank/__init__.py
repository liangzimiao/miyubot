from nonebot import on_keyword
from nonebot.adapters.cqhttp.event import File, MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, MessageSegment, message,Message
from src.plugins.nonebot_guild_patch import GuildMessageEvent
from configs.path_config import IMAGE_PATH, PCR_PATH
from configs.path_config import GIF_PATH
from utils.message_builder import image
from pathlib import Path
from nonebot.permission import MESSAGE, SUPERUSER
from typing import Union, List
from nonebot.adapters.cqhttp.permission import GROUP, GROUP_OWNER, PRIVATE,GROUP_ADMIN
import os
import random
import os
import json
import random
import datetime    
matcher = on_command("万用表",  permission=SUPERUSER , priority=5)
@matcher.handle()
async def _(bot: Bot, event: Event,state: T_State):
        result = (
            "《简中服公会战&攻略情报万用表》 主页\n"
                "https://docs.qq.com/sheet/DWkdtR2djbnFiUGRk?tab=ltc6xo\n"

                "公会战一阶段\n"
                "https://docs.qq.com/sheet/DWmZlaUZjeUZCUUdV\n\n"
                        "公会战二阶段\n"
                "https://docs.qq.com/sheet/DWUpVT2RnZUNGbEJh?tab=BB08J2\n\n"
                "公会战三阶段\n"
                "https://docs.qq.com/sheet/DWlFaWmdSRW9Rb29S\n\n"

                "花舞轴区投稿\n"
                "https://docs.qq.com/form/page/DWUVIUnl1clpxSU5u\n"
            ) 
        await matcher.finish(result)

def get_json(qufu,zuozhe):
    current_dir = os.path.join(PCR_PATH, f'stable\{qufu}\{zuozhe}\config.json')
    file = open(current_dir, 'r', encoding = 'utf-8')
    config = json.load(file)
    return config

def get_qufu(rqufu: str):
        if rqufu  in ["国","国服","cn","CN","B","b","陆"]: 
                        qz=('cn','ffby')
        elif rqufu  in ["台","台服","tw","TW"]: 
                        qz=('tw','wy')
        elif rqufu  in ["日","日服","jp","JP"]: 
                        qz=('jp','sl')
        else:
                return
        return qz

matcher = on_command("/rank表", aliases={"/rank","/品级","rank表"} , priority=5)
@matcher.handle()
async def _(bot: Bot, event: MessageEvent,state: T_State):
        args = str(event.get_message()).strip() 
        if args:
                state["rqufu"] = args
@matcher.got("rqufu", prompt="你想查询哪个区服的rank表呢？")
async def handle_city(bot: Bot, event: MessageEvent, state: T_State):
    rqufu = state["rqufu"]
    if rqufu not in ["国","台","日","国服", "台服","日服","cn", "jp","tw","CN", "TW","JP","陆","b","B"]:
        await matcher.finish("你想查询的区服暂不支持，请重新输入！")
    qufu =  get_qufu(rqufu)[0]
    zuozhe= get_qufu(rqufu)[1]
    config = get_json(qufu,zuozhe)
    notice=config['notice']
    files=config['files']
    meg=''
    for file in files:
                f =open( os.path.join(PCR_PATH,  f'stable\{qufu}\{zuozhe}\{file}'),"rb")
                img= f.read()
                f.close()
                meg+=f'{MessageSegment.image(img ,cache=False,)}'
    await matcher.send(Message(notice + meg) ,at_sender=True)
                        
 
matcher = on_command("/千里眼" , priority=5)
@matcher.handle()
async def _(bot: Bot, event: Event,state: T_State):
        result = (
            "亿里眼·一之章\n bbs.nga.cn/read.php?tid=21317816\n\n亿里眼·二之章\n bbs.nga.cn/read.php?tid=25358671\n\n"
                

                "【日服千里眼 · 详细版】\n"
                "https://shimowendang.com/sheets/tXd93RkQQrhxwhXw/vfkB1\n\n"

                "【日服千里眼 · 粗略版】\n"
                "https://docs.qq.com/sheet/DYVFSWXhYQlZyU1Rn?tab=BB08J2\n"
            ) 
        await matcher.finish(result)
