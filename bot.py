#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init(apscheduler_autostart=True)
app = nonebot.get_asgi()

driver = nonebot.get_driver()

driver.register_adapter(Adapter)  # 注册 CQHTTP 的 Adapter
config = driver.config
# driver.on_startup(init)
# driver.on_shutdown(disconnect)
nonebot.load_plugins("src/plugins")  # 加载插件目录，该目录下为各插件，以下划线开头的插件将不会被加载
nonebot.load_builtin_plugins()  # 加载 nonebot 内置插件
# nonebot.load_from_toml("pyproject.toml")

# app = nonebot.get_asgi()
# nonebot.load_from_toml("pyproject.toml")# 从 pyproject.toml 加载插件
# nonebot.load_from_json("plugin.json")# 从 plugin.json 加载插件
# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...
# from services.db_context import init, disconnect

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function

if __name__ == "__main__":
    # nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    # nonebot.run(app="__mp_main__:app")
    nonebot.run()

