import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List, Set, Tuple, Type, Union, Optional, TYPE_CHECKING
from nonebot import  logger
from nonebot.rule import Rule, command, keyword, regex
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.event import MessageEvent
from . import get_event_gid 



SERVICE_DIR = Path(".") / "data" / "service"
SERVICES_DIR = SERVICE_DIR / "services"
os.makedirs(SERVICE_DIR, exist_ok=True)
os.makedirs(SERVICES_DIR, exist_ok=True)

GLOBAL_SERVICE_DIR = SERVICE_DIR / "global_service"
os.makedirs(GLOBAL_SERVICE_DIR, exist_ok=True)

CD_DIR = Path(".") / "data" / "CD" 
os.makedirs(CD_DIR, exist_ok=True)


"""
    集成一套服务管理，对功能信息进行持久化
    服务文件结构：
    {
        "service": "Service name",
        "docs": "Main helps and commands",
        "cmd_list": {
            "/cmd0": {
                "type": "Command type",
                "docs": "Command help",
                "aliases": ["More trigger ways."]
            }
        },
        "enabled": True,
        "only_admin": False,
        "disable_user": [],
        "disable_group": []
    }
"""


class ServiceInfo(BaseModel):
    service: str 
    docs: str
    cmd_list: dict
    service_type: str
    enabled: bool
    only_admin: bool
    cd_time:int = 60 
    black_gid: list
    white_gid: list
    black_user: list
    white_user: list

class Service:

    def __init__(
            self,
            service: str,
            docs: str = None,
            service_type: str = None,
            only_admin: bool = False,

    ):
        self.service = service
        self.docs = docs
        self.service_type = service_type
        self.only_admin = only_admin
 

    def _generate_service_config(self, service: str = None, docs: str = None, service_type: str = None) -> None:
        if not service:
            service = self.service
        if not docs:
            docs = self.docs or str()
        if not service_type:
            service_type = self.service_type

        path = SERVICES_DIR /  f"{service}.json"
        data = ServiceInfo(
            service = service,
            docs = docs,
            cmd_list = dict(),
            service_type = service_type,
            enabled = True,
            only_admin = self.only_admin,
            cd_time = 60,
            black_gid = list(),
            black_user = list(),
            white_gid = list(),
            white_user = list(),
        )
        try:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps(data.dict(), indent=4,ensure_ascii=False))
        except IOError:
            raise IOError("Write service info failed!")

    def save_service(self, service_data: dict, service: str = None, service_type: str = None) -> None:
        if not service:
            service = self.service
        if not service_type:
            service_type = self.service_type

        path = SERVICES_DIR / f"{service_type}" / f"{service}.json"
        if not path.is_file():
            self._generate_service_config()

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(service_data, indent=4,ensure_ascii=False))

    def load_service(self, service: str = None, service_type: str = None) -> dict:
        if not service:
            service = self.service
        if not service_type:
            service_type = self.service_type
        

        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            self._generate_service_config()

        try:
            data = json.loads(path.read_bytes())
        except IOError:
            with open(path, "w", encoding="utf-8") as w:
                w.write(json.dumps({}, indent=4,ensure_ascii=False))
            self._generate_service_config()
            data = json.loads(path.read_bytes())
        return data

    def _save_cmds(self, cmds: dict) -> None:
        data = self.load_service(self.service)
        temp_data: dict = data["cmd_list"]
        temp_data.update(cmds)
        self.save_service(data)

    def _load_cmds(self) -> dict:
        path = SERVICES_DIR / f"{self.service}.json"
        if not path.is_file():
            self._generate_service_config()

        data = json.loads(path.read_bytes())
        return data["cmd_list"]
    

    async def rule(self,event: MessageEvent ) -> bool:
        path = SERVICES_DIR /  f"{self.service}.json" 
        if not path.is_file():
            self._generate_service_config()
        with open(path, "r", encoding="utf-8") as r:
            data = json.loads(r.read())
        global_enabled = data.get("enabled", True)
        black_user = data.get("black_user", list())
        black_gid = data.get("black_gid", list())
        white_user = data.get("white_user", list())
        white_gid = data.get("white_gid", list())

        if (not global_enabled) or (event.get_user_id() in black_user) or (get_event_gid(event) in black_gid):
            print("鉴定为不可以")
            return False
        elif (event.get_user_id() in white_user) or (get_event_gid(event) in white_gid):
            return self.check_cd()
        else:
            print("鉴定为可以")
            return True


    @staticmethod
    def readJson(service_name:str):
        path = CD_DIR + f"/{service_name}_usercd.json"
        try:
            with open(path, "r") as f_in:
                data = json.load(f_in)
                f_in.close()
                return data
        except FileNotFoundError:
            try:
                os.makedirs(path)
            except FileExistsError:
                pass
            with open(path + f"{service_name}_usercd.json", mode="w") as f_out:
                json.dump({}, f_out)

    @staticmethod
    def writeJson(qid: str, time: int, mid: int, data: dict, service_name: str, num:int = 0):
        path = CD_DIR + f"/{service_name}_usercd.json"
        try:
            data[qid] = [time, mid,num]
        except:    
            data = {}
            with open(path, "w") as f_out:
                json.dump(data, f_out)
            f_out.close()
            data[qid] = [time, mid, num]
        with open(path, "w") as f_out:
            json.dump(data, f_out)
            f_out.close()

    @staticmethod
    def removeJson(qid: str, service_name:str):
        path = CD_DIR + f"/{service_name}_usercd.json"
        with open(path, "r") as f_in:
            data = json.load(f_in)
            f_in.close()
        data.pop(qid)
        with open(path, "w") as f_out:
            json.dump(data, f_out)
            f_out.close()


    async def check_cd(self,bot:Bot,event:MessageEvent)->bool:
        path = SERVICES_DIR /  f"{self.service}.json" 
        if not path.is_file():
            self._generate_service_config()
        with open(path, "r", encoding="utf-8") as r:
            data = json.loads(r.read())
        cdTime = data.get("cd_time", 60)
        displaycd = data.get("displaycd", False) 
        reply = data.get("reply", True)

        data = self.readJson(self.service)
        try:
            cd = event.time - data[event.get_user_id()][0]
        except:
            cd = cdTime + 1
        try:
            num =  data[event.get_user_id()][2]
        except:
            num = 0

        if cd > cdTime: #or event.get_user_id() in nonebot.get_driver().config.superusers
            try:
                self.writeJson(event.get_user_id(), event.time, event.message_id, data, self.service)#清零次数重新计时
            except Exception as e:
                logger.warning(e)
                self.removeJson(event.get_user_id(), self.service)
            finally:
                return True
        else:
            try:
                num = num + 1
                self.writeJson(event.get_user_id(), data[event.get_user_id()][0], event.message_id, data, self.service, num)#不清零次数继续计时
                if num == 4:
                    time = event.time + 600
                    self.writeJson(event.get_user_id(), time, event.message_id, data, self.service, num)
                    await bot.send(event,f"检测到刷屏行为,禁用{cdTime - cd + 600}秒", at_sender=True)
                if  num > 4:
                    reply=False
                if reply:
                    if displaycd:
                        await bot.send(event,f"别急~  CD还有{cdTime - cd}秒", at_sender=True)
                    else:
                        await bot.send(event,f"别急~  还在CD中", at_sender=True)
            except Exception as e:
                logger.warning(e)
                self.removeJson(event.get_user_id(), self.service)
            finally:
                return False

            

class GlobalServiceInfo(BaseModel):
    black_group: list
    black_user: list

    
class ServiceTools(object):
    @staticmethod
    def save_service(service_data: dict, service: str) -> None:
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            raise IOError(
                f"Can't find service: ({service}) file.\n"
                "Please delete all file in data/service/services.\n"
                "Next reboot bot."
            )

        with open(path, "w", encoding="utf-8") as w:
            w.write(json.dumps(service_data, indent=4))

    @staticmethod
    def load_service(service: str) -> dict:
        path = SERVICES_DIR / f"{service}.json"
        if not path.is_file():
            raise IOError(
                f"Can't find service: ({service}) file.\n"
                "Please delete all file in data/service/services.\n"
                "Next reboot bot."
            )

        with open(path, "r", encoding="utf-8") as r:
            data = json.loads(r.read())
        return data

    @classmethod
    def auth_service(cls, service, user_id: str = None, group_id: str = None) -> bool:
        data = cls.load_service(service)

        auth_global = data.get("enabled", True)
        auth_user = data.get("disable_user", list())
        auth_group = data.get("disable_group", list())

        if user_id:
            if user_id in auth_user:
                return False

        if group_id:
            if group_id in auth_group:
                return False
            else:
                return True

        if not auth_global:
            return False
        else:
            return True
