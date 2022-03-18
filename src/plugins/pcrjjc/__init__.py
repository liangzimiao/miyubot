from pathlib import Path
from nonebot import get_driver
import nonebot
from .config import Config
import os
import sqlite3
import requests
import json

global_config = get_driver().config
config = Config(**global_config.dict())

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins/").
        resolve()))
# _sub_plugins = set()
# _sub_plugins |= nonebot.load_plugins(
#     str((Path(__file__).parent / "plugins/guess").
#         resolve()))
# _sub_plugins = set()
# _sub_plugins |= nonebot.load_plugins(
#     str((Path(__file__).parent / "plugins/gacha").
#         resolve()))
