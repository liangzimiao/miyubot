import re
from asyncio import Lock
from json import load
from os.path import dirname, join

from nonebot.adapters.onebot.v11 import MessageEvent, Bot, GroupMessageEvent, MessageSegment
from nonebot.typing import T_State
from nonebot import logger
from nonebot_plugin_guild_patch import GuildMessageEvent
from utils import send_guild_message
from .create_img import generate_info_pic, generate_support_pic
from .data_source import Arena
from datetime import datetime

curpath = dirname(__file__)
# 下面的内容后续优化为对象类型
cache = {}
client = None
info_url = None
support_url = None
request_lock = Lock()
response_check = False
oldMessageEvent: MessageEvent = None
group_id = 418416747
last_time = None

# oldMessageEvent.get_type()
with open(join(curpath, 'account.json')) as fp:
    acinfo = load(fp)

details = Arena().on_regex(r'^详细查询 ?(\d{13})?$', '详情查询uid')


@details.handle()
async def on_query_arena_all(bot: Bot, event: MessageEvent, state: T_State):
    global response_check, oldMessageEvent, last_time
    if last_time is None:
        last_time = datetime.now()
    elif (datetime.now() - last_time).seconds > 10 and request_lock.locked():
        request_lock.release()
    await request_lock.acquire()
    last_time = datetime.now()
    # await bot.send_private_msg(
    #     user_id=acinfo['admin'],
    #     message=f'''详情查询{state['_matched_groups'][1]}'''
    # )
    await bot.send_group_msg(
        group_id=group_id,
        message=f'''{event.get_message()}'''
    )
    oldMessageEvent = event
    response_check = True


validated = Arena().on_message(block=False)


# todo私聊消息
@validated.handle()
async def validate(bot: Bot, event: GroupMessageEvent):
    global response_check, oldMessageEvent, info_url, support_url
    if event.get_user_id() == str(acinfo['admin']) \
            and response_check and oldMessageEvent and group_id == event.group_id:
        result = re.findall("\[CQ:image,file=.+?,url=(.+?)subType=.+?", event.get_message().__str__())
        if len(result) >= 2:  # 不太可能>2
            try:
                info_url = result[0]
                support_url = result[1]
                message = f'''{MessageSegment.at(oldMessageEvent.get_user_id())}{MessageSegment.image(info_url)}{MessageSegment.image(support_url)}'''
                # 获取全局结果
                if type(oldMessageEvent) == GroupMessageEvent:
                    await bot.send_group_msg(
                        group_id=oldMessageEvent.group_id,
                        message=message
                    )
                elif type(oldMessageEvent) == GuildMessageEvent:
                    await send_guild_message(str(oldMessageEvent.guild_id), str(oldMessageEvent.channel_id), message)
            except Exception as e:
                logger.error(e)
            finally:
                oldMessageEvent = None
                response_check = False
                # 发送结果信息
                if request_lock.locked():
                    request_lock.release()
