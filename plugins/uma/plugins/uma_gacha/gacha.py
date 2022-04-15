import json
import os
import re
import requests
from nonebot import logger
import random
from plugins.uma.chara import guess_id
from plugins.uma.uma_data.resources import Uma_res
import json
import re
import requests
import numpy as np
from pyquery import PyQuery as pq
#from . import uma_data
UNKNOWN = 1000

class UmaGacha(object):

    def __init__(self):
        super().__init__()
        self.load_pool()

    def load_pool(self):

        try:
            self.dic=Uma_res().star_id_dict
            #self.uma_name_path = os.path.join(os.path.dirname(__file__), 'uma_gacha.json')
            #with open(self.uma_name_path, "w",encoding="utf-8") as f:
            #    f.write(json.dumps(self.dic, ensure_ascii=False, indent=4, separators=(',', ':')))    
            logger.info(f'uma-gacha初始化成功')
        except Exception as e:
            logger.error(f'uma-gacha初始化失败 {e}')
#单抽
    def gacha_one(self,up_id:list):
        up=up_id
        #up.append(up_id)
        pick=random.randint(0,999)
        if pick<30:
            if pick<=7:
                if UNKNOWN in up:
                    gacha_one=random.choice(self.dic["3"])
                else:
                    gacha_one=str(random.choice(up)) 
                    while gacha_one not in self.dic["3"]:
                        gacha_one=str(random.choice(up))  
            else:
                gacha_one=random.choice(self.dic["3"])
        elif pick<180:
            if pick<75:
                flag=False
                for i in up :
                    if i in self.dic["2"]:
                        flag=True
                        break
                if not flag:#无up
                    gacha_one=random.choice(self.dic["2"])
                else:#有up
                    gacha_one=str(random.choice(up)) 
                    while gacha_one not in self.dic["2"]:
                        gacha_one=str(random.choice(up))
            else:   
                gacha_one=random.choice(self.dic["2"])
        else :
            gacha_one=random.choice(self.dic["1"])
        return gacha_one
#十连
    def gacha_ten(self,up_id:list)->list:
        up=up_id
        #up.append(up_id)
        gacha_ten=[]
        for _ in range(9):  # 前9连
            gacha_ten.append(self.gacha_one(up_id))
        pick=random.randint(0,999)
        if pick<30:
            if pick<=7:
                if UNKNOWN in up:#无up
                    gacha_ten.append(random.choice(self.dic["3"]))
                else:#有up
                    gacha_ten.append(str(random.choice(up))) 
                    while gacha_ten[-1] not in self.dic["3"]:
                        del(gacha_ten[-1])
                        gacha_ten.append(str(random.choice(up)))  
            else:
                gacha_ten.append(random.choice(self.dic["3"]))
        else :
            flag=False
            for i in up :
                if i in self.dic["2"]:
                    flag=True
                    break
            if not flag:#无up
                gacha_ten.append(random.choice(self.dic["2"]))
            else:#有up
                gacha_ten.append(str(random.choice(up))) 
                while gacha_ten[-1] not in self.dic["2"]:
                    
                    del(gacha_ten[-1])
                    gacha_ten.append(str(random.choice(up)))
        return gacha_ten
#一井
    def gacha_jing(self,up_id:list)->list:
        gacha_jing=[]
        gacha=[]
        two_star=0
        one_star=0
        for _ in range(20):
            gacha_jing.append(self.gacha_ten(up_id))
        for ten in gacha_jing:
            for one in ten:
                if str(one) in self.dic["3"]:
                    gacha.append(one)
                elif str(one) in self.dic["2"]:
                    two_star=two_star+1
                else:
                    one_star=one_star+1
        return gacha,two_star,one_star

class UmaSupGacha(object):

    def __init__(self):
        super().__init__()
        self.load_pool()

    def load_pool(self):

        try:
            self.dic=Uma_res().rare_id_dict
            #self.uma_name_path = os.path.join(os.path.dirname(__file__), 'uma_gacha.json')
            #with open(self.uma_name_path, "w",encoding="utf-8") as f:
            #    f.write(json.dumps(self.dic, ensure_ascii=False, indent=4, separators=(',', ':')))    
            logger.info(f'uma-gacha-support初始化成功')
        except Exception as e:
            logger.error(f'uma-gacha-support初始化失败 {e}')
#单抽
    def gacha_one(self,up_id:list):
        up=up_id
        #up.append(up_id)
        pick=random.randint(0,999)
        if pick<30:
            if pick<=7:
                if UNKNOWN in up:
                    gacha_one=random.choice(self.dic["SSR"])
                else:
                    gacha_one=str(random.choice(up))
                    while gacha_one not in self.dic["SSR"]:
                        gacha_one=str(random.choice(up)) 
            else:
                gacha_one=random.choice(self.dic["SSR"])
        elif pick<180:
            if pick<75:
                flag=False
                for i in up :
                    if i in self.dic["SR"]:
                        flag=True
                        break
                if not flag:#无up
                    gacha_one=random.choice(self.dic["SR"])
                else:#有up
                    gacha_one=str(random.choice(up)) 
                    while gacha_one not in self.dic["SR"]:
                        gacha_one=str(random.choice(up)) 
            else :
                gacha_one=random.choice(self.dic["SR"])
        else :
            gacha_one=random.choice(self.dic["R"])
        return gacha_one
#十连
    def gacha_ten(self,up_id:list)->list:
        up=up_id
        #up.append(up_id)
        gacha_ten=[]
        for _ in range(9):  # 前9连
            gacha_ten.append(self.gacha_one(up_id))
        pick=random.randint(0,999)
        if pick<30:
            if pick<=7:
                if UNKNOWN in up:#无up
                    gacha_ten.append(random.choice(self.dic["SSR"]))
                else:#有up
                    gacha_ten.append(str(random.choice(up))) 
                    while gacha_ten[-1] not in self.dic["SSR"]:
                        del(gacha_ten[-1])
                        gacha_ten.append(str(random.choice(up)))
        else :
            flag=False
            for i in up :
                if i in self.dic["SR"]:
                    flag=True
                    break
            if not flag:#无up
                gacha_ten.append(random.choice(self.dic["SR"]))
            else:#有up
                gacha_ten.append(str(random.choice(up))) 
                while gacha_ten[-1] not in self.dic["SR"]:
                    del(gacha_ten[-1])
                    gacha_ten.append(str(random.choice(up)))
        return gacha_ten
#一井
    def gacha_jing(self,up_id:list)->list:
        gacha_jing=[]
        gacha=[]
        two_star=0
        one_star=0
        for _ in range(20):
            gacha_jing.append(self.gacha_ten(up_id))
        for ten in gacha_jing:
            for one in ten:
                if str(one) in self.dic["SSR"]:
                    gacha.append(one)
                elif str(one) in self.dic["SR"]:
                    two_star=two_star+1
                else:
                    one_star=one_star+1
        return gacha,two_star,one_star
                
class Up_pool():

    def __init__(self):
        super().__init__()
        self.get_pool_res()
#获取卡池资源
    def get_pool_res(self):
        self.pool_data_path = os.path.join(os.path.dirname(__file__), 'pool_data.json')
        if os.path.exists(self.pool_data_path):
            logger.info(f'pool_data from {self.pool_data_path}已存在')
        else :    
            self.update_pool()
        with open(self.pool_data_path,"r",encoding="utf-8")as f:
            self.pool_data_list=json.load(f)
        self.up_chara_name=self.pool_data_list[0]["chara_name"]
        self.up_card_name=self.pool_data_list[0]["card_name"]
        self.up_chara_id=[]
        for i in range(len(self.up_chara_name)):
            self.up_chara_id.append(str(guess_id(self.up_chara_name[i])[0]))
        self.up_card_id=[]
        for i in self.pool_data_list[0]["card_img_altt"]:
            m=i.split(" ")[2]
            i=m.split(".")[0]
            self.up_card_id.append(i)
        
        self.up_time=self.pool_data_list[0]["time"]#.replace("\n","")

        self.up_chara_pool=self.pool_data_list[0]["chara_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'chara_pool_img.png')
        if not os.path.exists(save_path):
            rsp = requests.get(self.pool_data_list[0]["chara_pool_img"], stream=True, timeout=5).content
            with open(save_path,"wb")as fp:
                    fp.write(rsp) 
        self.up_chara_pool_img=save_path

        self.up_card_pool=self.pool_data_list[0]["card_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'card_pool_img.png')
        if not os.path.exists(save_path):
            rsp = requests.get(self.pool_data_list[0]["card_pool_img"], stream=True, timeout=5).content
            with open(save_path,"wb")as fp:
                    fp.write(rsp) 
        self.up_card_pool_img=save_path
#更新卡池
    def update_pool(self):
        url="https://wiki.biligame.com/umamusume/%E5%8D%A1%E6%B1%A0"
        res=requests.get(url).text
        data= pq(res)
        data_list=data(".mw-parser-output>table>tbody>tr")
        pool_data_list=[]
        i=1
        for one in data_list:
            tr=pq(one)
            td=tr("td")
            if i==2:
                #pool=td.eq(2)(".center div>a")
                chara=td.eq(3)(".popup>span>div>a")
                chara_name_list=[]
                chara_img_alt_list=[]
                for a in chara:
                    j=pq(a)
                    chara_name_list.append(j.attr("title"))
                    chara_img_alt_list.append(j("img").attr("alt"))
                pool_data_item={
                    "time":td.eq(0).text(),
                    "chara_type":td.eq(1).text(),
                    "chara_pool_title":td.eq(2)(".center div>a").attr("title"),
                    "chara_pool_img":td.eq(2)(".center div>a")("img").attr("src"),
                    "chara_name":chara_name_list,
                    "chara_img_alt":chara_img_alt_list,
                }
                i=1
            else:
                #pool=td.eq(1)(".center div>a")
                card=td.eq(2)(".popup>span>div>a")
                card_name_list=[]
                card_img_alt_list=[]
                for a in card:
                    j=pq(a)
                    card_name_list.append(j.attr("title"))
                    card_img_alt_list.append(j("img").attr("alt"))
                pool_data_item={
                    "card_type":td.eq(0).text(),
                    "card_pool_title":td.eq(1)(".center div>a").attr("title"),
                    "card_pool_img":td.eq(1)(".center div>a")("img").attr("src"),
                    "card_name":card_name_list,
                    "card_img_altt":card_img_alt_list,
                }
                i=2
            pool_data_list.append(pool_data_item)
        pool_data_list=pool_data_list[1:]
        temp=pool_data_list[::2 ]
        j=0
        for i in temp:
            i.update(pool_data_list[1::2 ][j])
            j=j+1
        pool_data_list=temp  
        with open(self.pool_data_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(pool_data_list, ensure_ascii=False, indent=4, separators=(',', ':')))

uppool = Up_pool()  
gacha = UmaGacha()  
supgacha = UmaSupGacha()         
