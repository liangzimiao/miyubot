# -*- coding: utf-8 -*-
"""
@Time    : 2022/3/17 16:30
@Author  : 物述有栖
@File    : create_img_simple.py
@DES     : 
"""
from PIL import Image, ImageDraw, ImageFont, ImageColor
from src.plugins.pcrgames import chara
import time
from pathlib import Path
import zhconv

path = Path(__file__).parent  # 获取文件所在目录的绝对路径
font_cn_path = str(path / 'fonts' / 'SourceHanSansCN-Medium.otf')  # Path是路径对象，必须转为str之后ImageFont才能读取
font_tw_path = str(path / 'fonts' / 'pcrtwfont.ttf')
server_name = 'bilibili官方服务器'  # 设置服务器名称


def _TraditionalToSimplified(hant_str: str):
    '''
    Function: 将 hant_str 由繁体转化为简体
    '''
    return zhconv.convert(str(hant_str), 'zh-hans')


def _generate_info_pic_internal_simple(data):
    '''
    个人资料卡生成
    '''
    im = Image.open(path / 'img' / 'template.png')  # 图片模板
    im_frame = Image.open(path / 'img' / 'frame.png')  # 头像框
    try:
        id_favorite = int(str(data['favorite_unit']['id'])[0:4])  # 截取第1位到第4位的字符
    except:
        id_favorite = 1000  # 一个？角色
    pic_dir = chara.fromid(id_favorite).icon.path
    user_avatar = Image.open(pic_dir)
    user_avatar = user_avatar.resize((90, 90))
    im.paste(user_avatar, (44, 150), mask=user_avatar)
    im_frame = im_frame.resize((100, 100))
    im.paste(im=im_frame, box=(39, 145), mask=im_frame)
    cn_font = ImageFont.truetype(font_cn_path, 18)  # Path是路径对象，必须转为str之后ImageFont才能读取
    font = cn_font  # 选择字体
    cn_font_resize = ImageFont.truetype(font_cn_path, 16)
    font_resize = cn_font_resize  # 选择字体
    draw = ImageDraw.Draw(im)
    font_black = (77, 76, 81, 255)
    # 资料卡 个人信息
    user_name_text = _TraditionalToSimplified(data["user_info"]["user_name"])
    user_comment_arr = _cut_str(_TraditionalToSimplified(
        data["user_info"]["user_comment"]), 25)
    for index, value in enumerate(user_comment_arr):
        draw.text((170, 310 + (index * 22)), value, font_black, font_resize)
    draw.text((34, 392), server_name, font_black, font_resize)

    arena_group_text = _TraditionalToSimplified(
        data["user_info"]["arena_group"])
    arena_time_text = _TraditionalToSimplified(time.strftime(
        "%Y/%m/%d", time.localtime(data["user_info"]["arena_time"])))
    arena_rank_text = _TraditionalToSimplified(data["user_info"]["arena_rank"])
    grand_arena_group_text = _TraditionalToSimplified(
        data["user_info"]["grand_arena_group"])
    grand_arena_time_text = _TraditionalToSimplified(time.strftime(
        "%Y/%m/%d", time.localtime(data["user_info"]["grand_arena_time"])))
    grand_arena_rank_text = _TraditionalToSimplified(
        data["user_info"]["grand_arena_rank"])
    w, h = font_resize.getsize(arena_time_text)
    draw.text((550 - w, 598), arena_time_text, font_black, font_resize)
    w, h = font_resize.getsize(arena_group_text + "场")
    draw.text((550 - w, 630), arena_group_text + "场", font_black, font_resize)
    w, h = font_resize.getsize(arena_rank_text + "名")
    draw.text((550 - w, 662), arena_rank_text + "名", font_black, font_resize)
    w, h = font_resize.getsize(grand_arena_time_text)
    draw.text((550 - w, 704), grand_arena_time_text, font_black, font_resize)
    w, h = font_resize.getsize(grand_arena_group_text + "场")
    draw.text((550 - w, 738), grand_arena_group_text + "场", font_black, font_resize)
    w, h = font_resize.getsize(grand_arena_rank_text + "名")
    draw.text((550 - w, 772), grand_arena_rank_text + "名", font_black, font_resize)

    unit_num_text = _TraditionalToSimplified(data["user_info"]["unit_num"])
    w, h = font_resize.getsize(unit_num_text)
    draw.text((550 - w, 844), unit_num_text, font_black, font_resize)

    viewer_id_arr = _cut_str(_TraditionalToSimplified(
        data["user_info"]["viewer_id"]), 3)

    w, h = font.getsize(
        viewer_id_arr[0] + "  " + viewer_id_arr[1] + "  " + viewer_id_arr[2])
    draw.text((138 + (460 - 138) / 2 - w / 2, 1058),
              viewer_id_arr[0] + "  " + viewer_id_arr[1] + "  " + viewer_id_arr[2], (255, 255, 255, 255), font)

    return im


def _cut_str(obj: str, sec: int):
    """
    按步长分割字符串
    """
    return [obj[i: i + sec] for i in range(0, len(obj), sec)]
