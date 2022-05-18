from cmath import pi
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

    def __init__(self,type):
        self.type=type
        super().__init__()
        self.load_pool()

    def load_pool(self):

        try:
            if self.type=="chara":
                self.dic=Uma_res().star_id_dict
                self.rare=["3","2","1"]
            elif self.type=="support_card":
                self.dic=Uma_res().rare_id_dict
                self.rare=["SSR","SR","R"]
            else:
                logger.error(f'uma-gacha初始化失败')
            logger.info(f'uma_gacha_{self.type}初始化成功')
        except Exception as e:
            logger.error(f'uma_gacha初始化失败 {e}')
#单抽
    def gacha_one(self,up_id:list):
        up=up_id
        #up.append(up_id)
        pick=random.uniform(0,999)
        up3=0
        up2=0
        for i in up :
            if i in self.dic[self.rare[0]]:
                up3+=1#三星up数量
            elif i in self.dic[self.rare[0]]:
                up2+=1#两星up数量
        if pick<30:#出3星
            if up3>=2 and pick<=14:
                gacha_one=str(random.choice(up)) 
            elif up3==1 and pick<=7:
                gacha_one=str(random.choice(up))
            else:
                gacha_one=random.choice(self.dic[self.rare[0]]) 
            while gacha_one not in self.dic[self.rare[0]]:
                gacha_one=str(random.choice(up)) 
        elif pick<180: #出2星
            if up2>=1 and pick<48.75:
                gacha_one=str(random.choice(up)) 
                while gacha_one not in self.dic[self.rare[1]]:
                    gacha_one=str(random.choice(up))    
            else:
                gacha_one=random.choice(self.dic[self.rare[1]])
        else:#出1星
            gacha_one=random.choice(self.dic[self.rare[2]])  
        return gacha_one
#十连
    def gacha_ten(self,up_id:list)->list:
        up=up_id
        #up.append(up_id)
        gacha_ten=[]
        for _ in range(9):  # 前9连
            gacha_ten.append(self.gacha_one(up_id))
        pick=random.uniform(0,999)
        up3=0
        up2=0    
        for i in up :
            if i in self.dic[self.rare[0]]:
                up3+=1#三星up数量
            elif i in self.dic[self.rare[1]]:
                up2+=1#两星up数量
        if pick<30:
            if up3>=2 and pick<=14:
                gacha_ten.append(str(random.choice(up))) 
            elif up3==1 and pick<=7:
                gacha_ten.append(str(random.choice(up))) 
            else:
                gacha_ten.append(random.choice(self.dic[self.rare[0]])) 
            while gacha_ten[-1] not in self.dic[self.rare[0]]:
                del(gacha_ten[-1])
                gacha_ten.append(str(random.choice(up)))  
        else :
            if up2>=1 and pick<151.25:
                gacha_ten.append(str(random.choice(up))) 
                while gacha_ten[-1] not in self.dic[self.rare[1]]:
                    del(gacha_ten[-1])
                    gacha_ten.append(str(random.choice(up)))  
            else:
                gacha_ten.append(random.choice(self.dic[self.rare[1]]))
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
                if str(one) in self.dic[self.rare[0]]:
                    gacha.append(one)
                elif str(one) in self.dic[self.rare[1]]:
                    two_star=two_star+1
                else:
                    one_star=one_star+1
        return gacha,two_star,one_star

#从卡池页获取#暂时废弃
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
        if len(self.up_chara_name)>0:
            for i in range(len(self.up_chara_name)):
                self.up_chara_id.append(str(guess_id(self.up_chara_name[i])[0]))
        else:
            self.up_chara_id.append(str(UNKNOWN))
        self.up_card_id=[]
        if len(self.pool_data_list[0]["card_img_altt"])>0:
            for i in self.pool_data_list[0]["card_img_altt"]:
                m=i.split(" ")[2]
                i=m.split(".")[0]
                self.up_card_id.append(i)
        else:
            self.up_card_id.append(str(UNKNOWN))
        
        self.up_time=self.pool_data_list[0]["time"]#.replace("\n","")

        self.up_chara_pool=self.pool_data_list[0]["chara_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'chara_pool_img.png')
        #if not os.path.exists(save_path):
        rsp = requests.get(self.pool_data_list[0]["chara_pool_img"], stream=True, timeout=5).content
        with open(save_path,"wb")as fp:
            fp.write(rsp) 
        self.up_chara_pool_img=save_path

        self.up_card_pool=self.pool_data_list[0]["card_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'card_pool_img.png')
        #if not os.path.exists(save_path):
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

#从首页获取
class Up_Pool():

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
        self.up_chara_name=self.pool_data_list["chara_name"]
        self.up_card_name=self.pool_data_list["card_name"]
        self.up_chara_id=[]
        if len(self.up_chara_name)>0:
            for i in range(len(self.up_chara_name)):
                self.up_chara_id.append(str(guess_id(self.up_chara_name[i])[0]))
            print(self.up_chara_id)
        else:
            self.up_chara_id.append(str(UNKNOWN))
        self.up_card_id=[]
        if len(self.pool_data_list["card_img_altt"])>0:
            for i in self.pool_data_list["card_img_altt"]:
                m=i.replace(" ","_")
                m=i.split("_")[2]
                i=m.split(".")[0]
                dic=Uma_res().rare_id_dict
                if i in dic["SSR"]or i in dic["SR"]or i in  dic["R"]:
                    self.up_card_id.append(i)
            print(self.up_card_id)
        else:
            self.up_card_id.append(str(UNKNOWN))
        
        self.up_time=self.pool_data_list["time"]#.replace("\n","")

        self.up_chara_pool=self.pool_data_list["chara_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'chara_pool_img.png')
        #if not os.path.exists(save_path):
        rsp = requests.get(self.pool_data_list["chara_pool_img"], stream=True, timeout=5).content
        with open(save_path,"wb")as fp:
            fp.write(rsp) 
        self.up_chara_pool_img=save_path

        self.up_card_pool=self.pool_data_list["card_pool_title"]
        save_path=os.path.join(os.path.dirname(__file__), 'card_pool_img.png')
        #if not os.path.exists(save_path):
        rsp = requests.get(self.pool_data_list["card_pool_img"], stream=True, timeout=5).content
        with open(save_path,"wb")as fp:
            fp.write(rsp) 
        self.up_card_pool_img=save_path
#更新卡池
    def update_pool(self):
        url = "https://wiki.biligame.com/umamusume/%E9%A6%96%E9%A1%B5"
        res = requests.get(url).text
        data = pq(res)
        data_list = data("body>div>#content>#bodyContent>#mw-content-text")
        data_list = str(data_list)
        data = pq(data_list)
        pool_data = data("#mw-content-text>div>div>div").eq(2)
        data = pq(pool_data)
        #pool_data = data("div>div>div>div>div>center>div>a")
        chara_name_list=[]
        chara = data("div>div>div>div p a")
        for a in chara:
            j=pq(a)
            chara_name_list.append(j.attr("title"))

        pool_name=[]
        pool = data("div>div>div>div p .NotStart")
        for a in pool:
            j=pq(a).text()
            src='距离(.*?)开始'
            pool_name.append(re.findall(src,j,re.M))

        card_name_list=[]
        card_img_altt=[]
        card = data("div>div>div>div>div>center>div>a")
        for a in card :
            j=pq(a)
            card_name_list.append(j.attr("title"))
            j=str(j)
            src='70px-Support_thumb_(.*?).png"'
            alt = re.findall(src,j,re.S)
            img_alt=f"Support_thumb_{alt[0]}.png"
            card_img_altt.append(img_alt)
        time=f'{data("div>div>div>div p>span").eq(0).attr("data-start")}\n~\n{data("div>div>div>div p>span").eq(0).attr("data-end")}'
        pool_data_item={
                            "time":time,
                            "chara_pool_title":pool_name[0][0],
                            "chara_pool_img":data("div>div>div>div>.center>div").eq(0)("img").attr("src"),
                            "chara_name":chara_name_list,
                            "card_pool_title":pool_name[1][0],
                            "card_pool_img":data("div>div>div>div>.center>div").eq(1)("img").attr("src"),
                            "card_name":card_name_list,
                            "card_img_altt":card_img_altt,
                        }
        with open(self.pool_data_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(pool_data_item, ensure_ascii=False, indent=4, separators=(',', ':')))


uppool = Up_Pool()  
gacha = UmaGacha(type="chara")  
#supgacha = UmaSupGacha()         
supgacha = UmaGacha(type="support_card") 