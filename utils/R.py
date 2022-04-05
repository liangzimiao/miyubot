import os
from urllib.parse import urljoin
from urllib.request import pathname2url
from nonebot import logger
from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image
from utils import pic2b64
import utils
from configs.path_config import PCR_PATH
# 当QQ客户端与bot端不在同一台计算机时，可用http协议
RES_PROTOCOL = 'file'
# 资源库文件夹，需可读可写，windows下注意反斜杠转义
RES_DIR = PCR_PATH
# 使用http协议时需填写，原则上该url应指向RES_DIR目录
RES_URL = 'http://127.0.0.1:5000/static/'


RES_DIR = os.path.expanduser(RES_DIR)
assert RES_PROTOCOL in ('http', 'file', 'base64')


class ResObj:
    def __init__(self, res_path):
        res_dir = os.path.expanduser(RES_DIR)
        fullpath = os.path.abspath(os.path.join(res_dir, res_path))
        if not fullpath.startswith(os.path.abspath(res_dir)):
            raise ValueError('Cannot access outside RESOUCE_DIR')
        self.__path = os.path.normpath(res_path)

    @property
    def url(self):
        """资源文件的url，供Onebot（或其他远程服务）使用"""
        return urljoin(RES_URL, pathname2url(self.__path))

    @property
    def path(self):
        """资源文件的路径，供Hoshino内部使用"""
        return os.path.join(RES_DIR, self.__path)

    @property
    def exist(self):
        return os.path.exists(self.path)


class ResImg(ResObj):
    @property
    def cqcode(self) -> MessageSegment:
        if RES_PROTOCOL == 'http':
            return MessageSegment.image(self.url)
        elif RES_PROTOCOL == 'file':
            return MessageSegment.image(f'file:///{os.path.abspath(self.path)}')
        else:
            try:
                return MessageSegment.image(utils.pic2b64(self.open()))
            except Exception as e:
                logger.exception(e)
                return MessageSegment.text('[图片出错]')

    def open(self) -> Image:
        try:
            return Image.open(self.path)
        except FileNotFoundError:
            logger.error(f'缺少图片资源：{self.path}')
            raise


def get(path, *paths):
    return ResObj(os.path.join(path, *paths))


def img(path, *paths):
    return ResImg(os.path.join('img', path, *paths))
