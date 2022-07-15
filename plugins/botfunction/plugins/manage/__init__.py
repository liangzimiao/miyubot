import re

from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot_plugin_guild_patch import GuildMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN

from .data_source import Manage

block_user = Manage().on_command("封禁用户", "对目标用户进行封禁", permission=SUPERUSER)


@block_user.handle()
async def _ready_block_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["block_user"] = msg


@block_user.got("block_user", "哪位？GKD！")
async def _deal_block_user(bot: Bot, event: MessageEvent, state: T_State):
    user_id = f'{state["block_user"]}'
    quit_list = ["算了", "罢了"]
    if user_id in quit_list:
        await block_user.finish("...看来有人逃过一劫呢")

    is_ok = Manage().block_user(user_id)
    if not is_ok:
        await block_user.finish("kuso！封禁失败了...")

    await block_user.finish(f"用户 {user_id} 危！")


unblock_user = Manage().on_command("解封用户", "对目标用户进行解封", permission=SUPERUSER)


@unblock_user.handle()
async def _ready_unblock_user(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["unblock_user"] = msg


@unblock_user.got("unblock_user", "哪位？GKD！")
async def _deal_unblock_user(bot: Bot, event: MessageEvent, state: T_State):
    user_id = f'{state["unblock_user"]}'
    quit_list = ["算了", "罢了"]
    if user_id in quit_list:
        await unblock_user.finish("...有人又得继续在小黑屋呆一阵子了")

    is_ok = Manage().unblock_user(user_id)
    if not is_ok:
        await unblock_user.finish("kuso！解封失败了...")

    await unblock_user.finish(f"好欸！{user_id} 重获新生！")


block_group = Manage().on_command("封禁群", "对目标群进行封禁", permission=SUPERUSER)


@block_group.handle()
async def _ready_block_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["block_group"] = msg


@block_group.got("block_group", "哪个群？GKD！")
async def _deal_block_group(bot: Bot, event: MessageEvent, state: T_State):
    group_id =f'{state["block_group"]}'
    quit_list = ["算了", "罢了"]
    if group_id in quit_list:
        await block_group.finish("...看来有一群逃过一劫呢")

    is_ok = Manage().block_group(group_id)
    if not is_ok:
        await block_group.finish("kuso！封禁失败了...")

    await block_group.finish(f"群 {group_id} 危！")


unblock_group = Manage().on_command("解封群", "对目标群进行解封", permission=SUPERUSER)


@unblock_group.handle()
async def _ready_unblock_group(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["unblock_group"] = msg


@unblock_group.got("unblock_group", "哪个群？GKD！")
async def _deal_unblock_group(bot: Bot, event: MessageEvent, state: T_State):
    group_id = f'{state["unblock_group"]}'
    quit_list = ["算了", "罢了"]
    if group_id in quit_list:
        await unblock_group.finish("...有一群又得继续在小黑屋呆一阵子了")

    is_ok = Manage().unblock_group(group_id)
    if not is_ok:
        await unblock_group.finish("kuso！解封失败了...")

    await unblock_group.finish(f"好欸！群 {group_id} 重获新生！")


global_block_service = Manage().on_command("全局禁用", "全局禁用某服务", permission=SUPERUSER)


@global_block_service.handle()
async def _ready_block_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["global_block_service"] = msg


@global_block_service.got("global_block_service", "阿...是哪个服务呢")
async def _deal_global_block_service(bot: Bot, event: MessageEvent, state: T_State):
    block_service = state["global_block_service"]
    quit_list = ["算了", "罢了"]
    if block_service in quit_list:
        await global_block_service.finish("好吧...")

    is_ok = Manage().control_global_service(block_service, False)
    if not is_ok:
        await global_block_service.finish("kuso！禁用失败了...")

    await global_block_service.finish(f"服务 {block_service} 已被禁用")


global_unblock_service = Manage().on_command("全局启用", "全局启用某服务", permission=SUPERUSER)


@global_unblock_service.handle()
async def _ready_unblock_service(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["global_unblock_service"] = msg


@global_unblock_service.got("global_unblock_service", "阿...是哪个服务呢")
async def _deal_global_unblock_service(bot: Bot, event: MessageEvent, state: T_State):
    unblock_service = state["global_unblock_service"]
    quit_list = ["算了", "罢了"]
    if unblock_service in quit_list:
        await global_unblock_service.finish("好吧...")

    is_ok = Manage().control_global_service(unblock_service, True)
    if not is_ok:
        await global_unblock_service.finish("kuso！启用服务失败了...")

    await global_unblock_service.finish(f"服务 {unblock_service} 已启用")


user_block_service = Manage().on_regex(
    r"对用户(.*?)禁用(.*)", "针对某一用户禁用服务", permission=SUPERUSER
)


@user_block_service.handle()
async def _user_block_service(bot: Bot, event: MessageEvent):
    msg = str(event.message).strip()
    pattern = r"对用户(.*?)禁用(.*)"
    reg = re.findall(pattern, msg)
    print(reg)
    aim_user = reg[0][0]
    aim_service = reg[0][1]

    is_ok = Manage().control_user_service(aim_service, aim_user, False)
    if not is_ok:
        await user_block_service.finish("禁用失败...请检查服务名是否正确")
    await user_block_service.finish(f"完成～已禁止用户 {aim_user} 使用 {aim_service}")


user_unblock_service = Manage().on_regex(
    r"对用户(.*?)启用(.*)", "针对某一用户启用服务", permission=SUPERUSER
)


@user_unblock_service.handle()
async def _user_unblock_service(bot: Bot, event: MessageEvent):
    msg = str(event.message).strip()
    pattern = r"对用户(.*?)启用(.*)"
    reg = re.findall(pattern, msg)
    print(reg)
    aim_user = reg[0][0]
    aim_service = reg[0][1]

    is_ok = Manage().control_user_service(aim_service, aim_user, True)
    if not is_ok:
        await user_unblock_service.finish("启用失败...请检查服务名是否正确，或者此人并不存在于名单中")
    await user_unblock_service.finish(f"完成～已允许用户 {aim_user} 使用 {aim_service}")


group_block_service = Manage().on_command("禁用", "针对所在群禁用某服务", permission=SUPERUSER)


@group_block_service.handle()
async def _ready_group_block_service(
        bot: Bot, event: MessageEvent, state: T_State
):
    msg = str(event.message).strip()
    if msg:
        state["group_block_service"] = msg


@group_block_service.got("group_block_service", "阿...是哪个服务呢")
async def _deal_group_block_service(bot: Bot, event: MessageEvent, state: T_State):
    aim_service = state["group_block_service"]
    if type(event) is GroupMessageEvent:
        group_id = f"{event.group_id}"
        nick = '本群'
    elif type(event) is GuildMessageEvent:
        group_id = f'''{event.guild_id}_{event.channel_id}'''
        nick = '本频道'
    quit_list = ["算了", "罢了"]
    if aim_service in quit_list:
        await group_block_service.finish("好吧...")

    is_ok = Manage().control_group_service(aim_service, group_id, False)
    if not is_ok:
        await group_block_service.finish("禁用失败...请检查服务名是否输入正确")
    await group_block_service.finish(f"完成！～已禁止{nick}使用服务：{aim_service}")


group_unblock_service = Manage().on_command(
    "启用", "针对所在群启用某服务", permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN
)


@group_unblock_service.handle()
async def _ready_group_unblock_service(
        bot: Bot, event: MessageEvent, state: T_State
):
    msg = str(event.message).strip()
    if msg:
        state["group_unblock_service"] = msg


@group_unblock_service.got("group_unblock_service", "阿...是哪个服务呢")
async def _deal_group_unblock_service(
        bot: Bot, event: MessageEvent, state: T_State
):
    aim_service = state["group_unblock_service"]
    if type(event) is GroupMessageEvent:
        group_id = f"{event.group_id}"
        nick = '本群'
    elif type(event) is GuildMessageEvent:
        group_id = f'''{event.guild_id}_{event.channel_id}'''
        nick = '本频道'
    quit_list = ["算了", "罢了"]
    if aim_service in quit_list:
        await group_unblock_service.finish("好吧...")

    is_ok = Manage().control_group_service(aim_service, group_id, True)
    if not is_ok:
        await group_unblock_service.finish("启用失败...请检查服务名是否输入正确，或群不存在于名单中")
    await group_unblock_service.finish(f"完成！～已允许{nick}使用服务：{aim_service}")


get_friend_add_list = Manage().on_command("获取好友申请", "获取好友申请列表", permission=SUPERUSER)


@get_friend_add_list.handle()
async def _get_friend_add_list(bot: Bot, event: MessageEvent):
    data = Manage().load_friend_apply_list()
    temp_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i]["user_id"]
        apply_comment = data[i]["comment"]
        temp_msg = f"{apply_user} | {apply_comment} | {apply_code}"
        temp_list.append(temp_msg)

    msg0 = "申请人ID | 申请信息 | 申请码\n" + "\n".join(map(str, temp_list))
    msg1 = msg0 + "\nTip: 使用 同意/拒绝好友 [申请码] 以决定"
    await get_friend_add_list.finish(msg1)


approve_friend_add = Manage().on_command("同意好友", "同意好友申请", permission=SUPERUSER)


@approve_friend_add.handle()
async def _ready_approve_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["approve_friend_add"] = msg


@approve_friend_add.got("approve_friend_add", "申请码GKD!")
async def _deal_approve_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["approve_friend_add"]
    quit_list = ["算了", "罢了"]
    if apply_code in quit_list:
        await approve_friend_add.finish("好吧...")

    try:
        await bot.set_friend_add_request(flag=apply_code, approve=True)
    except BaseException:
        await approve_friend_add.finish("同意失败...尝试下手动？")
    data = Manage().load_friend_apply_list()
    data.pop(apply_code)
    Manage().save_friend_apply_list(data)
    await approve_friend_add.finish("好欸！申请已通过！")


refuse_friend_add = Manage().on_command("拒绝好友", "拒绝好友申请", permission=SUPERUSER)


@refuse_friend_add.handle()
async def _ready_refuse_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["refuse_friend_add"] = msg


@refuse_friend_add.got("refuse_friend_add", "申请码GKD!")
async def _deal_refuse_friend_add(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["refuse_friend_add"]
    quit_list = ["算了", "罢了"]
    if apply_code in quit_list:
        await refuse_friend_add.finish("好吧...")

    try:
        await bot.set_friend_add_request(flag=apply_code, approve=False)
    except BaseException:
        await refuse_friend_add.finish("拒绝失败...尝试下手动？")
    data = Manage().load_friend_apply_list()
    data.pop(apply_code)
    Manage().save_friend_apply_list(data)
    await refuse_friend_add.finish("已拒绝！")


get_group_invite_list = Manage().on_command("获取邀请列表", "获取群邀请列表", permission=SUPERUSER)


@get_group_invite_list.handle()
async def _get_group_invite_list(bot: Bot, event: MessageEvent):
    data = Manage().load_invite_apply_list()
    temp_list = list()
    for i in data:
        apply_code = i
        apply_user = data[i]["user_id"]
        apply_comment = data[i]["comment"]
        temp_msg = f"{apply_user} | {apply_comment} | {apply_code}"
        temp_list.append(temp_msg)

    msg0 = "申请人ID | 申请信息 | 申请码\n" + "\n".join(map(str, temp_list))
    msg1 = msg0 + "\nTip: 使用 同意/拒绝邀请 [申请码] 以决定"
    await get_friend_add_list.finish(msg1)


approve_group_invite = Manage().on_command("同意邀请", "同意群聊邀请", permission=SUPERUSER)


@approve_group_invite.handle()
async def _ready_approve_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["approve_group_invite"] = msg


@approve_group_invite.got("approve_group_invite", "申请码GKD!")
async def _deal_approve_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["approve_group_invite"]
    quit_list = ["算了", "罢了"]
    if apply_code in quit_list:
        await approve_group_invite.finish("好吧...")

    try:
        await bot.set_group_add_request(
            flag=apply_code, sub_type="invite", approve=True
        )
    except BaseException:
        await approve_group_invite.finish("同意失败...尝试下手动？")
    data = Manage().load_invite_apply_list()
    data.pop(apply_code)
    Manage().save_invite_apply_list(data)
    await approve_group_invite.finish("好欸！申请已通过！")


refuse_group_invite = Manage().on_command("拒绝邀请", "拒绝群聊邀请", permission=SUPERUSER)


@refuse_group_invite.handle()
async def _ready_refuse_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.message).strip()
    if msg:
        state["refuse_group_invite"] = msg


@refuse_group_invite.got("refuse_group_invite", "申请码GKD!")
async def _deal_refuse_group_invite(bot: Bot, event: MessageEvent, state: T_State):
    apply_code = state["refuse_group_invite"]
    quit_list = ["算了", "罢了"]
    if apply_code in quit_list:
        await refuse_group_invite.finish("好吧...")

    try:
        await bot.set_group_add_request(
            flag=apply_code, sub_type="invite", approve=False
        )
    except BaseException:
        await refuse_group_invite.finish("拒绝失败...尝试下手动？")
    data = Manage().load_invite_apply_list()
    data.pop(apply_code)
    Manage().save_invite_apply_list(data)
    await refuse_group_invite.finish("已拒绝！")

# track_error = Manage().on_command("追踪", "获取报错信息，传入追踪码", aliases={"/track"})


# @track_error.handle()
# async def _track_error(bot: Bot, event: MessageEvent):
#     track_id = str(event.message).strip()
#     repo = await Manage().track_error(track_id)
#     await track_error.finish(repo)
