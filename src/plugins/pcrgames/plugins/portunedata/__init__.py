# -*- coding: utf-8 -*-
"""
@Time    : 2021/12/16 15:04
@Author  : 物述有栖
@File    : __init__.py.py
@DES     :
"""
import os
import random

from PIL import Image, ImageDraw, ImageFont
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent

from utils import DailyNumberLimiter, pic2b64
from utils import R
from .data_source import PortuneData
from .luck_desc import luck_desc
from .luck_type import luck_type

lmt = DailyNumberLimiter(1)
# 设置每日抽签的次数，默认为1
Data_Path = R.RES_DIR
# 也可以直接填写为res文件夹所在位置，例：absPath = "C:/res/"
Img_Path = 'portunedata/imgbase'


def drawing_pic(model) -> Image:
    fontPath = {
        'title': R.img('portunedata/font/Mamelon.otf').path,
        'text': R.img('portunedata/font/sakura.ttf').path
    }

    if model == 'xcw':
        base_img = get_base_by_name("frame_28.jpg")
    else:
        base_img = get_base_by_name("frame_" + str(random.randint(1, 66)) + ".jpg")

    filename = os.path.basename(base_img.path)
    charaid = filename.lstrip('frame_')
    charaid = charaid.rstrip('.jpg')

    img = base_img.open()
    # Draw title
    draw = ImageDraw.Draw(img)
    text, title = get_info(charaid)

    text = text['content']
    font_size = 45
    color = '#F5F5F5'
    image_font_center = (140, 99)
    ttfront = ImageFont.truetype(fontPath['title'], font_size)
    font_length = ttfront.getsize(title)
    draw.text((image_font_center[0] - font_length[0] / 2, image_font_center[1] - font_length[1] / 2),
              title, fill=color, font=ttfront)
    # Text rendering
    font_size = 25
    color = '#323232'
    image_font_center = [140, 297]
    ttfront = ImageFont.truetype(fontPath['text'], font_size)
    result = decrement(text)
    if not result[0]:
        return Exception('Unknown error in daily luck')
    textVertical = []
    for i in range(0, result[0]):
        font_height = len(result[i + 1]) * (font_size + 4)
        textVertical = vertical(result[i + 1])
        x = int(image_font_center[0] + (result[0] - 2) * font_size / 2 +
                (result[0] - 1) * 4 - i * (font_size + 4))
        y = int(image_font_center[1] - font_height / 2)
        draw.text((x, y), textVertical, fill=color, font=ttfront)

    img = pic2b64(img)
    img = MessageSegment.image(img)
    return img


def get_base_by_name(filename) -> R.ResImg:
    return R.img(os.path.join(Img_Path, filename))


def random_Basemap() -> R.ResImg:
    base_dir = R.img(Img_Path).path
    random_img = random.choice(os.listdir(base_dir))
    return R.img(os.path.join(Img_Path, random_img))


def get_info(charaid):
    for i in luck_desc:
        if charaid in i['charaid']:
            typewords = i['type']
            desc = random.choice(typewords)
            return desc, get_luck_type(desc)
    raise Exception('luck description not found')


def get_luck_type(desc):
    target_luck_type = desc['good-luck']
    for i in luck_type:
        if i['good-luck'] == target_luck_type:
            return i['name']
    raise Exception('luck type not found')


def decrement(text):
    length = len(text)
    result = []
    cardinality = 9
    if length > 4 * cardinality:
        return [False]
    numberOfSlices = 1
    while length > cardinality:
        numberOfSlices += 1
        length -= cardinality
    result.append(numberOfSlices)
    # Optimize for two columns
    space = ' '
    length = len(text)
    if numberOfSlices == 2:
        if length % 2 == 0:
            # even
            fillIn = space * int(9 - length / 2)
            return [numberOfSlices, text[:int(length / 2)] + fillIn, fillIn + text[int(length / 2):]]
        else:
            # odd number
            fillIn = space * int(9 - (length + 1) / 2)
            return [numberOfSlices, text[:int((length + 1) / 2)] + fillIn,
                    fillIn + space + text[int((length + 1) / 2):]]
    for i in range(0, numberOfSlices):
        if i == numberOfSlices - 1 or numberOfSlices == 1:
            result.append(text[i * cardinality:])
        else:
            result.append(text[i * cardinality:(i + 1) * cardinality])
    return result


def vertical(str):
    list = []
    for s in str:
        list.append(s)
    return '\n'.join(list)


pcr_portune = PortuneData().on_command("抽签", "抽签", aliases={'人品', '运势'}, priority=5)


@pcr_portune.handle()
async def portune(bot, event: MessageEvent):
    args = str(event.get_message()).strip()
    if args:
        return
    # if not lmt.check(uid):
    # await bot.finish(ev, f'你今天已经抽过签了，欢迎明天再来~', at_sender=True)
    # lmt.increase(uid)
    model = 'DEFAULT'
    pic = drawing_pic(model)
    await pcr_portune.send(pic, at_sender=True)


xcw_portune = PortuneData().on_keyword({'抽镜华签', '抽小仓唯签', '抽xcw签', '抽露娜签'}, "抽特定签")


@xcw_portune.handle()
async def portune_kyaru(bot, event: GuildMessageEvent):
    # uid = ev.user_id
    # if not lmt.check(uid):
    #   await bot.finish(ev, f'你今天已经抽过签了，欢迎明天再来~', at_sender=True)
    # lmt.increase(uid)
    model = 'xcw'
    pic = drawing_pic(model)
    await xcw_portune.send(pic, at_sender=True)
