from utils.service import Service
from utils.rule import is_in_service

__doc__ = """
要我一直[图片]吗
"""


class Yaowoyizhi(Service):
    def __init__(self):
        Service.__init__(self, "要我一直", __doc__, rule=is_in_service("要我一直"))
