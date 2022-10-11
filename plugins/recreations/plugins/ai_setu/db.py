import base64
import os
import sqlite3

XP_DB_PATH = os.path.expanduser('~/.hoshino/ai_setu2.db')
class XpCounter:
    def __init__(self):
        os.makedirs(os.path.dirname(XP_DB_PATH), exist_ok=True)
        self._create_table()

    def _connect(self):
        return sqlite3.connect(XP_DB_PATH)

    def _create_table(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS XP_NUM
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           KEYWORD         TEXT   NOT NULL,
                           NUM             INT    NOT NULL,
                           PRIMARY KEY(GID,UID,KEYWORD));''')
        except:
            raise Exception('创建表发生错误')

    def _add_xp_num(self, gid, uid, keyword):
        try:
            num = self._get_xp_num(gid, uid, keyword)
            if num == None:
                num = 0
            num += 1
            with self._connect() as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO XP_NUM (GID,UID,KEYWORD,NUM) \
                                VALUES (?,?,?,?)", (gid, uid, keyword, num)
                )
        except:
            raise Exception('更新表发生错误')

    def _get_xp_num(self, gid, uid, keyword):
        try:
            r = self._connect().execute("SELECT NUM FROM XP_NUM WHERE GID=? AND UID=? AND KEYWORD=?", (gid, uid, keyword)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')


    def _get_xp_list_group(self, gid, num):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT KEYWORD,NUM FROM XP_NUM WHERE GID={gid} ORDER BY NUM desc LIMIT {num}").fetchall()
        return r if r else {}

    def _get_xp_list_personal(self, gid, uid, num):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT KEYWORD,NUM FROM XP_NUM WHERE GID={gid} AND UID={uid} ORDER BY NUM desc LIMIT {num}").fetchall()
        return r if r else {}

    def _get_xp_list_kwd_group(self, gid, num):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT KEYWORD FROM XP_NUM WHERE GID={gid} ORDER BY NUM desc LIMIT {num}").fetchall()
        return r if r else {}

    def _get_xp_list_kwd_personal(self, gid, uid, num):
        with self._connect() as conn:
            r = conn.execute(
                f"SELECT KEYWORD FROM XP_NUM WHERE GID={gid} AND UID={uid} ORDER BY NUM desc LIMIT {num}").fetchall()
        return r if r else {}

def get_xp_list_group(gid,num=10):
    XP = XpCounter()
    xp_list = XP._get_xp_list_group(gid, num)
    if len(xp_list)>0:
        data = sorted(xp_list,key=lambda cus:cus[1],reverse=True)
        new_data = []
        for xp_data in data:
            keyword, num = xp_data
            new_data.append((keyword,num))
        rankData = sorted(new_data,key=lambda cus:cus[1],reverse=True)
        return rankData
    else:
        return []

def get_xp_list_personal(gid,uid,num=10):
    XP = XpCounter()
    xp_list = XP._get_xp_list_personal(gid,uid,num)
    if len(xp_list)>0:
        data = sorted(xp_list,key=lambda cus:cus[1],reverse=True)
        new_data = []
        for xp_data in data:
            keyword, num = xp_data
            new_data.append((keyword,num))
        rankData = sorted(new_data,key=lambda cus:cus[1],reverse=True)
        return rankData
    else:
        return []

def get_xp_list_kwd_group(gid,num=10):
    XP = XpCounter()
    xp_list_kwd = XP._get_xp_list_kwd_group(gid, num)
    if len(xp_list_kwd)>0:
        return xp_list_kwd
    else:
        return []

def get_xp_list_kwd_personal(gid,uid,num=10):
    XP = XpCounter()
    xp_list_kwd = XP._get_xp_list_kwd_personal(gid,uid,num)
    if len(xp_list_kwd)>0:
        return xp_list_kwd
    else:
        return []


def add_xp_num(gid,uid,keyword):
    XP = XpCounter()
    XP._add_xp_num(gid,uid,keyword)



######################################################################
