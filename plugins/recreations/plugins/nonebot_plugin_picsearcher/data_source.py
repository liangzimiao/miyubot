# -*- coding: utf-8 -*-

from utils.service import Service
from utils.rule import is_in_service
__doc__ = """
- [搜图] 
"""


class   PicSearcherService(Service):
    def __init__(self):
        Service.__init__(self, "搜图", __doc__, rule=is_in_service("搜图"))

