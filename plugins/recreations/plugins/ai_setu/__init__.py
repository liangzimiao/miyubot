# 2022.10.10 20:40


from distutils.log import error
from PIL import Image
from base64 import b64encode
from io import BytesIO
import re,json
from heapq import nsmallest
from . import youdao,db,config,limit
from nonebot.adapters.onebot.v11 import  MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import  CommandArg
from utils import get_event_gid,aiorequests, img_check, upload_oss
from .data_source import Ai_Draw
from utils.CD_Checker import check_cd


api_ip = config.api_ip
token = config.token
tags_moren = config.tags_moren



def process_tags(gid,uid,tags,add_db=config.add_db,trans=config.trans,limit_word=config.limit_word,arrange_tags=config.arrange_tags): #录入数据库，翻译，过滤屏蔽词，为1时开启
    error_msg ="" #报错信息
    tags_guolu="" #过滤词信息
    if add_db:
        try:
            msg = re.split('&',tags)[0]
            taglist = re.split(',|，',msg)
            while "" in taglist:
                taglist.remove("")#去除空元素
            for tag in taglist:
                db.add_xp_num(gid,uid,tag)
        except Exception as e:
            error_msg = "录入数据库失败"
    if trans:
        try:
            msg = re.split("([&])", tags ,1)
            msg[0] = youdao.tag_trans(msg[0])#有道翻译
            tags = "".join(msg)
        except Exception as e:
            error_msg = "翻译失败"
    if limit_word:
        try:
            tags,tags_guolu = limit.guolv(tags)#过滤屏蔽词
        except Exception as e:
            error_msg = "过滤屏蔽词失败"
    if arrange_tags:
        try:
            taglist = re.split(',|，',tags)
            while "" in taglist:
                taglist.remove("")#去除空元素
            tags = ",".join(taglist)
        except Exception as e:
            error_msg = "整理tags失败"
    return tags,error_msg,tags_guolu


async def process_img(data):
    error_msg ="" #报错信息
    imgmes=""
    msg=""
    try:
        msgdata = json.loads(re.findall('{"steps".+?}',str(data))[0])
        msg = f'\nseed:{msgdata["seed"]}   scale:{msgdata["scale"]}'
        img = Image.open(BytesIO(data)).convert("RGB")
        buffer = BytesIO()  # 创建缓存
        img.save(buffer, format="png")
        flag = await img_check.check(data)
        print(flag)
        if not flag : 
            imgme = 'base64://' + b64encode(buffer.getvalue()).decode()
            imgmes = f'{MessageSegment.image(imgme, cache=False, )}'
        else:
            file_name = str(msgdata["seed"])+".jpg"
            imgmes = upload_oss.upd.upload_file("3483623696",BytesIO(data).read(),file_name)
            print(imgmes)
    except Exception as e:
        error_msg = "处理图像失败"
    return msg,imgmes,error_msg

matcher = Ai_Draw().on_command("绘图","ai绘图" ,aliases={"ai绘图","aidraw","绘画","ai绘画"}, priority=5)


@matcher.handle()
async def special_title11(event: MessageEvent,args: Message = CommandArg()):
    await check_cd(matcher,event,__name__,cdTime=45)
    gid = get_event_gid(event)
    #gid = event.user_id
    uid = event.user_id
    tags = args.extract_plain_text() 
    tags,error_msg,tags_guolu=process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await matcher.send( f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolu):
        await matcher.send( f"已过滤：{tags_guolu}", at_sender=True)
    if not len(tags):
        tags = tags_moren
        await matcher.send( f"将使用默认tag：{tags_moren}", at_sender=True)
    try:
        url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
        response = await aiorequests.get(url, timeout = 45)
        data = await response.content
    except Exception as e:
        await matcher.finish(f"请求超时~", at_sender=True)

        
    msg,imgmes,error_msg = await process_img(data)
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
    #resultmes += f"\n tags:{tags}"
    resultmes  = imgmes
    await matcher.send( Message(resultmes+msg), at_sender=True)

matcher = Ai_Draw().on_command("以图绘图","ai绘图" ,aliases={"ai以图绘图","以画绘画"}, priority=5)

@matcher.handle()
async def img2img(event: MessageEvent,args: Message = CommandArg()):
    await check_cd(matcher,event,__name__,cdTime=45)
    gid = get_event_gid(event)
    uid = event.user_id
    tags = args.extract_plain_text() 
    tags,error_msg,tags_guolu=process_tags(gid,uid,tags) #tags处理过程
    if len(error_msg):
        await matcher.send( f"已报错：{error_msg}", at_sender=True)
    if len(tags_guolu):
        await matcher.send( f"已过滤：{tags_guolu}", at_sender=True)
    ret = re.search(r"\[CQ:image,file=(.*)?,url=(.*)\]", str(event.message))
    url = ret.group(2)
    print(url)
    if tags == "":
        #url = event.message[0]["data"]["url"]
        tags = tags_moren
        await matcher.send( f"将使用默认tag：{tags_moren}", at_sender=True)
    else:
        url = ret.group(2)
        #url = event.message[1]["data"]["url"]
    try:
        img_data = await aiorequests.get(url, timeout = 30)
        image = Image.open(BytesIO(await img_data.content))
        a,b = image.size
        c = a/b
        s = [0.6667,1.5,1]
        s1 =["Portrait","Landscape","Square"]
        shape=s1[s.index(nsmallest(1, s, key=lambda x: abs(x-c))[0])]#判断形状

        image = image.convert("RGB")
        #thumbSize = (768, 768)
        #image.thumbnail(thumbSize, resample=Image.ANTIALIAS)#用于压缩图片大小
        b_io = BytesIO()
        image.save(b_io, format="JPEG")
    except Exception as e:
        await matcher.finish( f"图片处理失败捏~", at_sender=True)
    try:
        response = await aiorequests.post(
            (f"http://{api_ip}/got_image2image") + (f"?tags={tags}") +(f"&shape={shape}")+ (f"&token={token}"),
            data=b64encode(b_io.getvalue()),
        )
        data = await response.content
    except Exception as e:
        await matcher.finish(f"请求超时~", at_sender=True)

    msg,imgmes,error_msg = await process_img(data)
    if len(error_msg):
        await matcher.finish( f"已报错：{error_msg}", at_sender=True)
    #resultmes += f"\n tags:{tags}"
    resultmes  = imgmes
    await matcher.send( Message(resultmes+msg), at_sender=True)

'''
@sv.on_fullmatch(['本群XP排行'])
async def get_group_xp(bot, ev):
    gid = ev.group_id
    xp_list = db.get_xp_list_group(gid)
    msg = '本群的XP排行榜为：\n'
    if len(xp_list)>0:
        for xpinfo in xp_list:
            keyword, num = xpinfo
            msg += f'关键词：{keyword}；次数：{num}\n'
    else:
        msg += '暂无本群的XP信息'
    await bot.send(ev, msg)

@sv.on_fullmatch(['个人XP排行'])
async def get_personal_xp(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    xp_list = db.get_xp_list_personal(gid,uid)
    msg = '本群的XP排行榜为：\n'
    if len(xp_list)>0:
        for xpinfo in xp_list:
            keyword, num = xpinfo
            msg += f'关键词：{keyword}；次数：{num}\n'
    else:
        msg += '暂无你在本群的XP信息'
    await bot.send(ev, msg)

@sv.on_fullmatch(['本群XP缝合'])
async def get_group_xp_pic(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    xp_list = db.get_xp_list_kwd_group(gid)
    msg = []
    if len(xp_list)>0:
        for xpinfo in xp_list:
            keyword = xpinfo
            msg.append(keyword)
        xp_tags = (',').join(str(x) for x in msg)
        tags = (',').join(str(x) for x in (re.findall(r"'(.+?)'",xp_tags)))
        tags,error_msg,tags_guolu=process_tags(gid,uid,tags,add_db=0,arrange_tags=0) #tags处理过程
        if len(error_msg):
            await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
        if len(tags_guolu):
            await bot.send(ev, f"已过滤：{tags_guolu}", at_sender=True)
        if not len(tags):
            tags = tags_moren
            await bot.send(ev, f"将使用默认tag：{tags_moren}", at_sender=True)
        try:
            url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
            response = await aiorequests.get(url, timeout = 30)
            data = await response.content
        except Exception as e:
            await bot.finish(ev, f"请求超时~", at_sender=True)
        msg,imgmes,error_msg = process_img(data)
        if len(error_msg):
            await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
        resultmes = f"[CQ:image,file={imgmes}]"
        resultmes += msg
        resultmes += f"\n tags:{tags}"
        await bot.send(ev, resultmes, at_sender=True)
    else:
        msg += '暂无本群的XP信息'

@sv.on_fullmatch(['个人XP缝合'])
async def get_personal_xp_pic(bot, ev):
    gid = ev.group_id
    uid = ev.user_id
    xp_list = db.get_xp_list_kwd_personal(gid,uid)
    msg = []
    if len(xp_list)>0:
        for xpinfo in xp_list:
            keyword = xpinfo
            msg.append(keyword)
        xp_tags = (',').join(str(x) for x in msg)
        tags = (',').join(str(x) for x in (re.findall(r"'(.+?)'",xp_tags)))
        tags,error_msg,tags_guolu=process_tags(gid,uid,tags,add_db=0,arrange_tags=0) #tags处理过程
        if len(error_msg):
            await bot.send(ev, f"已报错：{error_msg}", at_sender=True)
        if len(tags_guolu):
            await bot.send(ev, f"已过滤：{tags_guolu}", at_sender=True)
        if not len(tags):
            tags = tags_moren
            await bot.send(ev, f"将使用默认tag：{tags_moren}", at_sender=True)
        try:
            url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
            response = await aiorequests.get(url, timeout = 30)
            data = await response.content
        except Exception as e:
            await bot.finish(ev, f"请求超时~", at_sender=True)
        msg,imgmes,error_msg = process_img(data)
        if len(error_msg):
            await bot.finish(ev, f"已报错：{error_msg}", at_sender=True)
        resultmes = f"[CQ:image,file={imgmes}]"
        resultmes += msg
        resultmes += f"\n tags:{tags}"
        await bot.send(ev, resultmes, at_sender=True)
    else:
        msg += '暂无你在本群的XP信息'
'''