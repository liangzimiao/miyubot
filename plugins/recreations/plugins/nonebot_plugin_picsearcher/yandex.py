# -*- coding: utf-8 -*-
from typing import List, Tuple

import nonebot
from nonebot.adapters.onebot.v11 import MessageSegment
from lxml.html import fromstring
import aiohttp

"""
http://yandex.com/clck/jsredir?from=yandex.com%3Bimages%2Fsearch%3Bimages%3B%3B&text=&etext=9185.K4iyzsNBG9xrJrSJCUTF4i-XPMAfmBQYR_Igss1ESRc.65568e796f3375fae39da91273ae8a1a82410929&uuid=&state=iric5OQ0sS2054x1_o8yG9mmGMT8WeQxqpuwa4Ft4KVzd9aE_Y4Dfw,,&data=eEwyM2lDYU9Gd1VROE1ZMXhZYkJTYW5fZC1TWjIzaFh5TmR1Z09fQm5DdDB3bFJSSUpVdUxfZmUzcVhfaXhTN1BCU2dINGxmdkY4NFVNcHYyUmw0emFKT2pnOWJoVmlPVzAzX1FIbWh6aXVFV3F0YWFaMGdxeGFtY2dxTzFZZl9VY1huZmlLaGVGOFZleUthZXBlM1pxUGM2elVDLXdvZEo3OGJwdVFqYmVkTDJxWElHSzFZR2NVQUhVcTdzelJwSXlrTjhlS0txdHpYY1RMMHRLOU5HSTYtT0VDb0hpdll6YjVYRXNVcUhCRFJaeDExNTQwZlhMdjh4M2YtTVFUbVJ5ZzBxMTVJcG9DNW51UWhvRzE0WjlFS19uS0VUZWhNRGxOZWlPUkFlRUUs&sign=7ba9ee25d3716868ec8464fb766c9e25&keyno=IMGS_0&b64e=2&l10n=en
"""
headers = {
    'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'yandexuid=2273458361656492941; is_gdpr=0; is_gdpr_b=CNzDcxC7ew==; i=prCcpLvUQripdJTs5zAk5IpQguata8K8CtGTX8RhUgW4idEeKawiNEUTH5cZJCt9XWaV/rAwB/tmNTk5BnNovRPZFxo=; gdpr=0; _ym_uid=1626673628172262761; _ym_d=1656492946; _ym_isad=2; yuidss=2273458361656492941; ymex=1971853439.yrts.1656493439; yp=1657097744.szm.1:1920x1080:1920x969; _ym_visorc=b; _yasc=UTW244RCrUTiykaTec5U7rJ8k1qL9P6pCC29zIGSyxI+n7zNyIot9bRC7UE=; spravka=dD0xNjU2NDk1OTIyO2k9MTQwLjIyNy4xMjcuMjE5O0Q9QjlCOThBNjNGNEM2NjE4OTJCRjNBNjgxREExMDEyOUUzNEQ3QjE4MzEyQzZDODQyNTEzREZDMzhBQTMyMDQ5QTE0QjhFRTY4O3U9MTY1NjQ5NTkyMjk1NDI1OTE4NDtoPTM5NzQyOWFhZTY0MGI3MmYzMmM4NGJjZDU0OTBlNjlh; cycada=1isUOYn6Nnqpq/INGY4xkHMbxdShY6y7NvlYL/A9ydg=',
    #'Referer': 'https://yandex.com/images/search?rpt=imageview&url=https%3A%2F%2Favatars.mds.yandex.net%2Fget-images-cbir%2F1856503%2FJ1VOsD4XiZuZhba1KFurvA2998%2Forig&cbir_id=1856503%2FJ1VOsD4XiZuZhba1KFurvA2998',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.109 Safari/537.36 CrKey/1.54.248666 Edg/103.0.5060.53',
    'x-requested-with': 'XMLHttpRequest'}

driver = nonebot.get_driver()
proxy: str = getattr(driver.config, "proxy", None)


def parse_html(html: str):
    selector = fromstring(html)
    for item in selector.xpath('/html/body/div[3]/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/section/div[2]/div'):              
        pic_url = item.xpath('./div[1]/a/img/@src')  # 图床    
        if pic_url:
            pic_url = f"https:{pic_url[0]}"
            des = item.xpath('./div[2]/div[1]/a/text()')  # 简介
            if des:
                des=des[0]
            else :
                des="无"
            url = item.xpath('./div[2]/div[1]/a/@href')  # 链接
            if url:
                url=url[0]
            else :
                url="无"
            yield pic_url, des, url



async def get_pic_from_url(url: str):
    real_url = f"https://yandex.com/images/search?rpt=imageview&url={url}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url=real_url, headers=headers) as resp:
            html: str = await resp.text()
            #with open("yandex.html", "w", encoding="utf-8") as f:
            #    f.write(html)
        return [i for i in parse_html(html)]


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        msg: str = "yandex\n找不到高相似度的"
        yield msg
        return
    for pic in image_data:
        msg = MessageSegment.image(file=pic[0]) + f"yandex\n简介:{pic[1]}\n链接:{pic[2]}"
        #for i in pic[1:]:
        #    msg = msg + f"{i}\n"
        yield msg


if __name__ == "__main__":
    with open("yandex.html", "r", encoding="utf-8") as f:
        data = f.read()
    for item in parse_html(data):
        print(item)
