# ref: https://github.com/GWYOG/GWYOG-Hoshino-plugins/blob/master/pcravatarguess
# Originally written by @GWYOG
# Reflacted by @Ice-Cirno
# GPL-3.0 Licensed
# Thanks to @GWYOG for his great contribution!

import asyncio
import os
import random
import aiohttp
import requests
from bs4 import BeautifulSoup
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, Message
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.typing import T_State
from pathlib import Path
from .data_source import Guess
from nonebot.params import  CommandArg
from ... import  chara
from . import  GameMaster, get_guild_member_info

'''
sv = Service('voiceguess', bundle='pcr娱乐', help_=''
[cygames] 猜猜随机的"cygames"语音来自哪位角色
''.strip())
'''
# pcr图片路径
PCR_PATH = Path("resources/pcr/")
RES_DIR = PCR_PATH
DOWNLOAD_THRESHOLD = 76
MULTIPLE_VOICE_ESTERTION_ID_LIST = ['0044']
ONE_TURN_TIME = 20
RES_PATH = os.path.expanduser(RES_DIR)
DIR_PATH = os.path.join(RES_PATH, 'voice_ci')
DB_PATH = os.sep.join(['plugins', 'pcr', 'data',  'pcr_voice_guess.db'])
gm = GameMaster(DB_PATH)
finish_event = asyncio.Event()

def get_estertion_id_list():
    url = 'https://redive.estertion.win/sound/vo_ci/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    l = []
    for a in soup.find_all('a'):
        s = a['href'][:-1]
        if s.isdigit():
            l.append(s)
    return l


def estertion_id2chara_id(estertion_id):
    return (estertion_id + 1000)


async def download(url, path):
    try:
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                content = await resp.read()
                with open(path, 'wb') as f:
                    f.write(content)
        return True
    except:
        return False


async def download_voice_ci(bot):
    if not os.path.exists(DIR_PATH):
        os.makedirs(DIR_PATH)
    file_name_list = os.listdir(DIR_PATH)
    file_name_list_no_suffix = [file.rsplit('.', 1)[0] for file in file_name_list]
    if len(file_name_list) < DOWNLOAD_THRESHOLD:
        count = 0
        await bot.send(f'正在下载"cygames"语音资源，请耐心等待')
        estertion_id_list = get_estertion_id_list()
        for eid in estertion_id_list:
            file_number_list = ['001'] if eid not in MULTIPLE_VOICE_ESTERTION_ID_LIST else ['001', '002']
            for file_number in file_number_list:
                url = f'https://redive.estertion.win/sound/vo_ci/{eid}/vo_ci_1{eid[1:]}01_{file_number}.m4a'
                file_name = url.split('/')[-1]
                if file_name.rsplit('.', 1)[0] not in file_name_list_no_suffix:
                    file_path = os.path.join(DIR_PATH, file_name)
                    print(f'准备下载{file_name}...')
                    if not await download(url, file_path):
                        print(f'下载{file_name}失败, 准备删除文件.')
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        print(f'删除文件{file_name}成功.')
                    else:
                        print(f'下载{file_name}成功!')
                        count = count + 1
        await bot.send(
            f'下载完毕，此次下载"cygames"语音包{count}个，目前共{len(os.listdir(DIR_PATH))}个. 如果您使用的是go-cqhttp，请更新到v0.9.28或更高的版本并自行配置ffmpeg，否则无法发送m4a格式的语音.')


matcher = Guess().on_command("猜语音排行", "猜语音排行", aliases={"猜语音排行", "猜语音排行榜", "猜语音群排行"}, priority=5)


@matcher.handle()
async def description_guess_group_ranking(bot: Bot, event: MessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    type=get_id(event)[2]
    ranking = gm.db.get_ranking(get_gid)
    msg = ["【猜语音小游戏排行榜】"]
    for i, item in enumerate(ranking):
        uid, count = item
        if type == 'guild':
            m = get_guild_member_info(get_gid, uid) or uid
        if type == 'group':
            user = await bot.get_group_member_info(group_id=event.group_id, user_id=uid)
            m = user['card'] if user['card'] else user['nickname']
        name = str(m)
        msg.append(f"第{i + 1}名：{name} 猜对{count}次")
    await matcher.send("\n".join(msg))


matcher = Guess().on_command("cygames", "猜cygames", priority=5)


@matcher.handle()
async def cygames_voice_guess(bot: Bot, event: MessageEvent, state: T_State,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    if   get_id(event)[1]=="guild":
        return
    get_gid=get_id(event)[1]
    if gm.is_playing(get_gid):
        await matcher.finish("游戏仍在进行中…")
    with gm.start_game(get_gid) as game:
        await download_voice_ci(matcher)
        file_list = os.listdir(DIR_PATH)
        chosen_file = random.choice(file_list)
        file_path = os.path.join(DIR_PATH, chosen_file)
        await matcher.send(f'猜猜这个“cygames”语音来自哪位角色? ({ONE_TURN_TIME}s后公布答案)')
        # result=f"[CQ:record,file={os.path.abspath(file_path)}]"
        result = MessageSegment.record(f'file:///{os.path.abspath(file_path)}')
        await matcher.send(result)

        # await bot.send(event,result)#f'[CQ:record,file={os.path.abspath(file_path)}]'
        estertion_id = chosen_file[7:10]
        chara_id = estertion_id2chara_id(int(estertion_id))
        game.answer = chara_id
        print(chara.fromid(game.answer).name)
        try:
            await asyncio.wait_for(finish_event.wait(), timeout=ONE_TURN_TIME) # 等待15秒或者收到指令
        except asyncio.TimeoutError:
            if game.winner:
                return
            c = chara.fromid(game.answer)
            txt = f"正确答案是：{c.name}"
            meg = c.icon.cqcode
            await matcher.send(Message(txt + meg) + f"\n很遗憾，没有人答对~")
        finally:
            finish_event.clear() # 清除事件标志
            print("事件响应器结束")


matcher = Guess().on_command("猜语音","猜语音", priority=5)


@matcher.handle()
async def voice_guess(bot: Bot, event: MessageEvent, state: T_State,args: Message = CommandArg()):
    args = args.extract_plain_text() 
    if   args:
        return
    get_gid=get_id(event)[1]
    if gm.is_playing(get_gid):
        await matcher.finish("游戏仍在进行中…")
    with gm.start_game(get_gid) as game:
        img_path = os.path.join(RES_PATH, 'img', 'priconne', 'unit', 'icon_unit_100031.png')

        file_ci_list = os.listdir(DIR_PATH)
        chosen_file = random.choice(file_ci_list)
        voice_path = os.path.join(DIR_PATH, chosen_file)

        estertion_id = chosen_file[7:10]
        chara_id = estertion_id2chara_id(int(estertion_id))
        record_path = os.path.join(RES_PATH, 'record', f'{chara_id}')

        if not os.path.exists(record_path):
            os.makedirs(record_path)
        file_list = os.listdir(record_path)
        if file_list:
            included_extensions = ['mp4']
            file_names = [fn for fn in os.listdir(record_path)
                          if any(fn.endswith(ext) for ext in included_extensions)]
            chosen_file = random.choice(file_names).split('.')[0]
            print(chosen_file)
        else:
            chosen_file = chara_id
        video_path = os.path.join(RES_PATH, 'record', f'{chara_id}', f'{chosen_file}.mp4')

        print(not os.path.exists(video_path))
        if not os.path.exists(video_path):
            get_video(video_path, img_path)
            get_audio(voice_path, video_path)
        await matcher.send(f'猜猜这段语音来自哪位角色? ({ONE_TURN_TIME}s后公布答案)')
        print(f'file:///{os.path.abspath(video_path)}')
        await matcher.send(MessageSegment.video(f'file:///{os.path.abspath(video_path)}'))

        game.answer = chara_id
        # print(chara.fromid(game.answer).name)
        try:
            await asyncio.wait_for(finish_event.wait(), timeout=ONE_TURN_TIME) # 等待15秒或者收到指令
        except asyncio.TimeoutError:
            if game.winner:
                return
            c = chara.fromid(game.answer)
            txt = f"正确答案是：{c.name}"
            meg = c.icon.cqcode
            await matcher.send(Message(txt + meg) + f"\n很遗憾，没有人答对~")
        finally:
            finish_event.clear() # 清除事件标志
            print("事件响应器结束")


sv = Guess().on_message(priority=5)


@sv.handle()
async def on_input_chara_name(bot: Bot, event: MessageEvent):
    get_gid=get_id(event)[1]
    game = gm.get_game(get_gid)
    if not game or game.winner:
        return
    c = chara.fromname(event.message.extract_plain_text())
    if c.id != chara.UNKNOWN and c.id == game.answer:
        game.winner = event.user_id
        n = game.record()
        txt = f"猜对了，真厉害！TA已经猜对{n}次了~\n正确答案是{c.name}"
        msg = c.icon.cqcode
        await sv.send(Message(txt + msg) + f"\n(此轮游戏将在几秒后自动结束，请耐心等待)", at_sender=True)
        finish_event.set() 


import os
from moviepy.editor import VideoFileClip, AudioFileClip
import cv2


def get_video(video_path, img_path):
    video_dir = video_path  # 输出视频的保存路径
    fps = 60  # 帧率
    img_size = (128, 128)  # 图片尺寸
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
    frame = cv2.imread(img_path)
    frame = cv2.resize(frame, img_size)  # 生成视频   图片尺寸和设定尺寸相同
    videoWriter.write(frame)  # 将图片写进视频里
    videoWriter.release()  # 释放资源


# 加入音频
def get_audio(voice_path, video_path):
    videoFile = os.path.abspath(video_path)  # 视频文件
    video = VideoFileClip(videoFile)
    videos = video.set_audio(AudioFileClip(os.path.abspath(voice_path)))  # 音频文件
    videos.write_videofile(video_path, audio_codec='aac')  # 保存合成视频，注意加上参数audio_codec='aac'，否则音频无声音


def do(img_path, voice_path, video_path):
    if not os.path.exists(video_path):
        get_video(video_path, img_path)
        get_audio(voice_path, video_path)
    return

def get_id(event: MessageEvent):
    type = str(event.message_type)
    if type == 'group':
        group_id = event.group_id
        user_id = event.user_id
        get_gid = group_id
    elif type == 'private':
        user_id = event.user_id
        get_gid = user_id
    elif type == 'guild':
        guild_id = event.guild_id
        gc_id = f'{guild_id}'
        user_id = event.user_id
        get_gid = gc_id
    else:
        return 
    return user_id,get_gid,type
    
