from nonebot import logger
import random
from plugins.uma.uma_res_data import UMA_DATA

BLACK_NAME=["100103"]
UNKNOWN = 1000

class UmaGacha(object):

    def __init__(self,type):
        self.type=type
        super().__init__()
        self.load_pool()

    def load_pool(self):

        try:
            if self.type=="chara":
                self.dic=UMA_DATA.star_id_dict
                self.rare=["3","2","1"]
            elif self.type=="support_card":
                self.dic=UMA_DATA.rare_id_dict
                self.rare=["SSR","SR","R"]
            else:
                logger.error(f'uma-gacha初始化失败')
            logger.info(f'uma_gacha_{self.type}初始化成功;{self.rare[0]}_rare:{len(self.dic[self.rare[0]])}')
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
            while gacha_one not in self.dic[self.rare[0]] or gacha_one in BLACK_NAME :
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
            while gacha_ten[-1] not in self.dic[self.rare[0]] or gacha_ten[-1] in BLACK_NAME :
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

UMAGACHA = UmaGacha(type="chara")  
SUPGACHA = UmaGacha(type="support_card") 