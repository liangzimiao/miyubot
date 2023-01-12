from typing import Optional

from nonebot.adapters.onebot.v11 import MessageEvent


def reply_message_id(event: MessageEvent) -> Optional[int]:
    message_id = None
    if bool(event.reply):
        message_id = int(event.reply.message_id)
    #for seg in event.original_message:
    #    if seg.type == "reply":
    #        message_id = int(seg.data["id"])
    #        break
    return message_id
