import os

from utils.service import Service, SERVICES_DIR, ServiceTools
import nonebot

driver = nonebot.get_driver()
config = driver.config

SERVICE_INFO_FORMAT = """
服务名：{service}
说明：{docs}
可用命令：\n{cmd_list}
是否全局启用：{enabled}
Tip: 帮助 [服务] [命令] 以查看对应命令详细信息
""".strip()

COMMAND_INFO_FORMAT = """
命令：{cmd}
类型：{cmd_type}
说明：{docs}
更多触发方式：{aliases}
""".strip()


class Helper(Service):
    def __init__(self):
        Service.__init__(self, "帮助", "bot的食用指南~")

    @staticmethod
    def menu() -> str:
        return (
            "哦呀？~需要帮助？\n"
            "关于 -查看bot基本信息\n"
            "服务列表 -以查看所有可用服务\n"
            "帮助 [服务] -以查看对应服务帮助\n"
            "Tip: 均需要at触发。菜单 以打开此页面"
        )

    @staticmethod
    def about() -> str:
        return f'你好呀~我是{config.dict().get("nickname")}~'
        # temp_list = list()
        # for i in BotSelfConfig.nickname:
        #     temp_list.append(i)
        # nickname = "、".join(map(str, temp_list))
        # return (
        #     "唔...是来认识咱的么\n"
        #     f"可以称呼咱：{nickname}\n"
        # )

    @staticmethod
    def service_list() -> str:
        files = os.listdir(SERVICES_DIR)
        temp_list = list()
        for i in files:
            service = i.replace(".json", "")
            temp_list.append(service)

        msg0 = "咱搭载了以下服务~\n"
        services = " | ".join(map(str, temp_list))
        msg0 = msg0 + services
        repo = msg0 + "\n@ 帮助 [服务] -以查看对应服务帮助"
        return repo

    @staticmethod
    def service_info(service: str) -> str:
        try:
            data = ServiceTools().load_service(service)
        except IOError:
            return "请检查是否输入错误呢..."

        service_name = data.get("service", "error")
        service_docs = data.get("docs", "error")
        service_enabled = data.get("enabled", True)

        _service_cmd_list = list(data.get("cmd_list", {"error"}))
        service_cmd_list = "\n".join(map(str, _service_cmd_list))

        repo = SERVICE_INFO_FORMAT.format(
            service=service_name,
            docs=service_docs,
            cmd_list=service_cmd_list,
            enabled=service_enabled,
        )
        return repo

    @staticmethod
    def cmd_info(service: str, cmd: str) -> str:
        try:
            data = ServiceTools().load_service(service)
        except IOError:
            return "请检查是否输入错误..."

        cmd_list: dict = data["cmd_list"]
        cmd_info = cmd_list.get(cmd, dict())
        if not cmd_info:
            return "请检查命令是否输入错误..."
        cmd_type = cmd_info.get("type", "ignore")
        docs = cmd_info.get("docs", "ignore")
        aliases = cmd_info.get("aliases", "ignore")

        repo = COMMAND_INFO_FORMAT.format(
            cmd=cmd, cmd_type=cmd_type, docs=docs, aliases=aliases
        )
        return repo
