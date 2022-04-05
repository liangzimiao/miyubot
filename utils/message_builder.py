from configs.path_config import IMAGE_PATH, VOICE_PATH
from nonebot.adapters.onebot.v11.message import MessageSegment
from typing import Union, List
from pathlib import Path
import os


def image(
    img_name: Union[str, Path] = None,
    path: str = None,
    abspath: str = None,
    b64: str = None,
) -> Union[MessageSegment, str]:
    """
    说明：
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数：
        :param img_name: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param abspath: 图片绝对路径
        :param b64: 图片base64
    """
    if abspath:
        return (
            MessageSegment.image("file:///" + abspath)
            if os.path.exists(abspath)
            else ""
        )
    elif isinstance(img_name, Path):
        if img_name.exists():
            return MessageSegment.image(f"file:///{img_name.absolute()}")
       # logger.warning(f"图片 {img_name.absolute()}缺失...")
        return ""
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if "http" in img_name:
            return MessageSegment.image(img_name)
        if len(img_name.split(".")) == 1:
            img_name += ".jpg"
        file = (
            Path(IMAGE_PATH) / path / img_name if path else Path(IMAGE_PATH) / img_name
        )
        if file.exists():
            return MessageSegment.image(f"file:///{file.absolute()}")
        else:
          #  logger.warning(f"图片 {file.absolute()}缺失...")
            return ""
