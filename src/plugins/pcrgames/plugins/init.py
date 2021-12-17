# -*- coding: utf-8 -*-
"""
@Time    : 2021/12/16 15:04
@Author  : 物述有栖
@File    : __init__.py.py
@DES     : 
"""
from pathlib import Path
from nonebot import get_driver
import nonebot
from nonebot.config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "guess").
    resolve()))