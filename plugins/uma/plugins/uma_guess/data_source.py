import json
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[猜卡面]
猜马娘支援卡卡面的相关角色
答案以wiki数据为准以及部分别名
'''


class UmaGuess(Service):
    def __init__(self):
        Service.__init__(self, "uma_guess", __doc__, rule=is_in_service("uma_guess"))
