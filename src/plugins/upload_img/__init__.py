from io import BytesIO
import json
from PIL import Image
from nonebot.adapters.cqhttp.event import File, MessageEvent
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot, MessageSegment
from pydantic.networks import url_regex
import requests
from configs.path_config import IMAGE_PATH, PCR_PATH
from utils.message_builder import image
from nonebot.permission import SUPERUSER
import os
import re
import filetype
upload_img = on_command("上传图片",  permission=SUPERUSER , priority=5)
@upload_img.handle()
async def _(bot: Bot, event: Event,state: T_State):
        args = str(event.get_message()).strip() 
        if args:
                state["path"] = args
        else:
                dir_path = os.path.join(os.path.expanduser(IMAGE_PATH))
                files = os.listdir(dir_path)
                await upload_img.send(f"{files}")
                
@upload_img.got("path", prompt="你想上传到哪个图库呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        path = state["path"]
        dir_path = os.path.join(os.path.expanduser(IMAGE_PATH))
        files = os.listdir(dir_path)
        if path not in files:
                await upload_img.finish("你想上传的图库不存在，请重新输入！")

@upload_img.got("img_name", prompt="图片命名为?")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        img_name=state["img_name"]
        print(img_name)

@upload_img.got("img", prompt="图片呢")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):    
        img = state["img"]
        img_name= state["img_name"] 
        path=os.path.join(os.path.expanduser(IMAGE_PATH),f'{state["path"]}')
        ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", img)
        url = ret.group(2)
        print(url)
        mes=upload_images(url,img_name,path)
        await upload_img.send( mes)

def upload_images(url,img_name,path):
        try:
                rep = requests.get(url,timeout=10)
                content = rep.content
                try:
                        extension = filetype.guess_mime(content).split('/')[1]
                        abs_path = os.path.join(path, f'{img_name}.{extension}')
                        if 200 == rep.status_code:
                                f = Image.open(BytesIO(rep.content))
                                f.save(abs_path)
                                return f"图片上传成功"
                        else:
                                return f"图片上传失败"
                except:
                        return f'不是有效文件类型'
                
        except:
                return f"图片下载超时"




upload_img = on_command("上传rank图片",  permission=SUPERUSER , priority=5)
@upload_img.handle()
async def _(bot: Bot, event: Event,state: T_State):
        args = str(event.get_message()).strip() 
        if args:
                state["path"] = args
        else:
                dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable")
                files = os.listdir(dir_path)
                await upload_img.send(f"{files}")        
@upload_img.got("qf", prompt="你想上传哪个区服rank图呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        path = state["qf"]
        dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable")
        files = os.listdir(dir_path)
        if path not in files:
                await upload_img.finish("你想上传的区服不存在，请重新输入！")
        else:
                dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable",f'{path}')
                files = os.listdir(dir_path)
                await upload_img.send(f"{files}")
@upload_img.got("zz", prompt="你想上传哪个作者rank图呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        zz=state["zz"]
        print(zz)
@upload_img.got("img_name", prompt="图片命名为?(例如15-4_1)")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        img_name=state["img_name"]
        print(img_name)
@upload_img.got("img", prompt="图片呢")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):    
        img = state["img"]
        img_name= state["img_name"] 
        path=os.path.join(os.path.expanduser(PCR_PATH),"stable",f'{state["qf"]}',f'{state["zz"]}')
        ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", img)
        url = ret.group(2)
        print(url)
        mes=upload_images(url,img_name,path)
        await upload_img.send( mes)



rank_= on_command("修改rank图片",  permission=SUPERUSER , priority=5)
@rank_.handle()
async def _(bot: Bot, event: Event,state: T_State):
        dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable")
        files = os.listdir(dir_path)
        await rank_.send(f"{files}")
@rank_.got("qf", prompt="你想修改哪个区服rank图呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State): 
        qf=state["qf"]
        dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable",f'{qf}')
        files = os.listdir(dir_path)
        await rank_.send(f"{files}")
@rank_.got("zz", prompt="你想修改哪个作者rank图呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        pass

dict = {}

@rank_.got("files", prompt="你想修改内容为什么呢？")
async def handle_(bot: Bot, event: MessageEvent, state: T_State):
        dir_path = os.path.join(os.path.expanduser(PCR_PATH),"stable",f'{state["qf"]}',f'{state["zz"]}')
        path = os.path.join(dir_path, 'config.json')
        with open(path, 'rb') as f:
                params = json.load(f)
                print(params)
                #await rank_.send(params['files'])
                params['files']=list(state["files"])
                print(state['files'])
                print(params['files'])
                print(params)
                dict = params
        f.close()
        with open(path, 'w') as r:
                json.dump(dict, r)
        r.close()
        await rank_.finish("修改完成")