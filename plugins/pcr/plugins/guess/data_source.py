import json
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[猜头像|猜卡面|猜角色|猜语音]
总之就是猜各种东西
看看谁又快又准吧
'''


class Guess(Service):
    def __init__(self):
        Service.__init__(self, "guess", __doc__, rule=is_in_service("guess"))
