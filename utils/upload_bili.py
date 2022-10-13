import requests

class BiliUploader:
    def __init__(self, cookies: dict) -> None:
        assert cookies['bili_jct']
        assert cookies['SESSDATA']

        self.cookies = cookies

    def upload(self, bytes, filename=None):
        api_url = "https://api.vc.bilibili.com/api/v1/drawImage/upload"

        if filename is None:
            filename = str(hash(bytes))

        # 设置post参数
        files = {"file_up": (filename, bytes)}
        data = {
            "biz": "draw",
            "category": "daily",
        }
        headers = {
            "Origin": "https://t.bilibili.com",
            "Referer": "https://t.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
        }

        # 向api发送post请求
        r = requests.post(
            api_url,
            files=files,
            data=data,
            headers=headers,
            cookies=self.cookies,
            timeout=300,
        )

        # 解析返回值，得到图片链接
        img_url = r.json()["data"]["image_url"]

        return img_url

    def upload_file(self, filepath: str):
        with open(filepath, "rb") as f:
            img_file = f.read()
        return self.upload(img_file, filename=filepath.split("/")[-1])




cookies = {
    "bili_jct": "",
    "SESSDATA": "",
}

b_uploader = BiliUploader(cookies=cookies)

if __name__=="__main__":
    with open("test.jpg", 'rb') as f:
        data = f.read()

    print("Upload bytes:")
    print(b_uploader.upload(data))

    print("Upload file:")
    print(b_uploader.upload_file("test.jpg"))