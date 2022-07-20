from utils.service import Service
from utils.rule import is_in_service

__doc__ = """
[搜图]
搜图
搜图指令后加图片/对图片回复搜图
"""


class PicSearch(Service):
    def __init__(self):
        Service.__init__(self, "搜图", __doc__, rule=is_in_service("搜图"))
