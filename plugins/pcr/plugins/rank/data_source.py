import json
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[rank表]
公主连结的角色rank表
记得提醒我更新，，，
吐血( ๑ŏ ﹏ ŏ๑ )
'''


class Rank(Service):
    def __init__(self):
        Service.__init__(self, "rank表", __doc__, rule=is_in_service("rank表"))
