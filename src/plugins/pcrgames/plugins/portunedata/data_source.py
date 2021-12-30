import json
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[抽签|人品|运势|抽xcw签]
随机角色/指定凯露预测今日运势
准确率高达114.514%！
'''


class PortuneData(Service):
    def __init__(self):
        Service.__init__(self, "抽签", __doc__, rule=is_in_service("抽签"))
