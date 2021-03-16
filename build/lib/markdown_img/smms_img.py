from config import Config
from user_exception import UserException
import requests


class SmmsImg():
    def __init__(self):
        self.sysConfig = Config()
        pass

    def uploadToSmms(self, path: str) -> str:
        '''上传本地图片到smms,并返回网络图片地址'''
        token = self.sysConfig.getSmmsToken()
        headers = {'Authorization': token}
        files = {'smfile': open(path, 'rb')}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=headers).json()
        if res['success']:
            return res['data']['url']
        elif res['code'] == 'image_repeated':
            return res['images']
        else:
            pass
        # logOpen = open(file='upload.log', mode='a')
        # print(res, file=logOpen)
        # logOpen.close()
        self.sysConfig.writeErrorLog(str(res))
        return False

    def multiUploadImage(self, images: list, results: dict):
        '''批量上传图片'''
        if len(images) <= 10:
            for localImg in images:
                webImage = self.uploadToSmms(localImg)
                if webImage == False:
                    # print("文件上传出错")
                    # exit()
                    raise UserException(
                        UserException.CODE_UPLOAD_ERROR, "文件上传出错")
                else:
                    results[localImg] = webImage
        else:
            self.multiUploadImage(images[0:10], results)
            self.multiUploadImage(images[10:len(images)], results)
