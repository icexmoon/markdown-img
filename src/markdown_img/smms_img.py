from .config import Config
from .user_exception import UserException
import requests
import json
from concurrent import futures
import qcloud_cos.cos_exception
from .qcloud_client import QcloudClient


class SmmsImg():
    def __init__(self):
        self.sysConfig = Config()
        self.qclient = None

    def uploadToQCloud(self, path: str) -> str:
        '''上传到腾讯云'''
        clientInfo = self.sysConfig.getQCloudInfo()
        if self.qclient == None:
            self.qclient = QcloudClient(clientInfo[Config.QCLOUD_INFO_SECRET_ID], clientInfo[Config.QCLOUD_INFO_SECRET_KEY],
                                        clientInfo[Config.QCLOUD_INFO_REGION], clientInfo[Config.QCLOUD_INFO_BUCKET])
        try:
            urlEncodeMode = self.sysConfig.getConfigParam(Config.PARAM_URL_ENCODE_MODE)
            url = self.qclient.upload(
                path, clientInfo[Config.QCLOUD_INFO_DES_DIR], urlEncodeMode)
        except qcloud_cos.cos_exception.CosServiceError as e:
            self.sysConfig.writeErrorLog(str(e))
            return False
        return url

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
        try:
            respJson = r.json()
        except json.decoder.JSONDecodeError as e:
            self.sysConfig.writeErrorLog("接口解析错误："+str(e)+"\n返回信息："+r.text)
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        except Exception as e:
            self.sysConfig.writeErrorLog("未知的接口调用错误:"+str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        urls = {}
        if str(respJson['code']).strip() == '200' and str(respJson['msg']).strip() == 'success':
            urls['rruu'] = respJson['data']['url']['distribute']
            urls['ali'] = respJson['data']['url']['ali']
        else:
            return False
        if self.sysConfig.getConfigParam(Config.PARAM_IMG_SERVICE) == Config.IMG_SERVICE_ALI2:
            return urls['ali']
        return urls['rruu']

    def uploadToYujian(self, imgPath):
        '''上传到遇见图床和阿里图床'''
        imgOpen = open(imgPath, 'rb')
        files = {'image': imgOpen}
        apiType = 'ali'
        token = self.sysConfig.getYujianToken()
        r = requests.post('https://www.hualigs.cn/api/upload',
                          data={'apiType': apiType, 'privateStorage': '', 'token': token}, files=files)
        imgOpen.close()
        try:
            respJson = r.json()
        except json.decoder.JSONDecodeError as e:
            self.sysConfig.writeErrorLog("接口解析错误："+str(e)+"\n返回信息："+r.text)
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        except Exception as e:
            self.sysConfig.writeErrorLog("未知的接口调用错误:"+str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        urls = {}
        if str(respJson['code']).strip() == '200' and str(respJson['msg']).strip() == 'success':
            urls['yujian'] = respJson['data']['url']['distribute']
            urls['ali'] = respJson['data']['url']['ali']
        else:
            return False
        if self.sysConfig.getConfigParam(Config.PARAM_IMG_SERVICE) == Config.IMG_SERVICE_ALI:
            return urls['ali']
        return urls['yujian']

    def multiUploadImage(self, images: list, results: dict):
        '''批量上传图片'''
        MAX_SAME_TIME_DEAL = 10
        if len(images) <= MAX_SAME_TIME_DEAL:
            maxThreadWorks = min(len(images), MAX_SAME_TIME_DEAL)
            # fixed 如果有没有图片的md文件，直接不做处理。
            if maxThreadWorks > 0:
                with futures.ThreadPoolExecutor(max_workers=maxThreadWorks) as futuresExecutor:
                    futureMap = {}
                    for localImg in images:
                        future = futuresExecutor.submit(
                            self.uploadOne, localImg)
                        futureMap[future] = localImg
                    futureDone = futures.as_completed(futureMap)
                    for future in futureDone:
                        try:
                            webImage = future.result()
                        except UserException as e:
                            raise e
                        if webImage == False:
                            raise UserException(
                                UserException.CODE_UPLOAD_ERROR, "文件上传出错")
                        else:
                            results[futureMap[future]] = webImage
        else:
            self.multiUploadImage(images[0:MAX_SAME_TIME_DEAL], results)
            self.multiUploadImage(
                images[MAX_SAME_TIME_DEAL:len(images)], results)

    def uploadOne(self, localImg):
        imgService = self.sysConfig.getConfigParam(
            Config.PARAM_IMG_SERVICE)
        webImage = False
        if imgService == Config.IMG_SERVICE_ALI:
            webImage = self.uploadToYujian(localImg)
        elif imgService == Config.IMG_SERVICE_ALI2:
            webImage = self.uploadToRruu(localImg)
        elif imgService == Config.IMG_SERVICE_RRUU:
            webImage = self.uploadToRruu(localImg)
        elif imgService == Config.IMG_SERVICE_VIMCN:
            webImage = self.uploadToVimCn(localImg)
        elif imgService == Config.IMG_SERVICE_YUJIAN:
            webImage = self.uploadToYujian(localImg)
        elif imgService == Config.IMG_SERVICE_QCLOUD:
            webImage = self.uploadToQCloud(localImg)
        else:
            webImage = self.uploadToSmms(localImg)
        return webImage
