import json
import os
from nonebot.params import  CommandArg
from nonebot.params import State
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Message
from nonebot.plugin import on_command,on_regex
from nonebot.adapters.onebot.v11.event import MessageEvent
from .data_source import Rank

from nonebot.adapters.onebot.v11 import  MessageSegment





def get_json(service):

    current_dir = os.path.expanduser(f"resources\pcr\\rank\{service}\config.json")
    file = open(current_dir, 'r', encoding='utf-8')
    config = json.load(file)
    return config


def get_service(service_name: str):
    if service_name in ["国", "国服", "cn", "CN", "B", "b", "陆","陆服","b服", "B服"]:
        service = ('cn')
    elif service_name in ["台", "台服", "tw", "TW"]:
        service = ('tw')
    elif service_name in ["日", "日服", "jp", "JP"]:
        service = ('jp')
    else:
        return
    return service


matcher = Rank().on_command("/rank表","rank表",aliases={"/rank", "/品级", "rank表","rank","Rank表","/Rank"}, priority=5)


@matcher.handle()
async def _(bot: Bot, args: Message = CommandArg(), state: T_State = State()):
    plain_text = args.extract_plain_text() 
    print(plain_text) 
    if plain_text:
        state["serivce"] = plain_text
 

@matcher.got("serivce", prompt="你想查询哪个区服的rank表呢？\n国服\n台服\n日服")
async def handle_serivce(bot: Bot,state: T_State = State()):

    service_name=str(state["serivce"])
    print(service_name)
    if len(service_name)>2:
        return  
    if service_name not in ["国", "台", "日", "国服", "台服", "日服", "cn", "jp", "tw", "CN", "TW", "JP", "陆","陆服", "b", "B"]:
        await matcher.finish("你想查询的区服暂不支持，请重新输入！")

    service=get_service(service_name)
    config = get_json(service)
    print(service)
    notice = config['notice']
    files = config['files']
    meg = ''
    for file in files:
        f = open(os.path.expanduser(f"resources\pcr\\rank\{service}\{file}"), "rb")
        img = f.read()
        f.close()
        meg += f'{MessageSegment.image(img, cache=False, )}'
    await matcher.send(Message(notice + meg), at_sender=True)


matcher2 =Rank().on_regex(r'^([陆国日台Bb][服]|[陆国日台Bb])[Rr]ank(表)?',"rank表", priority=5)


@matcher2.handle()
async def _(bot: Bot, event: MessageEvent):

    plain_text = event.get_plaintext()
    service_name = plain_text.split("r", 1)[0]
    if  service_name == plain_text:
        service_name = plain_text.split("R", 1)[0]
    if len(service_name)>2:
        return
    if service_name not in ["国", "台", "日", "国服", "台服", "日服", "cn", "jp", "tw", "CN", "TW", "JP", "陆","陆服", "b", "B" "b服", "B服"]:
        await matcher2.finish("你想查询的区服暂不支持，请重新输入！")
    service=get_service(service_name)
    config = get_json(service)
    print(service)
    notice = config['notice']
    files = config['files']
    meg = ''
    for file in files:
        f = open(os.path.expanduser(f"resources\pcr\\rank\{service}\{file}"), "rb")
        img = f.read()
        f.close()
        meg += f'{MessageSegment.image(img, cache=False, )}'
        
    await matcher2.send(Message(notice + meg), at_sender=True)
        

