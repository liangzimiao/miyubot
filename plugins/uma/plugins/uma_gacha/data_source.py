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
- [马娘/支援卡十连] 转蛋模拟
- [马娘/支援卡单抽] 转蛋模拟
- [马娘/支援卡一井] 3w钻！
- [查看马娘卡池] 模拟卡池
"""


class UmaGachaService(Service):
    def __init__(self):
        Service.__init__(self, "uma_gacha", __doc__, rule=is_in_service("uma_gacha"))

