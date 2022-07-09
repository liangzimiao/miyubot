from .utils import Command
from .functions import *

commands = [
    Command(universal, ("万能表情", "空白表情")),
    Command(petpet, ("摸", "摸摸", "摸头", "rua"), r"摸摸?头?|rua"),
    Command(kiss, ("亲", "亲亲"), r"亲亲?"),
    Command(rub, ("贴", "贴贴", "蹭", "蹭蹭"), r"贴贴?|蹭蹭?"),
    Command(play, ("顶", "玩","吞")),
    Command(pat, ("拍",)),
    Command(rip, ("撕",)),
    Command(throw, ("丢", "扔")),
    Command(throw_gif, ("抛", "掷")),
    Command(crawl, ("爬",)),
    Command(support, ("精神支柱",)),
    Command(always, ("一直",)),
    Command(loading, ("加载中",)),
    Command(turn, ("转",)),
    Command(littleangel, ("小天使",)),
    Command(dont_touch, ("不要靠近",)),
    Command(alike, ("一样",)),
    Command(roll, ("滚",)),
    Command(play_game, ("玩游戏",), r"来?玩游戏"),
    Command(worship, ("膜", "膜拜"), r"膜拜?"),
    Command(eat, ("吃",)),
    Command(bite, ("啃",)),
    Command(police, ("出警",)),
    Command(police1, ("警察",)),
    Command(ask, ("问问",), r"去?问问"),
    Command(prpr, ("舔", "舔屏", "prpr"), r"舔屏?|prpr"),
    Command(twist, ("搓",)),
    Command(wallpaper, ("墙纸",)),
    Command(china_flag, ("国旗",)),
    Command(make_friend, ("交个朋友",)),
    Command(back_to_work, ("继续干活", "打工人")),
    Command(perfect, ("完美",), r"完美的?"),
    Command(follow, ("关注",)),
    Command(my_friend, ("我朋友{name}说",), r"我(?:有个)?朋友(?P<name>.*?)说"),
    Command(paint, ("这像画吗",)),
    Command(shock, ("震惊",)),
    Command(coupon, ("兑换券",)),
    Command(listen_music, ("听音乐",)),
    Command(dianzhongdian, ("典中典", "黑白草图")),
    Command(funny_mirror, ("哈哈镜",)),
    Command(love_you, ("永远爱你",)),
    Command(symmetric, ("对称",)),
    Command(safe_sense, ("安全感",)),
    Command(always_like, ("我永远喜欢",), r"我?永远喜欢"),
    Command(interview, ("采访",)),
    Command(punch, ("打拳",)),
    Command(cyan, ("群青",)),
    Command(pound, ("捣",)),
    Command(thump, ("捶",)),
    Command(need, ("需要", "你可能需要")),
    Command(cover_face, ("捂脸",)),
    Command(knock, ("敲",)),
    Command(garbage, ("垃圾", "垃圾桶"), r"垃圾桶?"),
    Command(whyatme, ("为什么@我",), r"为什么(?:@|at)我"),
    Command(decent_kiss, ("像样的亲亲",)),
    Command(jiujiu, ("啾啾",)),
    Command(suck, ("吸", "嗦")),
    Command(hammer, ("锤",)),
    Command(tightly, ("紧贴", "紧紧贴着")),
    Command(distracted, ("注意力涣散",)),
    Command(anyasuki, ("阿尼亚喜欢",)),
    Command(thinkwhat, ("想什么",)),
    Command(keepaway, ("远离",)),
    Command(marriage, ("结婚申请", "结婚登记", "结婚")),
    Command(painter, ("小画家",)),
    Command(repeat, ("复读",)),
]
from utils.service import Service
from utils.rule import is_in_service

__doc__ = '''
[头像表情包]
摸头等头像相关表情制作
触发方式：指令 + @user/qq/自己/图片\n发送“头像表情包”查看支持的指令
'''


class Petpet(Service):
    def __init__(self):
        Service.__init__(self, "petpet", __doc__, rule=is_in_service("petpet"))

