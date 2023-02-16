'''赛马娘的游戏数据'''

'''角色名称
遵照格式： iD: [wiki官译简体, 日文原名, 英文名(罗马音), (B服官译), 常见别称, 带错别字的别称等] （<-依此顺序）
若暂无台服官译则用日文原名占位，一律使用半角括号
来源wiki&che
'''
import json
import os
import requests
import re
from nonebot import logger
from pyquery import PyQuery as pq
from utils import aiorequests

UNKNOWN=100101

CHARA_NAME = {}


class Uma_Data:

    def __init__(self) -> None:
        
        self.load_chara_res()
        self.load_card_res()
        self.load_uma_alias()
        self.load_pool_res()

        self.__load_uma_data()
        self.__selfcheck()
    
    def __selfcheck(self) -> None:  #检查马娘id与name（别名）数据
        for id in CHARA_NAME:
            if "" in CHARA_NAME[int(id)]:
                CHARA_NAME[int(id)].remove("")
        self.__save_uma_data()

    def __load_uma_data(self) -> None:  #加载马娘id与name（别名）数据
        # load CHARA_NAME
        self.uma_name_path = os.path.join(os.path.dirname(__file__), 'dict_id_name.json')
        with open(self.uma_name_path , 'r', encoding='utf-8') as f:
            self.chara_name_str = json.load(f)
        global CHARA_NAME 
        for id in self.chara_name_str:
            CHARA_NAME[int(id)] = self.chara_name_str[id]

    def __save_uma_data(self) -> None:  #更新马娘id与name（别名）数据
        # save CHARA_NAME
        with open(self.uma_name_path, 'w+', encoding='utf-8') as f:
            json.dump(CHARA_NAME, f, indent=4, ensure_ascii=False)

    def load_chara_res(self) -> None:    #加载角色卡资源
        self.chara_info_dict_path = os.path.join(os.path.dirname(__file__), 'chara_info_dict.json')
        if not os.path.exists(self.chara_info_dict_path):
            self.update_chara_res()
        try:
            with open(self.chara_info_dict_path, "r",encoding="utf-8") as f:
                self.chara_info_dict=json.load(f)
                f.close
            self.id_name_dict={}
            self.star_id_dict=dict()    
            for id in self.chara_info_dict:
                self.star_id_dict.setdefault(self.chara_info_dict[id]["star"],[]).append(id)
                self.id_name_dict[id]=[self.chara_info_dict[id]["cn_name"],self.chara_info_dict[id]["jp_name"]]
            logger.info(f'加载chara_info成功')
            #logger.info(f'star_id_dict(马娘)更新成功')
            #logger.info(f'id_name_dict(wiki)更新成功')
        except Exception as e:
            logger.error(f'加载chara_info失败:{e}')

    def load_card_res(self) -> None:     #加载支援卡资源
        self.card_info_dict_path = os.path.join(os.path.dirname(__file__), 'card_info_dict.json')
        if not os.path.exists(self.card_info_dict_path):
            self.update_card_res()
        try:
            with open(self.card_info_dict_path, "r",encoding="utf-8") as f:
                self.card_info_dict=json.load(f)
                f.close
            self.rare_id_dict={}   
            for id in self.card_info_dict:
                if self.card_info_dict[id]["origin"]=="卡池" or self.card_info_dict[id]["origin"]=="":
                    self.rare_id_dict.setdefault(self.card_info_dict[id]["rare"],[]).append(id)
                else:
                    continue
            logger.info(f'加载card_info成功')
            #logger.info(f'rare_id_dict(支援卡)更新成功')
        except Exception as e:
            logger.error(f'加载card_info失败:{e}')
    
    def load_uma_alias(self) -> None:    #加载角色别名
        uma_alias_path = os.path.join(os.path.dirname(__file__), 'uma_alias.json')
        if not os.path.exists(uma_alias_path):
            self.update_uma_alias()
        try:
            with open(uma_alias_path , 'r', encoding='utf-8') as f:
                    chara_name_str = json.load(f)
                    f.close
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
                f.close
            logger.info(f'加载角色别名成功')
            #logger.info(f'id_name_dict(wiki&别名)更新成功')
        except Exception as e:
            logger.error(f'加载角色别名失败')

    def load_pool_res(self) -> None: #加载卡池资源
        self.pool_data_path = os.path.join(os.path.dirname(__file__), 'pool_data.json')
        if not os.path.exists(self.pool_data_path):
            self.update_pool2()
        try:
            with open(self.pool_data_path,"r",encoding="utf-8")as f:
                self.pool_data_list=json.load(f)
                f.close

            self.up_chara_pool=self.pool_data_list["chara_pool_title"]
            self.up_card_pool=self.pool_data_list["card_pool_title"]
            self.up_chara_name=self.pool_data_list["chara_name"]
            self.up_card_name=self.pool_data_list["card_name"]
            self.up_chara_id=self.pool_data_list["chara_id"]
            
            if len(self.up_chara_name)>0:
                logger.info(f'up角色:{self.up_chara_name};id:{self.up_chara_id}')
            else:
                self.up_chara_id.append(str(UNKNOWN))

            self.up_card_id=[]
            if len(self.pool_data_list["card_img_altt"])>0:
                for i in self.pool_data_list["card_img_altt"]:
                    m=i.replace(" ","_")
                    m=i.split("_")[2]
                    i=m.split(".")[0]
                    dic=self.rare_id_dict
                    if i in dic["SSR"]or i in dic["SR"]or i in  dic["R"]:
                        self.up_card_id.append(i)
                logger.info(f'up支援卡:{self.up_card_name};id:{self.up_card_id}')
            else:
                self.up_card_id.append(str(UNKNOWN))


            save_path=os.path.join(os.path.dirname(__file__), 'chara_pool_img.png')
            #if not os.path.exists(save_path):
            rsp = requests.get(self.pool_data_list["chara_pool_img"], stream=True, timeout=5).content
            with open(save_path,"wb")as fp:
                fp.write(rsp) 
            self.up_chara_pool_img=save_path

            save_path=os.path.join(os.path.dirname(__file__), 'card_pool_img.png')
            #if not os.path.exists(save_path):
            rsp = requests.get(self.pool_data_list["card_pool_img"], stream=True, timeout=5).content
            with open(save_path,"wb")as fp:
                fp.write(rsp) 
            self.up_card_pool_img=save_path
            logger.info(f'加载卡池资源成功')
        except Exception as e:
            logger.error(f'加载卡池资源失败:{e}')


    def update_chara_res(self) -> None: #更新角色卡资源
        logger.info(f'开始更新chara_info')
        url="https://wiki.biligame.com/umamusume/%E8%B5%9B%E9%A9%AC%E5%A8%98%E5%9B%BE%E9%89%B4"
        res=requests.get(url).text
        src='data-param1="(.*?)" .*?\n<td><a href="(.*?)" title="(.*?)"><img alt="Chr icon (.*?) 01.png" src=".*?".* srcset=".*?1.5x, (.*?) 2x".*/></a>\n</td>\n<td>.*?>.*?>(.*?)】</a>'
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
            f.close

    def update_card_res(self) -> None:  #更新支援卡资源
        logger.info(f'开始更新card_info')
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
            f.close

    def update_pool(self) -> None:  #更新马娘卡池资源
        logger.info(f'开始更新马娘卡池资源pool_data')
        url = "https://wiki.biligame.com/umamusume/%E9%A6%96%E9%A1%B5"
        res = requests.get(url).text
        data = pq(res)
        data_list = data("body>div>#content>#bodyContent>#mw-content-text")
        data_list = str(data_list)
        data = pq(data_list)
        pool_data = data("#mw-content-text>div>div>div").eq(2)
        data = pq(pool_data)
        #pool_data = data("div>div>div>div>div>center>div>a")

        pool_name=[]
        pool = data("div>div>div>div p .NotStart")
        for a in pool:
            j=pq(a).text()
            src='距离(.*?)开始'
            pool_name.append(re.findall(src,j,re.M))

        chara_name_list=[]
        chara_id_list=[]
        chara = data("div>div>div>div p a")
        for a in chara:
            j=pq(a)
            chara_name_list.append(j.attr("title"))
            j=str(j)
            src='100px-Chr_icon_.*?_(.*?)_01.png"'
            alt = re.findall(src,j,re.S)
            img_alt=alt[0]
            chara_id_list.append(img_alt)

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
                            "chara_id":chara_id_list,
                            "card_pool_title":pool_name[1][0],
                            "card_pool_img":data("div>div>div>div>.center>div").eq(1)("img").attr("src"),
                            "card_name":card_name_list,
                            "card_img_altt":card_img_altt,
                        }
        self.pool_data_path = os.path.join(os.path.dirname(__file__), 'pool_data.json')
        with open(self.pool_data_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(pool_data_item, ensure_ascii=False, indent=4, separators=(',', ':')))
            f.close

    def update_pool2(self) -> None: #更新马娘卡池资源(卡池页)
        logger.info(f'开始更新马娘卡池资源pool_data')
        url="https://wiki.biligame.com/umamusume/%E5%8D%A1%E6%B1%A0"
        res=requests.get(url).text
        data= pq(res)
        data_list=data(".mw-parser-output>table>tbody>tr")
        pool_data_path = os.path.join(os.path.dirname(__file__), 'pool_data.html')
        #with open(pool_data_path, "w",encoding="utf-8") as f:
        #    f.write(str(data_list))
        tr=pq(data_list.eq(1))
        td=tr("td")
        chara=td.eq(3)("span>span>div>a")
        time = td.eq(0).text()
        chara_pool_title = td.eq(2)(".center div>a").attr("title")
        chara_pool_img = re.findall('1.5x, (.*?) 2x',str(td.eq(2)(".center div>a")("img").attr("srcset")),re.S)[0]
        chara_name_list=[]
        chara_id_list=[]
        for a in chara:
            j=pq(a)
            chara_name_list.append(j.attr("title"))
            j=str(j)
            src='100px-Chr_icon_.*?_(.*?)_01.png"'
            alt = re.findall(src,j,re.S)
            img_alt=alt[0]
            chara_id_list.append(img_alt)
        tr=pq(data_list.eq(2))
        td=tr("td")
        card=td.eq(2)("span>span>div>a")
        card_pool_title = td.eq(1)(".center div>a").attr("title")
        card_pool_img = re.findall('1.5x, (.*?) 2x',str(td.eq(1)(".center div>a")("img").attr("srcset")),re.S)[0]
        card_name_list=[]
        card_img_alt_list=[]
        for a in card:
            j=pq(a)
            card_name_list.append(j.attr("title"))
            j=str(j)
            src='100px-Support_thumb_(.*?).png"'
            alt = re.findall(src,j,re.S)
            img_alt=f"Support_thumb_{alt[0]}.png"
            card_img_alt_list.append(img_alt)

        pool_data_item={
                            "time":time,
                            "chara_pool_title":chara_pool_title,
                            "chara_pool_img":chara_pool_img,
                            "chara_name":chara_name_list,
                            "chara_id":chara_id_list,
                            "card_pool_title":card_pool_title,
                            "card_pool_img":card_pool_img,
                            "card_name":card_name_list,
                            "card_img_altt":card_img_alt_list,
                        }
        self.pool_data_path = os.path.join(os.path.dirname(__file__), 'pool_data.json')
        with open(self.pool_data_path, "w",encoding="utf-8") as f:
            f.write(json.dumps(pool_data_item, ensure_ascii=False, indent=4, separators=(',', ':')))
            f.close

        ''' pool_data_list=[]     
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

            pool_data_list.append(pool_data_item)'''  

    def update_uma_alias(self) -> None:#更新马娘角色别名
        logger.info(f'开始更新马娘角色别名uma_alias')
        url = "https://ghproxy.com/https://github.com/chieri-bot/umamusume-alias/blob/main/uma_alias.json"
        try:
            resp = requests.get(url,timeout=20)
            uma_alias = resp.json()
            if uma_alias:
                uma_alias_path = os.path.join(os.path.dirname(__file__), 'uma_alias.json')
                with open(uma_alias_path, "w",encoding="utf-8") as f:
                    f.write(json.dumps(uma_alias, ensure_ascii=False, indent=4, separators=(',', ': ')))
                    f.close
                logger.info(f"更新马娘别名成功")
        except Exception as e:
            logger.error(f"更新马娘别名失败{e}")

    def chara_icon_download(self,id) -> None:   #下载角色卡icon
        id=str(id)
        icon_save_path = f'resources\\uma\\img\\unit\\icon_unit_{self.chara_info_dict[id]["png_name"]}.png'
        if not os.path.exists(icon_save_path):
            logger.info(f'Downloading chara icon from {self.chara_info_dict[id]["url"]}')
        else :    
            #logger.info(f'chara icon from {self.chara_info_dict[id]["cn_name"]}已存在')
            return
        try:
            rsp = requests.get(self.chara_info_dict[id]["url"], stream=True, timeout=5).content
            with open(icon_save_path,"wb")as fp:
                fp.write(rsp)    
            logger.info(f'{self.chara_info_dict[id]["cn_name"]}:{self.chara_info_dict[id]["png_name"]}.png Saved to {icon_save_path}')
        except Exception as e:
            logger.error(f'Failed to download {self.chara_info_dict[id]["cn_name"]}. {type(e)}')


    def support_card_download(self,id) -> None: #下载支援卡card
        id=str(id)
        card_save_path = f'resources\\uma\\img\\support_card\\{self.card_info_dict[id]["png_name"]}.png'
        if not os.path.exists(card_save_path):
            logger.info(f'Downloading support chard from {self.card_info_dict[id]["url"]}')
        else :    
            #logger.info(f'card icon from {self.card_info_dict[id]["cn_name"]}已存在')
            return
        try:
            rsp = requests.get(self.card_info_dict[id]["url"], stream=True, timeout=5).content
            with open(card_save_path,"wb")as fp:
                fp.write(rsp)    
            logger.info(f'{self.card_info_dict[id]["cn_name"]}:{self.card_info_dict[id]["png_name"]}.png Saved to {card_save_path}')
        except Exception as e:
            logger.error(f'Failed to download {self.card_info_dict[id]["cn_name"]}. {type(e)}')
            logger.exception(e)
        


UMA_DATA = Uma_Data()


