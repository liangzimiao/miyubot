import requests
from utils import aiorequests
import nonebot


config = nonebot.get_driver().config


API_KEY = config.baidu_appid   #你的API Key
SECRET_KEY = config.baidu_appsecret   #你的Secret Key

host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
response = requests.get(host)
access_token = response.json()["access_token"]
request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined"
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}


async def porn_pic_index(base):
    params = {"image": base}
    resp = await aiorequests.post(request_url, data=params, headers=headers)

    if resp.ok:
        data = await resp.json()
        print(data)
    try:
        if (data):
            r = data
            value = 0
            if "error_code" in r:   #失败响应
                #return { 'code': r['error_code'], 'msg': r['error_msg'] }
                return 1,value #调用失败 默认有风险
            if r['data']:
                data = r['data'] 
                porn_0 = 0
                porn_1 = 0
                porn_2 = 0
                for c in data:
                    #由于百度的图片审核经常给出极低分,所以不合规项置信度*500后为分数
                    if c['type'] == 1 and c['subType'] == 0:
                        porn_0 = int(c['probability'] * 500)
                    elif c['type'] == 1 and c['subType'] == 1:
                        porn_1 = int(c['probability'] * 500)
                    elif c['type'] == 1 and c['subType'] == 10:
                        porn_2 = int(c['probability'] * 500)
                value = max(porn_0,porn_1,porn_2)
            print(r["conclusionType"])
            print(r["conclusion"])    
            if  r["conclusionType"] == 1: #合规
                return 0,value
            if  r["conclusionType"] == 2: #不合规
                return 1,value
            if  r["conclusionType"] == 3: #疑似
                return 0,value
            if  r["conclusionType"] == 4: #失败
                return 1,value
        else:
            #return { 'code': -1, 'msg': 'API Error' }
            return 1,0 #调用失败 默认有风险
    except FileNotFoundError:
        #return { 'code': -1, 'msg': 'File not found' }
        return 1,0 #调用失败 默认有风险