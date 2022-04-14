'''赛马娘的游戏数据'''

'''角色名称

遵照格式： id: [wiki官译简体, 日文原名, 英文名(罗马音), (B服官译), 常见别称, 带错别字的别称等] （<-依此顺序）
若暂无台服官译则用日文原名占位，一律使用半角括号
'''
import json
import os



CHARA_NAME = {}


class Uma_data:

    def __init__(self) -> None:
        
        self.uma_name_path = os.path.join(os.path.dirname(__file__), 'dict_id_name.json')
        self.__load_uma_data()
        self.__selfcheck()
    
    def __selfcheck(self) -> None:
        for id in CHARA_NAME:
            if "" in CHARA_NAME[int(id)]:
                CHARA_NAME[int(id)].remove("")
        self.__save_uma_data()

    def __load_uma_data(self) -> None:
        # load CHARA_NAME
        with open(self.uma_name_path , 'r', encoding='utf-8') as f:
            chara_name_str = json.load(f)
        global CHARA_NAME 
        for id in chara_name_str:
            CHARA_NAME[int(id)] = chara_name_str[id]

    def __save_uma_data(self) -> None:
        # save CHARA_NAME
        with open(self.uma_name_path, 'w+', encoding='utf-8') as f:
            json.dump(CHARA_NAME, f, indent=4, ensure_ascii=False)

    def check_nickname(self, id: int, nickname: str):
        '''
        Return true if nickname already existed.
        '''
        if id not in CHARA_NAME:
            return None
        nicknames = CHARA_NAME[id]
        if nickname in nicknames:
            return True
        else:
            return False

    def add_chara(self, id: int, names: list) -> None:
        CHARA_NAME[id] = names
        self.__save_uma_data()

    def add_nickname(self, id: int, nickname: str) -> None:
        CHARA_NAME[id].append(nickname)
        self.__save_uma_data()

uma_data = Uma_data()
#print(CHARA_NAME)


