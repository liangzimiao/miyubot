from typing import Optional
from pathlib import Path
from pydantic import Extra, BaseModel
import os
from nonebot.log import logger
import copy


def check_character(name, valid_names, tts_gal):
    index = None
    model_name = ""
    for names, model in tts_gal.items():
        if names in valid_names and ((isinstance(names,str) and names == name) or name in names):
            model_name= model[0] 
            index = None if len(model) == 1 else int(model[1])
            break
    return  model_name, index

async def checkFile(tts_gal,plugin_meta,valid_names):
    '''添加目前检测出来的可以使用的角色语音'''
    valid_character_names_list = [name for name,model in tts_gal.items()]
    valid_names += valid_character_names_list
    valid_character_names = []
    for name in valid_character_names_list:
        if isinstance(name,str):
            valid_character_names.append(name)
        else:
            valid_character_names.append("/".join(name))
    if len(valid_character_names):
        plugin_meta.usage = plugin_meta.usage + "\n目前可使用的语音角色：\n" + "\n".join(valid_character_names)
    else:
        plugin_meta.usage = plugin_meta.usage + "\n目前无可使用的语音角色\n"


tts_gal = {
    ("亚托莉","ATRI","atri",): ["ATRI",0],
    ("绫地宁宁", "宁宁",): ["YuzuSoft",0],
    ("因幡爱瑠", "爱瑠"): ["YuzuSoft",1],
    ("朝武芳乃", "芳乃"): ["YuzuSoft",2],
    ("常陸茉子", "茉子"): ["YuzuSoft",3],
    ("丛雨", "幼刀"): ["YuzuSoft",4],
    ("鞍马小春", "鞍馬小春", "小春"): ["YuzuSoft",5],
    ("在原七海", "七海"): ["YuzuSoft",6],
    ("特别周",): ["uma87",0],
    ("无声铃鹿",): ["uma87",1],
    ("东海帝皇",): ["uma87",2],
    ("丸善斯基",): ["uma87",3],
    ("富士奇迹",): ["uma87",4],
    ("小栗帽",): ["uma87",5],
    ("黄金船",): ["uma87",6],
    ("伏特加",): ["uma87",7],
    ("大和赤骥",): ["uma87",8],
    ("大树快车",): ["uma87",9],
    ("草上飞",): ["uma87",10],
    ("菱亚马逊",): ["uma87",11],
    ("目白麦昆",): ["uma87",12],
    ("神鹰",): ["uma87",13],
    ("好歌剧",): ["uma87",14],
    ("成田白仁",): ["uma87",15],
    ("皇帝",): ["uma87",16],
    ("气槽",): ["uma87",17],
    ("爱丽数码",): ["uma87",18],
    ("青云天空",): ["uma87",19],
    ("玉藻十字",): ["uma87",20],
    ("美妙姿势",): ["uma87",21],
    ("琵琶晨光",): ["uma87",22],
    ("重炮",): ["uma87",23],
    ("曼城茶座",): ["uma87",24],
    ("美浦波旁",): ["uma87",25],
    ("目白赖恩",): ["uma87",26],
    ("菱曙",): ["uma87",27],
    ("雪之美人",): ["uma87",28],
    ("米浴",): ["uma87",29],
    ("艾尼斯风神",): ["uma87",30],
    ("爱丽速子",): ["uma87",31],
    ("爱慕织姬",): ["uma87",32],
    ("稻荷一",): ["uma87",33],
    ("胜利奖券",): ["uma87",34],
    ("空中神宫",): ["uma87",35],
    ("荣进闪耀",): ["uma87",36],
    ("真机伶",): ["uma87",37],
    ("川上公主",): ["uma87",38],
    ("黄金城",): ["uma87",39],
    ("樱花进王",): ["uma87",40],
    ("采珠",): ["uma87",41],
    ("新光风",): ["uma87",42],
    ("东商变革",): ["uma87",43],
    ("超级小海湾",): ["uma87",44],
    ("醒目飞鹰",): ["uma87",45],
    ("荒漠英雄",): ["uma87",46],
    ("东瀛佐敦",): ["uma87",47],
    ("中山庆典",): ["uma87",48],
    ("成田大进",): ["uma87",49],
    ("西野花",): ["uma87",50],
    ("春乌拉拉",): ["uma87",51],
    ("青竹回忆",): ["uma87",52],
    ("微光飞驹",): ["uma87",53],
    ("美丽周日",): ["uma87",54],
    ("待兼福来",): ["uma87",55],
    ("千明代表",): ["uma87",56],
    ("名将怒涛",): ["uma87",57],
    ("目白多伯",): ["uma87",58],
    ("优秀素质",): ["uma87",59],
    ("帝王光辉",): ["uma87",60],
    ("待兼诗歌剧",): ["uma87",61],
    ("生野狄杜斯",): ["uma87",62],
    ("目白善信",): ["uma87",63],
    ("大拓太阳神",): ["uma87",64],
    ("双涡轮",): ["uma87",65],
    ("里见光钻",): ["uma87",66],
    ("北部玄驹",): ["uma87",67],
    ("樱花千代王",): ["uma87",68],
    ("天狼星象征",): ["uma87",69],
    ("目白阿尔丹",): ["uma87",70],
    ("八重无敌",): ["uma87",71],
    ("鹤丸刚志",): ["uma87",72],
    ("目白光明",): ["uma87",73],
    ("樱花桂冠",): ["uma87",74],
    ("成田路",): ["uma87",75],
    ("也文摄辉",): ["uma87",76],
    ("吉兆",): ["uma87",77],
    ("谷野美酒",): ["uma87",78],
    ("第一红宝石",): ["uma87",79],
    ("真弓快车",): ["uma87",80],
    ("骏川手纲","绿帽"): ["uma87",81],
    ("凯斯奇迹",): ["uma87",82],
    ("小林历奇",): ["uma87",83],
    ("北港火山",): ["uma87",84],
    ("奇锐骏",): ["uma87",85],
    ("秋川理事长","理事长"): ["uma87",86],
    
    ("佩可莉姆","pecorine",): ["pecorine",10],
    ("可可萝","kokoro",): ["kokoro",0],
    ("凯露","kyaru",): ["kyaru",10],
    ("美空","misora",): ["misora",0],
    ("爱梅斯","ameth",): ["ameth",0],
    ("日和莉","hiyori",): ["hiyori",0],
    ("柏崎初音","hatsune","星法"): ["hatsune",10],
    ("惠理子","eriko",): ["eriko",0],
    ("镜华","kyoka"): ["kyoka",0],
    ("优妮",
        "ユニ",
        "Yuni",
        "真行寺由仁",
        "由仁",
        "优尼",
        "u2",
        "优妮辈先",
        "辈先",
        "书记",
        "uni",
        "先辈",
        "仙贝",
        "油腻",
        "优妮先辈",
        "学姐",
        "18岁黑丝学姐"): ["bzd4567",0],
    ("琪爱儿",
        "チエル",
        "Chieru",
        "千爱瑠",
        "切露",
        "茄露",
        "茄噜",
        "切噜"): ["bzd4567",1],
    ("克萝依",
        "クロエ",
        "Kuroe",
        "克罗依",
        "华哥",
        "黑江",
        "黑江花子",
        "花子"): ["bzd4567",2],
    
    
    ("天童爱丽丝","alice","爱丽丝",): ["ba",0],
    ("一之濑明日奈","asuna","明日奈", ): ["ba",1],
    ("白洲梓","azusa","阿梓","梓", ): ["ba",2],
    ("空崎日奈","hina","日奈", ): ["ba",3],
    ("小鸟游星野","hoshino","星野","大叔", ): ["ba",4],
    ("银镜伊织","iori","伊织", ): ["ba",5],
    ("伊吕波","iroha","168", ): ["ba",6],
    ("久田泉奈","itsuna","泉奈", ): ["ba",7],
    ("角楯花凛","karin","花凛", ): ["ba",8],
    ("圣园未花","mika","未花", ): ["ba",9],
    ("霞泽美游","miyu","美游", ): ["ba",10],
    ("砂狼白子","shiroko","白子", ): ["ba",11],
    ("早濑优香","youka","优香",): ["ba",12],
    ("天童爱丽丝_zh","alice_zh","爱丽丝_zh",): ["ba_zh",0],
    ("一之濑明日奈_zh","asuna_zh","明日奈_zh", ): ["ba_zh",1],
    ("白洲梓_zh","azusa_zh","阿梓_zh","梓_zh", ): ["ba_zh",2],
    ("空崎日奈_zh","hina_zh","日奈_zh", ): ["ba_zh",3],
    ("小鸟游星野_zh","hoshino_zh","星野_zh","大叔_zh", ): ["ba_zh",4],
    ("银镜伊织_zh","iori_zh","伊织_zh", ): ["ba_zh",5],
    ("伊吕波_zh","iroha_zh","168_zh", ): ["ba_zh",6],
    ("久田泉奈_zh","itsuna_zh","泉奈_zh", ): ["ba_zh",7],
    ("角楯花凛_zh","karin_zh","花凛_zh", ): ["ba_zh",8],
    ("圣园未花_zh","mika_zh","未花_zh", ): ["ba_zh",9],
    ("霞泽美游_zh","miyu_zh","美游_zh", ): ["ba_zh",10],
    ("砂狼白子_zh","shiroko_zh","白子_zh", ): ["ba_zh",11],
    ("早濑优香_zh","youka_zh","优香_zh",): ["ba_zh",12],

    ("刻晴","keqing",): ["keqing",115],
    ("优菈","eula",): ["eula",124],

    ("布洛妮娅","bronya","理之律者","板鸭"): ["bronya",193],
    ("德莉莎","delisha","德丽莎"): ["delisha",205],

    ("锦木千束","chisato","千束"): ["chisato",0],
    ("井上泷奈","takina","泷奈"): ["takina",0],
}