from utils.service import Service
from utils.rule import is_in_service

__doc__ = """
[超级分辨率]
使用方法很简单，首先输入[超分，重建, 清晰术, real-esrgan, 超分辨率重建, esrgan, real_esrgan]中的任意一个来启动插件。

然后输入[anime, base]中的一个来作为重建的类型，其中base相对适用于一般图片，而anime则对二刺螈图比较好，但也不绝对。

不输入默认 anime 模式

最后发送一张图片即可，但不能以文件形式发送。
"""


class RealESRGAN(Service):
    def __init__(self):
        Service.__init__(self, "超级分辨率", __doc__, rule=is_in_service("超级分辨率"))
