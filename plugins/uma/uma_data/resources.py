import json
import os
import re
import requests
from nonebot import logger


class Uma_res:

    def __init__(self):

        self.get_chara_res()
        self.get_card_res()
        self.update_chara_name()
 
#获取角色卡资源
    def get_chara_res(self):
        self.chara_info_dict_path = os.path.join(os.path.dirname(__file__), 'chara_info_dict.json')
        if not os.path.exists(self.chara_info_dict_path):
            self.update_chara_res()
            logger.info(f'开始更新chara_info')
        try:
            with open(self.chara_info_dict_path, "r",encoding="utf-8") as f:
                self.chara_info_dict=json.load(f)

            self.id_name_dict={}
            self.star_id_dict=dict()    
            for id in self.chara_info_dict:
                self.star_id_dict.setdefault(self.chara_info_dict[id]["star"],[]).append(id)
                self.id_name_dict[id]=[self.chara_info_dict[id]["cn_name"],self.chara_info_dict[id]["jp_name"]]
        except Exception as e:
            logger.warning(f'获取chara_info失败:{e}')
#获取支援卡资源
    def get_card_res(self):
        self.card_info_dict_path = os.path.join(os.path.dirname(__file__), 'card_info_dict.json')
        if not os.path.exists(self.card_info_dict_path):
            self.update_card_res()
            logger.info(f'开始更新card_info')
        try:
            with open(self.card_info_dict_path, "r",encoding="utf-8") as f:
                self.card_info_dict=json.load(f)
            self.rare_id_dict={}   
            for id in self.card_info_dict:
                if self.card_info_dict[id]["origin"]=="卡池" or self.card_info_dict[id]["origin"]=="":
                    self.rare_id_dict.setdefault(self.card_info_dict[id]["rare"],[]).append(id)
                else:
                    continue
        except Exception as e:
            logger.warning(f'获取card_info失败:{e}')

#更新角色卡资源
    def update_chara_res(self):
        url="https://wiki.biligame.com/umamusume/%E8%B5%9B%E9%A9%AC%E5%A8%98%E5%9B%BE%E9%89%B4"
        res=requests.get(url).text
        src='data-param1="(.*?)" .*?\n<td><a href="(.*?)" title="(.*?)"><img alt="Chr icon (.*?) 01.png" src=".*?".* srcset=".*?1.5x, (.*?) 2x".*/></a>\n</td>\n<td>.*?>.*?>(.*?)】'
        chara_src_list=re.findall(src,res,re.M)
        self.chara_info_dict={}
        self.id_name_dict={}
        self.star_id_dict=dict()
        for src in chara_src_list:
            id=src[3].split(" ")[1]
            #chara_icon_name=src[3].replace(" ","_")
            chara_web=f"https://wiki.biligame.com/{src[1]}"
            self.chara_info_dict[id]={
                "star":src[0],
                "chara_web":chara_web,
                "cn_name":src[2],
                "png_name":id,
                "url":src[4],
                "jp_name":src[5]
            }
            self.id_name_dict[id]=[src[2],src[5]]
            self.star_id_dict.setdefault(src[0],[]).append(id)
        #print(self.chara_info_dict)
        self.chara_info_dict_path = os.path.join(os.path.dirname(__file__), 'chara_info_dict.json')
        with open(self.chara_info_dict_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(self.chara_info_dict, ensure_ascii=False, indent=4, separators=(',', ':')))
#更新支援卡资源
    def update_card_res(self):
        url="https://wiki.biligame.com/umamusume/%E6%94%AF%E6%8F%B4%E5%8D%A1%E5%9B%BE%E9%89%B4"
        res=requests.get(url).text
        src='data-param1="(.*?)" data-param2="(.*?)" data-param3="(.*?)">\n.*?<img alt="(.*?)".*?1.5x, (.*?) 2x.*\n.*\n.*">(.*?)</a>\n.*\n.*">(.*?)</a>\n.*\n.*">(.*?)</a>\n.*\n.*\n.*\n.*\n.*\n.*>(.*?)\n</td>'
        card_src_list=re.findall(src,res,re.M)
        self.card_info_dict={}
        for src in card_src_list:
            card_png_name=src[3]
            card_png_name=card_png_name.split(".")[0]
            card_png_name=card_png_name.replace(" ","_")
            id=card_png_name.split("_")[2] 
            self.card_info_dict[id]={
                "rare":src[0],
                "type":src[1],
                "effecct":src[2],
                "png_name":card_png_name,
                "url":src[4],
                "jp_name":src[5],
                "cn_name":src[6],
                "chara":src[7],
                "origin":src[8]
                }
        #print(self.card_info_dict)
        self.card_info_dict_path = os.path.join(os.path.dirname(__file__), 'card_info_dict.json')
        with open(self.card_info_dict_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(self.card_info_dict, ensure_ascii=False, indent=4, separators=(',', ':')))

#下载角色卡icon
    def chara_icon_download(self,id):
        id=str(id)
        icon_save_path = f'resources\\uma\\img\\unit\\icon_unit_{self.chara_info_dict[id]["png_name"]}.png'
        if os.path.exists(icon_save_path):
            logger.info(f'chara icon from {self.chara_info_dict[id]["cn_name"]}已存在')
            return
        else :    
            logger.info(f'Downloading chara icon from {self.chara_info_dict[id]["url"]}')
        try:
            rsp = requests.get(self.chara_info_dict[id]["url"], stream=True, timeout=5).content
            with open(icon_save_path,"wb")as fp:
                fp.write(rsp)    
            logger.info(f'{self.chara_info_dict[id]["cn_name"]}:{self.chara_info_dict[id]["png_name"]}.png Saved to {icon_save_path}')
        except Exception as e:
            logger.info(f'Failed to download {self.chara_info_dict[id]["cn_name"]}. {type(e)}')
            logger.exception(e)
#下载支援卡card
    def support_card_download(self,id):
        id=str(id)
        card_save_path = f'resources\\uma\\img\\support_card\\{self.card_info_dict[id]["png_name"]}.png'
        if os.path.exists(card_save_path):
            logger.info(f'card icon from {self.card_info_dict[id]["cn_name"]}已存在')
            return
        else :    
            logger.info(f'Downloading support chard from {self.card_info_dict[id]["url"]}')
        try:
            rsp = requests.get(self.card_info_dict[id]["url"], stream=True, timeout=5).content
            with open(card_save_path,"wb")as fp:
                fp.write(rsp)    
            logger.info(f'{self.card_info_dict[id]["cn_name"]}:{self.card_info_dict[id]["png_name"]}.png Saved to {card_save_path}')
        except Exception as e:
            logger.info(f'Failed to download {self.card_info_dict[id]["cn_name"]}. {type(e)}')
            logger.exception(e)
        
#更新角色别名
    def update_chara_name(self):
        uma_alias_path = os.path.join(os.path.dirname(__file__), 'uma_alias.json')
        with open(uma_alias_path , 'r', encoding='utf-8') as f:
                chara_name_str = json.load(f)
        uma_alias_dic={}        
        i=0
        for chara_name in chara_name_str: 
            for name in chara_name_str[chara_name]:
                i=i+1
                uma_alias_dic[int(i)]=chara_name_str[chara_name][name]
                uma_alias_dic[int(i)].append(f'{name}')
        icon_code_list=[]
        chara_name_list=[]
        chara_name2_list=[]
        for id in self.chara_info_dict:
            self.chara_info_dict[id]
            icon_code_list.append(id)
            chara_name_list.append(self.chara_info_dict[id]["cn_name"])
            chara_name2_list.append(self.chara_info_dict[id]["jp_name"])
        a=-1
        for k in icon_code_list:
            a=a+1
            for i in uma_alias_dic:
                for j in uma_alias_dic[int(i)]:
                    if j==chara_name_list[a] or j==chara_name2_list[a] :
                        for l in uma_alias_dic[int(i)]:
                            if l in self.id_name_dict[k] :
                                continue
                            else :
                                self.id_name_dict[k].append(l)
                        #print(self.id_name_dict[k].append(uma_alias_dic[int(i)]))
                        #self.id_name_dict[k].append(uma_alias_dic[int(i)])
                        #self.id_name_dict[k]=uma_alias_dic[int(i)]
                        #break
        uma_name_path = os.path.join(os.path.dirname(__file__), 'dict_id_name.json')
        with open(uma_name_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(self.id_name_dict, ensure_ascii=False, indent=4, separators=(',', ':')))


uma_res=Uma_res()