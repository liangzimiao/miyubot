
from asyncio.windows_events import NULL
import nonebot
from utils import aiorequests
from io import BytesIO

driver = nonebot.get_driver()
config = driver.config

appid = config.appid
appsecret = config.appsecret

async def check(img):
    try:
        _url = ("https://api.q.qq.com/api/getToken?grant_type=client_credential") + (f"&appid={appid}") + (
            f"&secret={appsecret}")
        response = await aiorequests.get(_url)
        data = await response.json()
        access_token = data["access_token"]
        params = {'access_token': {access_token},"appid":{appid}}

        files = {'media': NULL ,}
        files["media"] =  BytesIO(img).read() 
  
        response = await aiorequests.post(('https://api.q.qq.com/api/json/security/ImgSecCheck') , params=params, files=files)
        data = await response.json()
        print(data)
        if data["errMsg"] == "ok":
            return 0
        else:
            return 1
    except Exception as e:
        
        return 1

