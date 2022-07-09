from utils.service import Service
from utils.rule import is_in_service

__doc__ = """
[视频解析]
bilibili视频、番剧解析
私聊或群聊发送bilibili的小程序/链接
"""


class AnalysisBili(Service):
    def __init__(self):
        Service.__init__(self, "视频解析", __doc__, rule=is_in_service("视频解析"))
