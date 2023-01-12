import asyncio
import base64
import html
import json
import math
import os
import random
import re
import string
import time
import traceback
from io import BytesIO
from nonebot.permission import SUPERUSER
import aiohttp
import feedparser
from PIL import Image
from nonebot import get_driver
from nonebot import logger
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message,MessageSegment
from nonebot_plugin_apscheduler import scheduler
from nonebot.adapters.onebot.v11.event import MessageEvent
from utils import send_guild_message, get_event_gid
from utils.base_config import BotInfo
rss_news = {}
data = {
    'rsshub': 'http://127.0.0.1:1201',
    'proxy': '',
    'proxy_urls': [],
    'last_time': {},
    'guild_rss': {},
    'guild_mode': {},
}
HELP_MSG = '''rss订阅
rss list : 查看订阅列表
rss add rss地址 : 添加rss订阅
rss addb up主id : 添加b站up主订阅
rss addr route : 添加rsshub route订阅
rss remove 序号 : 删除订阅列表指定项
rss mode 0/1 : 设置消息模式 标准/简略
详细说明见项目主页: https://github.com/zyujs/rss
'''


def save_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    try:
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        traceback.print_exc()


def load_data():
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    if not os.path.exists(path):
        save_data()
        return
    try:
        with open(path, encoding='utf8') as f:
            d = json.load(f)
            if 'rsshub' in d:
                if d['rsshub'][-1] == '/':
                    d['rsshub'] = d['rsshub'][:-1]
                data['rsshub'] = d['rsshub']
            if 'last_time' in d:
                data['last_time'] = d['last_time']
            if 'guild_rss' in d:
                data['guild_rss'] = d['guild_rss']
            if 'guild_mode' in d:
                data['guild_mode'] = d['guild_mode']
            if 'proxy' in d:
                data['proxy'] = d['proxy']
            if 'proxy_urls' in d:
                data['proxy_urls'] = d['proxy_urls']
    except:
        traceback.print_exc()
    # global default_rss


load_data()


default_rss = [
     data['rsshub'] + '/bilibili/user/dynamic/353840826',  # pcr官方号
]

async def query_data(url, proxy=''):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=proxy) as resp:
                return await resp.read()
    except:
        return None


def get_image_url(desc):
    imgs = re.findall(r'<img.*?src="(.+?)".+?>', desc)
    return imgs


def remove_html(content):
    # 移除html标签
    p = re.compile('<[^>]+>')
    content = p.sub("", content)
    return content


def remove_lf(content):
    text = ''
    for line in content.splitlines():
        line = line.strip()
        if line:
            text += line + '\n'
    text = text.rstrip()
    return text


async def generate_image(url_list):
    raw_images = []
    num = 0
    for url in url_list:
        url = html.unescape(url)
        proxy = ''
        for purl in data['proxy_urls']:
            if purl in url:
                proxy = data['proxy']
        image = await query_data(url, proxy)
        if image:
            try:
                im = Image.open(BytesIO(image))
                im = im.convert("RGBA")
                raw_images.append(im)
                num += 1
            except:
                pass
        if num >= 9:
            break
    if num == 0:
        return None
    elif num == 1:
        io = BytesIO()
        raw_images[0].save(io, 'png')
        return io.getvalue()
    dest_img = None
    box_size = 300
    row = 3
    border = 5
    height = 0
    width = 0
    if num == 3 or num >= 5:  # 3列
        width = 900 + border * 2
        height = math.ceil(num / 3) * (300 + border) - border
    else:  # 2列
        box_size = 400
        row = 2
        width = 800 + border
        height = math.ceil(num / 2) * (400 + border) - border
    dest_img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    for i in range(num):
        im = raw_images[i]
        if im:
            w, h = im.size
            if w > h:
                x0 = (w // 2) - (h // 2)
                x1 = x0 + h
                im = im.crop((x0, 0, x1, h))
            elif h > w:
                y0 = (h // 2) - (w // 2)
                y1 = y0 + w
                im = im.crop((0, y0, w, y1))
            im = im.resize((box_size, box_size), Image.ANTIALIAS)
            x = (i % row) * (box_size + border)
            y = (i // row) * (box_size + border)
            dest_img.paste(im, (x, y))
    io = BytesIO()
    dest_img.save(io, 'png')
    return io.getvalue()


def get_published_time(item):
    time_t = 0
    if 'published_parsed' in item:
        time_t = time.mktime(item['published_parsed'])
    if 'updated_parsed' in item:
        time_t = time.mktime(item['updated_parsed'])
    return time_t


def get_latest_time(item_list):
    last_time = 0
    for item in item_list:
        time = get_published_time(item)
        if time > last_time:
            last_time = time
    return last_time


def check_title_in_content(title, content):
    title = title[:len(title) // 2]
    title = title.replace('\n', '').replace('\r', '').replace(' ', '')
    content = content.replace('\n', '').replace('\r', '').replace(' ', '')
    if title in content:
        return True
    return False


async def get_rss_news(rss_url):
    news_list = []
    proxy = ''
    for purl in data['proxy_urls']:
        if purl in rss_url:
            proxy = data['proxy']
    res = await query_data(rss_url, proxy)
    if not res:
        return news_list
    feed = feedparser.parse(res)
    if feed['bozo'] != 0:
        logger.info(f'rss解析失败 {rss_url}')
        return news_list
    if len(feed['entries']) == 0:
        return news_list
    if rss_url not in data['last_time']:
        logger.info(f'rss初始化 {rss_url}')
        data['last_time'][rss_url] = get_latest_time(feed['entries'])
        return news_list
    last_time = data['last_time'][rss_url]
    for item in feed["entries"]:
        if get_published_time(item) > last_time:
            summary = item['summary']
            # 移除转发信息
            i = summary.find('//转发自')
            if i > 0:
                summary = summary[:i]
            news = {
                'feed_title': feed['feed']['title'],
                'title': item['title'],
                'content': remove_html(summary),
                'id': item['id'],
                'image': await generate_image(get_image_url(summary)),
            }
            news_list.append(news)
    data['last_time'][rss_url] = get_latest_time(feed['entries'])
    return news_list


async def refresh_all_rss():
    # for item in default_rss:
    #     if item not in rss_news:
    #         rss_news[item] = []
    for guild_rss in data['guild_rss'].values():
        for rss_url in guild_rss:
            if rss_url not in rss_news:
                rss_news[rss_url] = []
    # 删除没有引用的项目的推送进度
    for rss_url in list(data['last_time'].keys()):
        if rss_url not in rss_news:
            data['last_time'].pop(rss_url)
    for rss_url in rss_news.keys():
        rss_news[rss_url] = await get_rss_news(rss_url)
    save_data()


def add_salt(data):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    return data + bytes(salt, encoding="utf8")


def format_msg(news):
    msg = f"{news['feed_title']}更新:\n{news['id']}"
    if not check_title_in_content(news['title'], news['content']):
        msg += f"\n{news['title']}"
    msg += f"\n----------\n{remove_lf(news['content'])}"
    if news['image']:
        base64_str = f"base64://{base64.b64encode(add_salt(news['image'])).decode()}"
        msg += MessageSegment.image(base64_str)#f'[CQ:image,file={base64_str}]'
    return msg


def format_brief_msg(news):
    msg = f"{news['feed_title']}更新:\n{news['id']}"
    msg += f"\n----------\n{news['title']}"
    return msg


async def guild_process():
    await refresh_all_rss()
    # todo 这么写rss失去了意义 
    bot : Bot = get_driver().bots[str(BotInfo.bot_id)]
    
    for key in data['guild_rss']:
        for rss_url in data['guild_rss'][key]:
            if rss_url in rss_news:
                news_list = rss_news[rss_url]
                for news in reversed(news_list):
                    msg = None
                    if str(key) in data['guild_mode'] and data['guild_mode'][str(key)] == 1:
                        msg = format_brief_msg(news)
                    else:
                        msg = format_msg(news)
                    try:
                        if   '_' in str(key):
                            splits = key.split('_')
                            await send_guild_message(splits[0], splits[1], msg)
                            logger.info(f'频道{key}推送成功')     
                        else:
                            await bot.send_group_msg(group_id=key,message=msg)
                            logger.info(f'群聊{key}推送成功')

                    except Exception as e:
                        logger.error(e)
                        logger.info(f'群聊/频道 {key} 推送失败')
                await asyncio.sleep(1)


async def rss_add(gc_id, rss_url):
    gc_id = str(gc_id)
    proxy = ''
    for purl in data['proxy_urls']:
        if purl in rss_url:
            proxy = data['proxy']
    res = await query_data(rss_url, proxy)
    feed = feedparser.parse(res)
    if feed['bozo'] != 0:
        return f'无法解析rss源:{rss_url}'
    if gc_id not in data['guild_rss']:
        #pass
        data['guild_rss'][gc_id] = default_rss
    if rss_url not in set(data['guild_rss'][gc_id]):
        if gc_id not in data['guild_rss']:
            data['guild_rss'][gc_id] = list()
        data['guild_rss'][gc_id].append(rss_url)
    else:
        return '订阅列表中已存在该项目'
    save_data()
    return '添加成功'


def rss_remove(gc_id, i):
    gc_id = str(gc_id)
    if gc_id not in data['guild_rss']:
        return '订阅列表已经是空的啦'
        # data['guild_rss'][gc_id] = default_rss
    if i >= len(data['guild_rss'][gc_id]):
        return '序号超出范围'
    data['guild_rss'][gc_id].pop(i)
    save_data()
    return '删除成功\n当前' + rss_get_list(gc_id)


def rss_get_list(gc_id):
    gc_id = str(gc_id)
    if gc_id not in data['guild_rss']:
        return '暂无订阅~'
        # data['guild_rss'][gc_id] = default_rss
    msg = '订阅列表:'
    num = len(data['guild_rss'][gc_id])
    for i in range(num):
        url = data['guild_rss'][gc_id][i]
        url = re.sub(r'http[s]*?://.*?/', '/', url)
        msg += f"\n{i}. {url}"
    if num == 0:
        msg += "\n空"
    return msg


def rss_set_mode(gc_id, mode):
    gc_id = str(gc_id)
    mode = int(mode)
    if mode > 0:
        data['guild_mode'][gc_id] = 1
        msg = '已设置为简略模式'
    else:
        data['guild_mode'][gc_id] = 0
        msg = '已设置为标准模式'
    save_data()
    return msg


rss = on_command('rss', permission=SUPERUSER)


@rss.handle()
async def rss_cmd(bot: Bot, event: MessageEvent):
    if event.get_user_id() == bot.self_id:
        pass
    msg = ''
    gc_id = get_event_gid(event)
    args = event.get_plaintext().split(' ')[1:]
    # todo 判断为管理员再进行操作
    is_admin = True
    if len(args) == 0:
        msg = HELP_MSG
    elif args[0] == 'help':
        msg = HELP_MSG
    elif args[0] == 'add':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2:
            msg = await rss_add(gc_id, args[1])
        else:
            msg = '需要附带rss地址'
    elif args[0] == 'addb' or args[0] == 'add-bilibili':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            rss_url = data['rsshub'] + '/bilibili/user/dynamic/' + str(args[1])
            msg = await rss_add(gc_id, rss_url)
        else:
            msg = '需要附带up主id'
    elif args[0] == 'addr' or args[0] == 'add-route':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2:
            rss_url = data['rsshub'] + args[1]
            msg = await rss_add(gc_id, rss_url)
        else:
            msg = '需要提供route参数'
        pass
    elif args[0] == 'remove' or args[0] == 'rm':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            msg = rss_remove(gc_id, int(args[1]))
        else:
            msg = '需要提供要删除rss订阅的序号'
    elif args[0] == 'list' or args[0] == 'ls':
        msg = rss_get_list(gc_id)
    elif args[0] == 'mode':
        if not is_admin:
            msg = '权限不足'
        elif len(args) >= 2 and args[1].isdigit():
            msg = rss_set_mode(gc_id, args[1])
        else:
            msg = '需要附带模式(0/1)'
    else:
        msg = '参数错误'
    await rss.send(Message(msg))


@scheduler.scheduled_job('interval', minutes=1)
async def job():
    await guild_process()
