from .config import Config
from .user_exception import UserException
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

    def uploadToVimCn(self, imgPath):
        '''上传到Vim-cn'''
        imgOpen = open(imgPath, 'rb')
        files = {'file': imgOpen}
        r = requests.post('https://img.vim-cn.com/',
                          data={'name': '@/path/to/image'}, files=files)
        imgOpen.close()
        return r.text

    def uploadToRruu(self, imgPath):
        '''上传到如优图床和阿里图床'''
        imgOpen = open(imgPath, 'rb')
        files = {'image': imgOpen}
        apiType = 'ali'
        token = self.sysConfig.getRruuToken()
        r = requests.post('https://img.rruu.net/api/upload',
                          data={'apiType': apiType, 'privateStorage': '', 'token': token}, files=files)
        imgOpen.close()
        respJson = r.json()
        urls = {}
        if str(respJson['code']).strip() == '200' and str(respJson['msg']).strip() == 'success':
            urls['rruu'] = respJson['data']['url']['distribute']
            urls['ali'] = respJson['data']['url']['ali']
        else:
            return False
        if self.sysConfig.getConfigParam(Config.PARAM_IMG_SERVICE) == Config.IMG_SERVICE_ALI:
            return urls['ali']
        return urls['rruu']

    def multiUploadImage(self, images: list, results: dict):
        '''批量上传图片'''
        if len(images) <= 10:
            for localImg in images:
                imgService = self.sysConfig.getConfigParam(Config.PARAM_IMG_SERVICE)
                webImage = ''
                if imgService == Config.IMG_SERVICE_ALI:
                    webImage = self.uploadToRruu(localImg)
                elif imgService == Config.IMG_SERVICE_RRUU:
                    webImage = self.uploadToRruu(localImg)
                elif imgService == Config.IMG_SERVICE_VIMCN:
                    webImage = self.uploadToVimCn(localImg)
                else:
                    webImage = self.uploadToSmms(localImg)
                if webImage == False:
                    raise UserException(
                        UserException.CODE_UPLOAD_ERROR, "文件上传出错")
                else:
                    results[localImg] = webImage
        else:
            self.multiUploadImage(images[0:10], results)
            self.multiUploadImage(images[10:len(images)], results)
