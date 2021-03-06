#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import nonebot
from nonebot.adapters.onebot.v11 import Adapter

nonebot.init(apscheduler_autostart=True)
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)  # 注册 CQHTTP 的 Adapter
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
