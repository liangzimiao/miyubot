from nonebot import  logger, on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import  MessageSegment
from plugins.uma.plugins.uma_gacha.data_source import UmaGachaService
from plugins.uma.plugins.uma_gacha.draw import draw
from plugins.uma.plugins.uma_gacha.gacha import uppool, gacha, supgacha
from utils import  pic2b64
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11 import Message
from PIL import Image


check_pick = UmaGachaService().on_command('查看马娘卡池','查看马娘卡池',priority=5)

@check_pick.handle()
async def gacha_info(bot, event: MessageEvent):
    up_chara = uppool.up_card_id
    if up_chara == 1000:
        msg = f'当前卡池无up角色'
    else:
        msg = f'当前卡池时间为\n{uppool.up_time}\n'
        msg += f'当前赛马娘卡池为\n{uppool.up_chara_pool}'
        res = Image.open(uppool.up_chara_pool_img).convert('RGBA') .resize((480, 120))
        box = (30, 0, 400,120)
        img =res.crop(box) 
        res=pic2b64(img)
        msg += f"{MessageSegment.image(file =res  ,cache=False,)}"
        msg += f'当前支援卡卡池为\n{uppool.up_card_pool}'
        res = Image.open(uppool.up_card_pool_img).convert('RGBA') .resize((480, 120))
        img =res.crop(box) 
        res=pic2b64(img)
        msg += f"{MessageSegment.image(file =res ,cache=False,)}"

    await matcher.send(Message(msg))







#单抽
matcher = UmaGachaService().on_command("马娘单抽", "马娘单抽",aliases={"uma gahca one","来发马娘单抽"}, priority=5)

@matcher.handle()
async def handle_func():
    up_chara=uppool.up_chara_id
    result = gacha.gacha_one(up_chara)
    res=draw.draw_one(result)
    res=pic2b64(res)
    await matcher.send(
        MessageSegment.image(file =res ,cache=False,),
        at_sender=True
        )

#10连
matcher = UmaGachaService().on_command("马娘十连","马娘十连", aliases={"马娘10连","十连马娘"},  priority=5)

@matcher.handle()
async def handle_func():

    up_chara=uppool.up_chara_id
    result = gacha.gacha_ten(up_chara)
    res=draw.draw_ten(result)
    res=pic2b64(res)
    await matcher.send(
        MessageSegment.image(file =res ,cache=False,),
        at_sender=True
        )

#一井
matcher = UmaGachaService().on_command("马娘一井","马娘一井", aliases={"马之井","来一井马娘"},  priority=5)

@matcher.handle()
async def handle_func():
    up_chara=uppool.up_chara_id
    result = gacha.gacha_jing(up_chara)
    s3=len(result[0])
    s2=result[1]
    s1=result[2]
    up=0
    for one in result[0]:
        if one in up_chara:
            up= up+1
    meg = ''
    while len(result[0])>10:
        res=draw.draw_tenten(result[0][:10])
        res=pic2b64(res)
        meg += f"{MessageSegment.image(file =res ,cache=False,)}"
        del result[0][0: 10]
    if len(result[0])<=10:
        res=draw.draw_tenten(result[0])
        res=pic2b64(res)
        meg += f"{MessageSegment.image(file =res ,cache=False,)}"   
    if s3 <= 0:
            meg = "竟...竟然没有3★？！\n"
    msg = [
        f"\n素敵な仲間が増えますよ！ {meg}\n",
        f"★★★×{s3} ★★×{s2} ★×{s1}\n"]         
    if up == 0 and s3 == 0:
        msg.append("太惨了，咱们还是退款删游吧...")
    elif up == 0 and s3 > 7:
        msg.append("up呢？我的up呢？")
    elif up == 0 and s3 <= 3:
        msg.append("这位酋长，梦幻包考虑一下？")
    elif up == 0:
        if up_chara == 1000:
            msg.append('抽到想要的角色了吗?')
        else:
            msg.append("据说天井的概率只有12.16%")
    elif up == 3:
        msg.append("抽井母五一气呵成！")
    elif up >= 4:
        msg.append("记忆碎片一大堆！您是托吧？")
    elif s3 > 7:
        msg.append("已经够欧了")

    await matcher.send(
            msg,
        at_sender=True)



#支援卡单抽
matcher = UmaGachaService().on_command("支援卡单抽","支援卡单抽" ,aliases={"uma gahca support one","来发支援卡单抽"}, priority=5)

@matcher.handle()
async def handle_func(): 
    up_card=uppool.up_card_id
    result = supgacha.gacha_one(up_card)
    print(result)
    #result="20013"
    res=draw.draw_support_one(result)
    res=pic2b64(res)
    await matcher.send(
        MessageSegment.image(file =res ,cache=False,),
        at_sender=True
        )

#10连
matcher = UmaGachaService().on_command("支援卡十连","支援卡十连", aliases={"支援卡10连","十连支援卡"}, priority=5)

@matcher.handle()
async def handle_func():
    up_card=uppool.up_card_id
    result = supgacha.gacha_ten(up_card)
    res=draw.draw_support_ten(result)
    res=pic2b64(res)
    await matcher.send(
        MessageSegment.image(file =res ,cache=False,),
        at_sender=True
        )

matcher = UmaGachaService().on_command("支援卡一井","支援卡一井", aliases={"卡之井","来一井支援卡"}, priority=5)

@matcher.handle()
async def handle_func(): 
    up_card=uppool.up_card_id
    result = supgacha.gacha_jing(up_card)
    s3=len(result[0])
    s2=result[1]
    s1=result[2]
    up=0
    for one in result[0]:
        if one in up_card:
            up= up+1
    meg = ''
    while len(result[0])>10:
        res=draw.draw_support_tenten(result[0][:10])
        res=pic2b64(res)
        meg += f"{MessageSegment.image(file =res ,cache=False,)}"
        del result[0][0: 10]
    if len(result[0])<=10:
        res=draw.draw_support_tenten(result[0])
        res=pic2b64(res)
        meg += f"{MessageSegment.image(file =res ,cache=False,)}"   
    if s3 <= 0:
            meg = "竟...竟然没有SSR？！\n"
    msg = [
        f"\n素敵な仲間が増えますよ！ {meg}",
        f"SSR×{s3} SR×{s2} R×{s1}\n"]         
    if up == 0 and s3 == 0:
        msg.append("太惨了，咱们还是退款删游吧...\n")
    elif up == 0 and s3 > 4:
        msg.append("up呢？我的up呢？")
    elif up == 0 and s3 <= 3:
        msg.append("这位酋长，梦幻包考虑一下？")
    elif up == 0:
        if up_card == 1000:
            msg.append('抽到想要的卡了吗?')
        else:
            msg.append("据说天井的概率只有12.16%")
    elif up == 3:
        msg.append("还要不要继续抽呢？")
    elif up >= 4:
        msg.append("已经够满破力")
    elif s3 > 7:
        msg.append("欧皇寿命极短")
    
    await matcher.send(
            msg,
        at_sender=True)

matcher = UmaGachaService().on_command("更新马娘卡池","更新马娘卡池", permission=SUPERUSER, priority=5)

@matcher.handle()
async def update_uma_pool():
    try:
        uppool.update_pool()
        await matcher.send('ok')
    except Exception as e:
        logger.exception(e)
        await matcher.send(f'Error: {type(e)}')
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

