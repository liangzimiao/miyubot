import json
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[是谁？]
xx是谁？
为什么不问问神奇的魔法海螺呢？
'''


class UmaWhois(Service):
    def __init__(self):
        Service.__init__(self, "uma_whois", __doc__, rule=is_in_service("uma_whois"))
