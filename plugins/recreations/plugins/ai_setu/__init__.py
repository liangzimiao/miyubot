# 2022.10.10 20:40


import base64
from distutils.log import error
from PIL import Image
from base64 import b64encode
from io import BytesIO
import re,json
from heapq import nsmallest
from . import youdao,db,config,limit,until
from nonebot.adapters.onebot.v11 import  MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import  CommandArg
from utils import check_iamge, get_event_gid,aiorequests, img_check, upload_oss
from .data_source import Ai_Draw
from utils.CD_Checker import check_cd



tags_moren = config.tags_moren
picsuper = config.picsuper



matcher = Ai_Draw().on_command("绘图","ai绘图" ,aliases={"ai绘图","ai_draw","绘画","ai绘画"}, priority=5)


@matcher.handle()
async def text2img(event: MessageEvent,args: Message = CommandArg()):
    await check_cd(matcher,event,__name__,cdTime=60)
    gid = get_event_gid(event)
    #gid = event.user_id
    uid = event.user_id
    tags = args.extract_plain_text() 
    tags,error_msg,tags_guolv=await until.process_tags(tags)
    if len(error_msg):
        await matcher.send( f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await matcher.send( f"已过滤：{tags_guolv}", at_sender=True)
    if not len(tags):
        tags = tags_moren
        await matcher.send( f"将使用默认tag：{tags_moren}", at_sender=True)
    resultmes,error_msg = await until.get_imgdata(tags)
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
        #resultmes = f"[CQ:reply,id={ev.message_id}]{resultmes}"     #回复形式发送
    await matcher.send( Message(resultmes), at_sender=True)
    

matcher = Ai_Draw().on_command("以图绘图","ai绘图" ,aliases={"ai以图绘图","以画绘画","以图生图"}, priority=5)

@matcher.handle()
async def img2img(event: MessageEvent,args: Message = CommandArg()):
    await check_cd(matcher,event,__name__,cdTime=60)
    gid = get_event_gid(event)
    uid = event.user_id
    tags = args.extract_plain_text() 
    print(f"!!{tags}!!")
    if event.message[0].type == "reply":
        tmsg = await event.get_message(message_id=int(event.message[0].data['id']))
        event.message = tmsg["message"]
    b_io,shape,error_msg,size = await until.get_pic_d(event.message)  #图片获取过程
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
    tags,error_msg,tags_guolv=await until.process_tags(tags)
    if len(error_msg):
        await matcher.send( f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolv):
        await matcher.send( f"已过滤：{tags_guolv}", at_sender=True)
    if not len(tags):
        tags = tags_moren
        await matcher.send( f"将使用默认tag：{tags_moren}", at_sender=True)
    resultmes,error_msg = await until.get_imgdata(tags,way=0,shape=shape,b_io=b_io)
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
        #resultmes = f"[CQ:reply,id={ev.message_id}]{resultmes}"     #回复形式发送
    await matcher.send( Message(resultmes), at_sender=True)




    if bool(event.reply):
        tmsg = event.reply.message
        print(tmsg)
        event.message = tmsg["message"]
    b_io,shape,error_msg,size = await until.get_pic_d(event.message)
    if len(error_msg):
        await matcher.finish(f"已报错：{error_msg}", at_sender=True)
    resultmes,error_msg = await until.img2tags_(b_io)
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
    await matcher.send(resultmes, at_sender=True)