import oss2
import requests
from io import BytesIO
from nonebot import get_driver

config = get_driver().config


auth1 = config.auth1
auth2 = config.auth2
bucket1 = config.bucket1
bucket2 = config.bucket2
class OssUploader:
    def __init__(self, proxies=None):
        self.bucket_url = "https://sumatofarukon.temp.chinosk6.cn/"
        self.base_folder = "image/ai"

        self.auth = oss2.Auth(auth1, auth2)
        self.bucket = oss2.Bucket(self.auth, bucket1, bucket2)

        self.proxies = proxies

    def upload_file(self, tag: str,file: bytes, file_name=None, retry=0):
        
        if file_name is None:
            file_name = str(hash(bytes))+".jpg"

        retry += 1
        bucket = self.bucket
        upload_name = f"{self.base_folder}/{tag}/{file_name}"
        
        try:
            bucket.put_object(upload_name, file)
            return self.get_file_url(tag, file_name)
        except BaseException as e:
            print(e)
            if retry <= 3:
                print(f"上传失败: {upload_name}, 重试: {retry}")
                return self.upload_file(tag=tag, file_name=file_name, file=file, retry=retry)
            else:
                print(f"上传失败: {upload_name}, 重试次数已耗尽")
                raise e

    def upload_file_from_url(self, tag: str, file_name: str, url, proxy=True, retry=0):
        retry += 1
        try:
            print(f"开始下载: {url}")
            content = requests.get(url, proxies=self.proxies if proxy else None).content
            self.upload_file(tag=tag, file_name=file_name, file=BytesIO(content))
            return self.get_file_url(tag, file_name)
        except BaseException as e:
            print(e)
            if retry <= 3:
                print(f"下载失败: {url}, 重试: {retry}")
                return self.upload_file_from_url(tag=tag, file_name=file_name, url=url, proxy=proxy, retry=retry)
            else:
                print(f"下载失败: {url}, 重试次数已耗尽")


    def check_file_exist(self, tag: str, file_name: str):
        return self.bucket.object_exists(f"{self.base_folder}/{tag}/{file_name}")

    def get_file_url(self, tag: str, file_name: str, check_exist=False):
        if check_exist:
            if self.check_file_exist(tag=tag, file_name=file_name):
                return f"{self.bucket_url}{self.base_folder}/{tag}/{file_name}"
            else:
                return None
        else:
            return f"{self.bucket_url}{self.base_folder}/{tag}/{file_name}"

upd = OssUploader()
if __name__ == "__main__":
    # 上传例子
    
    with open("ji.jpg", "rb") as f:

        img_url = upd.upload_file("2968274386",f.read())

    if img_url is not None:

        print(f"Image url: {img_url}")

    else:

        print("Upload failed")
