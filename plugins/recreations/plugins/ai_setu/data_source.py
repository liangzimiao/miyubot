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
逗号分隔tag，%20为空格转义
tags 图片含有的要素，使用大括号{}括住某些tag来增加此tag的权重，括号越多权重越高如{{{loli}}}
&shape=Portrait/Landscape/Square 分别为竖图、横图、方图，默认竖图
&r18=1 默认0，不开,r18用的full模型，非r18则是另一个  
&scale=11 默认11，修改一下对scale的解释 虽然根据网页描述，scale和模型参与度，精细度都有关联，建议6-20 但实际表现上来看，低(6-8)饱和度低，偏线稿，线条偏杂乱，高(18-20)则饱和度偏高，偏CG风格,再高一点点也行，但容易过曝
&seed=1111111 随机生成不建议用，如果想在返回的原图上修改，在响应头或者图片文件流里找到seed 请注意seed一脉单传，seed不会变，不能完美倒退，但可以发和原来相同的tag和种子达到几乎一致的效果 
&strength，强度，可以理解为ai参与度，建议0-0.7，太多了千篇一律，太低和原图没什么区别，微调建议在0.4，大调可以拉高一些，默认0.4 
&noise，噪点增加细节，建议0-0.15，多了会出现奇怪的光斑，默认相对保守的0.12 
以图生图某种程度上弥补了风格没有强约束，觉得没什么用的建议传一张游戏立绘感受一下 
屏蔽词已默认：lowres,bad anatomy,bad hands,text,error,extra digit,fewer digits,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,username,bad body,bad proportions,gross proportions,missing fingers,missing arms,missing legs,extra fingers,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,mutation,deformed,blurry,ugly,duplicate,morbid,mutilated 
step写死28,shape三个尺寸为768*512（横图，适合带背景），512*768（竖图，适合人物），640*640（方图） 过滤器即k_euler_ancestal 
怎么找tag: 1.b站微博知乎贴吧推特，已经泛滥了，抄就对了 2.tag表找些群会有的 3.最简单的风格约束：在图站Danbooru里找张自己喜欢的图，把这张图所有tag复制下来
"""


class Ai_Draw(Service):
    def __init__(self):
        Service.__init__(self, "ai_draw", __doc__, rule=is_in_service("ai_draw"))

