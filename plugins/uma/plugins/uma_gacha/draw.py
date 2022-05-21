import random
from PIL import Image
from plugins.uma import uma_res_data




star_id_dic=uma_res_data.STAR_ID_DICT
rare_id_dic=uma_res_data.RARE_ID_DICT   
#print (star_id_dic)
#uma_backgroud_dir = "resources\\uma\\img\\gacha\\bg\\uma_back.png"
uma_support_backgroud_one_dir="resources\\uma\\img\\gacha\\bg\\supportcard_back_one.png"
uma_support_backgroud_dir="resources\\uma\\img\\gacha\\bg\\supportcard_back.png"

star_dir ='resources\\uma\\img\\gacha\\stars'

uma_backgroud_one_dir= "resources\\uma\\img\\gacha\\bg\\uma_back_one.png"
uma_backgroud_dir= "resources\\uma\\img\\gacha\\bg\\uma_back.png"

def load_icon(id: str, size: float = 1.0) -> Image:

    uma_res_data.uma_data.chara_icon_download(id)
    icon_dir = f'resources\\uma\\img\\unit\\icon_unit_{id}.png'
    im = Image.open(icon_dir)
    icon = im.convert("RGBA")
    return icon

def load_card(id: str, size: float = 1.0) -> Image:

    uma_res_data.uma_data.support_card_download(id)
    card_dir = f'resources\\uma\\img\\support_card\\Support_thumb_{id}.png'
    im = Image.open(card_dir)
    card = im.convert("RGBA")
    return card


class Draw():
    #十连
    def draw_ten(self,data:list):
        
        im = Image.open(uma_backgroud_dir).convert('RGBA')  
        base_position = [[89, 221], [345, 221], [611, 221], [193, 480], [490, 480], [89, 221 + 518], [345, 221 + 518],
                         [611, 221 + 518], [193, 480 + 518], [490, 480 + 518]]                     
        for i in range(len(data)):
            b_x = base_position[i][0]
            b_y = base_position[i][1]
            icon = load_icon(data[i])
            if icon is None:
                continue
            im.paste(icon, (b_x, b_y),icon)
            star=0 
            for key, value in star_id_dic.items():
                if data[i] in value:
                    star=key              
                    if int(key)==int(3):
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\角色卡彩框.png").convert('RGBA')
                        im.paste(imgt, (b_x, b_y),imgt)

            stardir =f"{star_dir}\\{int(star)}.png" 
            star_img = Image.open(stardir).convert('RGBA').resize((136, 36))
            im.paste(star_img,( b_x + 31, b_y + 204),star_img)
            if star=="3"or star=="2":
                for j in range(random.randint(3,5)):
                    size=random.randint(20,80)
                    imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{star}\\{star}.png").convert('RGBA').resize((size, size))
                    im.paste(imgt, (
                        b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                        b_y+random.randint(0,180)+60-size
                        ),imgt)
        im = im.convert('RGB')
        #rdname = f"{random.randint(100000, 999999)}.jpg"
        #im.save(f"resources\\img\\temp\\{rdname}", quality=90)
        return im
    #单抽
    def draw_one(self,data):
        im = Image.open(uma_backgroud_one_dir).convert('RGBA').resize((900, 900))  
        #print(size(im))
        b_x=350
        b_y=290
        icon = load_icon(data)                    
        if icon is None:
            return
        im.paste(icon, (b_x, b_y),icon)
        star=0
        for key, value in star_id_dic.items():
            if data in value:
                star=key              
                if int(key)==int(3):
                    imgt = Image.open(f"resources\\uma\\img\\gacha\\角色卡彩框.png").convert('RGBA')
                    im.paste(imgt, (b_x, b_y),imgt)

        stardir =f"{star_dir}\\{int(star)}.png" 
        star = Image.open(stardir).convert('RGBA').resize((136, 36))
        im.paste(star,( b_x + 31, b_y + 204),star)
        im = im.convert('RGB')
        if star=="3"or star=="2":
            for j in range(random.randint(3,5)):
                size=random.randint(20,80)
                imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{star}\\{star}.png").convert('RGBA').resize((size, size))
                im.paste(imgt, (
                    b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                    b_y+random.randint(0,180)+60-size
                    ),imgt)
        #rdname = f"{random.randint(100000, 999999)}.jpg"
        #im.save(f"resources\\img\\temp\\{rdname}", quality=90)
        return im
    #百连
    def draw_tenten(self,data:list):
        im = Image.open(uma_backgroud_dir).convert('RGBA')  
        base_position = [[89, 221], [345, 221], [611, 221], [193, 480], [490, 480], [89, 221 + 518], [345, 221 + 518],
                         [611, 221 + 518], [193, 480 + 518], [490, 480 + 518]]                    
        for i in range(len(data)):
            b_x = base_position[i][0]
            b_y = base_position[i][1]
            icon = load_icon(data[i])
            if icon is None:
                continue
            im.paste(icon, (b_x, b_y),icon)
            star=0 
            for key, value in star_id_dic.items():
                if data[i] in value:
                    star=key              
                    if int(key)==int(3):
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\角色卡彩框.png").convert('RGBA')
                        im.paste(imgt, (b_x, b_y),imgt)

            stardir =f"{star_dir}\\{int(star)}.png" 
            star_img = Image.open(stardir).convert('RGBA').resize((136, 36))
            im.paste(star_img,( b_x + 31, b_y + 204),star_img)
            if star=="3"or star=="2":
                for j in range(random.randint(3,5)):
                    size=random.randint(20,80)
                    imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{star}\\{star}.png").convert('RGBA').resize((size, size))
                    im.paste(imgt, (
                        b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                        b_y+random.randint(0,180)+60-size
                        ),imgt)
            
        im = im.convert('RGB')
        #rdname = f"{random.randint(100000, 999999)}.jpg"
        #im.save(f"resources\\img\\temp\\{rdname}", quality=90)
        return im


    #支援卡单抽
    def draw_support_one(self,data)->Image:
        im = Image.open(uma_support_backgroud_one_dir).convert('RGBA').resize((900, 900))  
        #print(size(im))
        b_x=350
        b_y=290
        card = load_card(data)                    
        if card is None:
            return
        im.paste(card, (b_x, b_y),card)
        for key in rare_id_dic:
            if str(data) in rare_id_dic[key]:
                rare=key
                imgt = Image.open(f"resources\\uma\\img\\gacha\\rare\\{rare}.png").convert('RGBA')
                im.paste(imgt, (b_x+15, b_y),imgt)
                if rare=="SSR":
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\支援卡彩框.png").convert('RGBA')
                        im.paste(imgt, (b_x, b_y),imgt)
                if rare=="SSR"or rare=="SR":
                    for i in range(random.randint(3,7)):
                        size=random.randint(20,100)
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{rare}\\{rare}.png").convert('RGBA').resize((size, size))
                        im.paste(imgt, (
                            b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                            b_y+random.randint(-10,200)+60-size
                            ),imgt)

        im = im.convert('RGB')
        return im
    #支援卡十连
    def draw_support_ten(self,data:list)->Image:
        im = Image.open(uma_support_backgroud_dir).convert('RGBA')  
        base_position = [[109, 174], [358, 174], [609, 174], [217, 458], [468, 458], [109, 174 + 567], [358, 174 + 567],
                         [609, 174 + 567], [217, 458 + 567], [468, 458 + 567]]
        for i in range(len(data)):
            b_x = base_position[i][0]
            b_y = base_position[i][1]
            card = load_card(data[i])
            if card is None:
                continue
            im.paste(card, (b_x, b_y),card)
            for rare in rare_id_dic:
                if data[i] in rare_id_dic[rare]:
                    imgt = Image.open(f"resources\\uma\\img\\gacha\\rare\\{rare}.png").convert('RGBA')
                    im.paste(imgt, (b_x+15, b_y),imgt)
                    if rare=="SSR":
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\支援卡彩框.png").convert('RGBA')
                        im.paste(imgt, (b_x, b_y),imgt)
                    if rare=="SSR"or rare=="SR":
                        for j in range(random.randint(3,7)):
                            size=random.randint(20,100)
                            imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{rare}\\{rare}.png").convert('RGBA').resize((size, size))
                            im.paste(imgt, (
                                b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                                b_y+random.randint(-10,200)+60-size
                                ),imgt)
        im = im.convert('RGB')
        return im
    #支援卡百连
    def draw_support_tenten(self,data:list)->Image:
        im = Image.open(uma_support_backgroud_dir).convert('RGBA')  
        base_position = [[109, 174], [358, 174], [609, 174], [217, 458], [468, 458], [109, 174 + 567], [358, 174 + 567],
                         [609, 174 + 567], [217, 458 + 567], [468, 458 + 567]]
        for i in range(len(data)):
            b_x = base_position[i][0]
            b_y = base_position[i][1]
            card = load_card(data[i])
            if card is None:
                continue
            im.paste(card, (b_x, b_y),card)
            for rare in rare_id_dic:
                if data[i] in rare_id_dic[rare]:
                    imgt = Image.open(f"resources\\uma\\img\\gacha\\rare\\{rare}.png").convert('RGBA')
                    im.paste(imgt, (b_x+15, b_y),imgt)
                    if rare=="SSR":
                        imgt = Image.open(f"resources\\uma\\img\\gacha\\支援卡彩框.png").convert('RGBA')
                        im.paste(imgt, (b_x, b_y),imgt)
                    if rare=="SSR"or rare=="SR":
                        for j in range(random.randint(3,7)):
                            size=random.randint(20,100)
                            imgt = Image.open(f"resources\\uma\\img\\gacha\\effect\\{rare}\\{rare}.png").convert('RGBA').resize((size, size))
                            im.paste(imgt, (
                                b_x+random.choice([random.randint(-10,10)+60-size,random.randint(140,160)+60-size]),
                                b_y+random.randint(-10,200)+60-size
                                ),imgt)
               
        im = im.convert('RGB')
        return im

draw=Draw()       