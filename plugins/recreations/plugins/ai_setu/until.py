from base64 import b64encode
from io import BytesIO
import re,json
from heapq import nsmallest
#from hoshino import Service, priv
from utils import check_iamge, get_event_gid,aiorequests, img_check, upload_oss
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
import base64
import time,calendar
import re
import os
import math
from os.path import dirname, join, exists
from . import youdao,db,config
import ahocorasick
import uuid
import asyncio
from nonebot.adapters.onebot.v11 import  MessageSegment
from time import sleep
try:
    import hjson as json
except:
    import json

api_ip = config.api_ip
token = config.token
tags_moren = config.tags_moren
strength = config.strength
wordlist = config.wordlist
add_db=config.add_db
trans=config.trans
arrange_tags=config.arrange_tags
limit_word=config.limit_word
per_page_num = config.per_page_num
pic_super_url = config.pic_super_url
max_size = config.max_size
ip_token_list = config.ip_token_list#加载config

curpath = dirname(__file__)
save_image_path= join(curpath,'SaveImage')  # 保存图片路径
#font_path = join(curpath,"weiheijun.ttf")  #字体文件路径
if not exists(save_image_path):
    os.mkdir(save_image_path)


actree = ahocorasick.Automaton()#初始化AC自动机
for index, word in enumerate(wordlist):
    actree.add_word(word, (index, word))
actree.make_automaton() #初始化完成，一般来说重启才能重载屏蔽词


with open(join(curpath, 'magic.json'),encoding="utf-8") as f: #初始化法典
    magic_data = json.load(f)
magic_data_title = []
for i in magic_data:
    magic_data_title.append(i) #初始化法典目录


async def guolv(sent):#过滤屏蔽词
    sent_cp = sent.lower() #转为小写
    tags_guolv = ""
    for i in actree.iter(sent):
        sent_cp = sent_cp.replace(i[1][1], "")
        tags_guolv += str(i[1][1]) + " "
    return sent_cp,tags_guolv

async def process_tags(tags,trans=trans,limit_word=limit_word,arrange_tags=arrange_tags):
    error_msg ="" #报错信息
    tags_guolv="" #过滤词信息
    if not len(tags):
        return tags,error_msg,tags_guolv
    #初始化
    try:
        tags = f"tags={tags.strip().lower()}" #去除首尾空格换行#转小写#头部加上tags=
        taglist = re.split('&',tags) #分割
        id = ["tags=","ntags=","seed=","scale=","shape="]
        tag_dict = {x: "" for x in id} #初始化字典,结构为:tags+ntags+seed+scale+shape
        for i in id:
            tag_dict[i] = ("" if not [idx for idx in taglist if idx.startswith(i)] else [idx for idx in taglist if idx.startswith(i)][-1]).lstrip(i) #取出tags+ntags+seed+scale+shape,每种只取列表最后一个,并删掉id
    except Exception as e:
        error_msg += "tags初始化失败"
        return tags,error_msg,tags_guolv
    #翻译tags
    if trans:
        try:
            if tag_dict["ntags="]:
                tags2trans = tag_dict["tags="]+"&"+tag_dict["ntags="] # &作为分隔符
                tags2trans = await youdao.tag_trans(tags2trans) #翻译
                taglist1 = re.split('&',tags2trans)
                tag_dict["tags="] = taglist1[0]
                tag_dict["ntags="] = taglist1[1]
            else:
                tags2trans = tag_dict["tags="]
                tags2trans = await youdao.tag_trans(tags2trans) #翻译
                tag_dict["tags="] = tags2trans
        except Exception as e:
            error_msg += "翻译失败"
            return tags,error_msg,tags_guolv
    #过滤tags
    if limit_word:
        try:
            #过滤tags,只过滤正面tags
            tags2guolv = tag_dict["tags="]
            tags2guolv,tags_guolv = await guolv(tags2guolv)#过滤
            tag_dict["tags="] = tags2guolv
        except Exception as e:
            error_msg += "过滤失败"
            return tags,error_msg,tags_guolv
    #整理tags
    if arrange_tags:
        try:
            #整理tags,只整理正面tags
            id2tidy = ["tags=","ntags="]
            for i in id2tidy:
                tidylist = re.split(',|，',tag_dict[i])
                tidylist.remove("") if "" in tidylist else tidylist
                tag_dict[i] = ",".join(tidylist)
        except Exception as e:
            error_msg += f"整理失败{e}"
            return tags,error_msg,tags_guolv
    #整合tags
    tags = tag_dict["tags="]
    for i in id:
        if i != "tags=" and tag_dict[i]:
            tags += "&"+i+tag_dict[i]
    tags = tags.replace("landscape", "Landscape")
    tags = tags.replace("portrait", "Portrait")
    tags = tags.replace("square", "Square")
    return tags,error_msg,tags_guolv

async def retry_get_ip_token(i):
    if i < len(ip_token_list):
        api_ip,token = ip_token_list[i]
        i+=1
    return api_ip,token,i


async def get_imgdata(tags,way=1,shape="Portrait",strength=strength,b_io=None):#way=1时为get，way=0时为post
    error_msg =""  #报错信息
    resultmes = ""
    i = 0
    while i < len(ip_token_list):
        await asyncio.sleep(1) #防止过快
        i+=1
        print(f"第{i}次查询")
        api_ip,token,i = await retry_get_ip_token(i-1)
        try:
            if way:
                url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
                response = await aiorequests.get(url, timeout=180)
            else:
                url = (f"http://{api_ip}/got_image2image") + (f"?tags={tags}") +(f"&shape={shape}")+(f"&strength={strength}")+(f"&token={token}")
                response = await aiorequests.post(url,data=b64encode(b_io.getvalue()), timeout=180)
            imgdata = await response.content
            if len(imgdata) < 5000:
                error_msg = "token冷却中~"
                continue
        except Exception as e:
            i+=1
            sleep(1)
            error_msg = f"超时了~"
            continue
        i=999
        error_msg = ""
    try:
        msg=""
        msgdata = json.loads(re.findall('{"steps".+?}',str(imgdata))[0])
        #msg = f'\nseed:{msgdata["seed"]}   scale:{msgdata["scale"]}'
    except Exception as e:
        error_msg = f"获取图片信息失败"
        return resultmes,error_msg

    flag = await img_check.check(imgdata)
    flag2,value = await check_iamge.porn_pic_index(base64.b64encode(imgdata))
    try:
        print(bool(flag or flag2))
        if bool(flag or flag2):
            file_name = str(msgdata["seed"])+".jpg"
            imgmes = upload_oss.upd.upload_file("3483623696",BytesIO(imgdata).read(),file_name)
            print(imgmes)
        else:
            img = Image.open(BytesIO(imgdata)).convert("RGB")
            buffer = BytesIO()  # 创建缓存
            img.save(buffer, format="png")
            imgme = 'base64://' + b64encode(buffer.getvalue()).decode()
            imgmes = f'{MessageSegment.image(imgme, cache=False, )}'
        msg = f'\nseed:{msgdata["seed"]}   分数:{value}'
    except Exception as e:
        error_msg += "处理图像失败{e}"
        return resultmes,error_msg
    resultmes = imgmes + msg
    return resultmes,error_msg


async def get_pic_d(msg):
    error_msg = ""  # 报错信息
    b_io = ""
    shape = "Portrait"
    size = 0
    try:
        image_url = re.search(r"\[CQ:image,file=(.*)url=(.*?)[,|\]]", str(msg))
        url = image_url.group(2)
    except Exception as e:
        error_msg = "你的图片呢？"
        return b_io,shape,error_msg,size
    try:
        img_data = await aiorequests.get(url)
        image = Image.open(BytesIO(await img_data.content))
        a,b = image.size
        size = a*b
        c = a/b
        s = [0.6667,1.5,1]
        s1 =["Portrait","Landscape","Square"]
        shape=s1[s.index(nsmallest(1, s, key=lambda x: abs(x-c))[0])]#判断形状
        image = image.convert("RGB")
        b_io = BytesIO()
        image.save(b_io, format="JPEG")

    except Exception as e:
        error_msg = "图片处理失败" # 报错信息
        return b_io,shape,error_msg,size
    return b_io,shape,error_msg,size


async def fetch_data_pic_super(_hash):
    i = 0
    url_status = f'https://hf.space/embed/{pic_super_url}/api/queue/status/'
    while True:
        resj =  await (await aiorequests.post(url_status, json={'hash': _hash})).json()
        if resj['status'] == 'PENDING':
            sleep(1)
            i+=1
            if i > 120:
                raise IOError(f'超时了捏~')
            else:
                continue
        elif resj['status'] == 'COMPLETE':
            return resj['data']['data'][0].split("base64,")[1]
        else:
            raise IOError(f'生成失败')

async def get_pic_super_(b_io,msg,size):
    error_msg = ""
    resultmes = ""
    if size > max_size:
        error_msg = "图片这么大，进不去拉~"
        return resultmes,error_msg
    try:
        if "2倍超分" in msg:
            scale = 2
        elif "3倍超分" in msg:
            scale = 3
        elif "4倍超分" in msg:
            scale = 4
        else:
            scale = 2
        if "保守降噪" in msg:
            con = "conservative"
        elif "降噪" in msg:
            con = "denoise3x"
        else:
            con = "no-denoise"
        modelname = f"up{scale}x-latest-{con}.pth"
    except Exception as e:
        error_msg += "超分参数错误"
        return resultmes,error_msg
    try:
        url_push = f'https://hf.space/embed/{pic_super_url}/api/queue/push/'
        jsons = {
            "fn_index": 0,
            "data": json.dump("data:image/jpeg;base64," + base64.b64encode(b_io.getvalue()).decode(),modelname,2),
            "session_hash": str(uuid.uuid1()),
            "action": "predict"
        }

        _hash = (await (await aiorequests.post(url_push, json=jsons)).json())['hash']
        a = await fetch_data_pic_super(_hash)
        imgmes = 'base64://' + a
        resultmes = f"[CQ:image,file={imgmes}]"
    except Exception as e:
        error_msg += f"错误原因{e}"
        print(e)
        return resultmes,error_msg
    return resultmes,error_msg

async def img2tags_(b_io):
    error_msg = ""
    resultmes = ""
    try:
        url_push = 'https://hf.space/embed/hysts/DeepDanbooru/api/queue/push/'
        json = {
            "fn_index": 0,
            "data": ["data:image/jpeg;base64," + base64.b64encode(b_io.getvalue()).decode(),0.7],
            "session_hash": str(uuid.uuid1()),
            "action": "predict"
        }
        _hash = (await(await aiorequests.post(url_push, json=json)).json())['hash']
        resj = await fetch_data_tags(_hash)
        resultmes = ','.join([f'{i["label"]}' for i in resj]).replace("rating:safe,","")
        resultmes = f"\n鉴赏出的tags有:{resultmes}"
    except Exception as e:
        error_msg = f"鉴赏失败{e}"
        return resultmes,error_msg
    return resultmes,error_msg


async def fetch_data_tags(_hash):
    i = 0 #初始化最大时间
    url_status = 'https://hf.space/embed/hysts/DeepDanbooru/api/queue/status/'
    while 1:
        resj = await (await aiorequests.post(url_status, json={'hash': _hash})).json()
        if resj['status'] == 'PENDING':
            sleep(1)
            i+=1
            if i > 10:
                raise IOError(f'超时了捏~')
            else:
                continue
        elif resj['status'] == 'COMPLETE':
            return resj['data']['data'][0]['confidences']
        else:
            raise IOError('status error')

async def get_magic_book_(msg):
    error_msg = ""
    resultmes = ""
    if msg in magic_data_title:
        resultmes = magic_data[msg]["tags"] +"&ntags="+magic_data[msg]["ntags"] +"&shape=Landscape"
        return resultmes,error_msg
    else:
        error_msg = "没有这条魔咒"
        return resultmes,error_msg

async def get_imgdata_magic(tags):#way=1时为get，way=0时为post
    error_msg =""  #报错信息
    resultmes = ""
    i = 0
    while i < len(ip_token_list):
        print(f"第{i}次查询")
        api_ip,token,i = await retry_get_ip_token(i)
        try:
            url = (f"http://{api_ip}/got_image") + (f"?tags={tags}")+ (f"&token={token}")
            response = await aiorequests.get(url, timeout=180)
            imgdata = await response.content
        except Exception as e:
            i+=1
            sleep(1)
            error_msg = f"超时了~"
            continue
        try:
            msgdata = json.loads(re.findall('{"steps".+?}',str(imgdata))[0])
            msg = f'\nseed:{msgdata["seed"]}   scale:{msgdata["scale"]}'
        except Exception as e:
            i+=1
            sleep(1)
            error_msg = f"token冷却中~"
            continue
        i=999
        error_msg = ""
        flag = await img_check.check(imgdata)
        flag2,value = await check_iamge.porn_pic_index(base64.b64encode(imgdata))
    try:
        print(bool(flag or flag2))
        if bool(flag or flag2):
            file_name = str(msgdata["seed"])+".jpg"
            imgmes = upload_oss.upd.upload_file("3483623696",BytesIO(imgdata).read(),file_name)
            print(imgmes)
        else:
            img = Image.open(BytesIO(imgdata)).convert("RGB")
            buffer = BytesIO()  # 创建缓存
            img.save(buffer, format="png")
            imgme = 'base64://' + b64encode(buffer.getvalue()).decode()
            imgmes = f'{MessageSegment.image(imgme, cache=False, )}'
        msg = f'\nseed:{msgdata["seed"]}   分数:{value}'
    except Exception as e:
        error_msg += "处理图像失败{e}"
        return resultmes,error_msg
    resultmes = imgmes + msg
    return resultmes,error_msg