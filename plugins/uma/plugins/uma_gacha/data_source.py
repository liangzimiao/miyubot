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
- [十连] 转蛋模拟
- [来发单抽] 转蛋模拟
- [来一井] 3w钻！
- [查看马娘卡池] 模拟卡池&出率
- [切换马娘卡池] 更换模拟卡池
- [更新卡池] 用于更新卡池
"""


class UmaGachaService(Service):
    def __init__(self):
        Service.__init__(self, "uma抽卡", __doc__, rule=is_in_service("uma抽卡"))

