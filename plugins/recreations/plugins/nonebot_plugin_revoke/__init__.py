from typing import Optional

from nonebot import on_command, logger
from nonebot.adapters.onebot.v11 import ActionFailed, Bot
from nonebot.internal.params import Depends
from nonebot.permission import SUPERUSER

from .utils import reply_message_id

revoke_matcher = on_command("revoke", aliases={"撤回"}, permission=SUPERUSER)


@revoke_matcher.handle()
async def _(
        bot: Bot,
        reply_msg_id: Optional[int] = Depends(reply_message_id)
):
    try:
        if reply_msg_id is not None:
            await bot.delete_msg(message_id=reply_msg_id)
    except ActionFailed as e:
        logger.exception(e)
        await revoke_matcher.finish("权限不足")
        
