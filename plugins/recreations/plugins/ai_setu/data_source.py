# -*- coding: utf-8 -*-
"""
@Time    : 2021/12/29 11:30
@Author  : 物述有栖
@File    : data_source.py
@DES     : 
"""
from utils.service import Service
from utils.rule import is_in_service
__doc__ = """
主要功能：
【绘图 XXX】
【以图绘图 XXX 图片】

【绘图各参数指南】
规范：绘图 <tags>[&shape=Portrait/Landscape/Square|&scale=11|&seed=1234]
例如：绘图 loli,xcw&shape=Portrait&scale=24
<tags>为必选参,逗号分隔tag,%20为空格转义,加0代表增加权重,可以加很多个,可直接英语句子
[ ]为可选参数，其中：
tags 图片含有的要素，使用大括号{}括住某些tag来增加此tag的权重，括号越多权重越高如{{{loli}}}
shape 分别为竖图、横图、方图，默认竖图
scale 默认11,只建议11-24,细节会提高,太高了会过曝
seed 随机种子，任意数字。相同的种子可能会有相同的结果
"""


class Ai_Draw(Service):
    def __init__(self):
        Service.__init__(self, "ai_draw", __doc__, rule=is_in_service("ai_draw"))

