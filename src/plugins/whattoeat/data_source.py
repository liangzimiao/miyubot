from utils.service import Service
from utils.rule import is_in_service

__doc__ = """
r'^(今天|[早中午晚][上饭餐午]|夜宵)吃(什么|啥|点啥)'
"""


class WhatToEat(Service):
    def __init__(self):
        Service.__init__(self, "吃啥", __doc__, rule=is_in_service("吃啥"))
