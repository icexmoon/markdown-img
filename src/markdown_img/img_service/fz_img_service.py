from .img_service import ImgService
import requests
from ..config import Config
from ..user_exception import UserException
import json
from typing import Any


class FzImgService(ImgService):
    '''风筝图床'''

    def __init__(self) -> None:
        super().__init__()
        self.sysConfig = Config.getInstance()

    def __getToken(self):
        if hasattr(self, "__token"):
            return self.__token
        phone = self.__getInfo('phone')
        pwd = self.__getInfo('pwd')
        self.__token = self.__login(phone, pwd)
        return self.__token

    def __login(self, phone: str, pwd: str) -> str:
        '''登录并获取token'''
        r = requests.post('https://imgbed.link/imgbed/user/login',
                          data={'phoneNum': phone, 'pwd': pwd})
        try:
            respJson = r.json()
        except json.decoder.JSONDecodeError as e:
            self.sysConfig.writeErrorLog("接口解析错误："+str(e)+"\n返回信息："+r.text)
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        except Exception as e:
            self.sysConfig.writeErrorLog("未知的接口调用错误:"+str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        if respJson['code'] != 0:
            raise UserException(
                UserException.CODE_UPLOAD_ERROR, '接口调用出错：'+respJson['msg'])
        return respJson['token']

    def __getInfo(self, key: str) -> Any:
        info = self.getConfigInfo()
        if key in info:
            return info[key]
        raise UserException(UserException.CODE_OTHER, '缺少图床配置：'+key)

    def getConfigInfo(self) -> dict:
        sysConfig = Config.getInstance()
        info = sysConfig.getConfigParam(Config.PARAM_FZ_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return info

    def upload(self, localImg: str) -> str:
        url = "https://imgbed.link/imgbed/file/upload"
        payload = {}
        imgOpen = open(localImg, 'rb')
        files = {'file': imgOpen}
        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://www.apifox.cn)',
            'token': self.__getToken()
        }

        r = requests.request("POST", url, headers=headers,
                             data=payload, files=files)
        imgOpen.close()
        try:
            respJson = r.json()
        except json.decoder.JSONDecodeError as e:
            self.sysConfig.writeErrorLog("接口解析错误："+str(e)+"\n返回信息："+r.text)
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        except Exception as e:
            self.sysConfig.writeErrorLog("未知的接口调用错误:"+str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        return respJson['rows'][0]['url']
    
    def inputConfig(self) -> None:
        info = {}
        print(self.globalization.getTextWithColon("fz_info_required"))
        info[Config.FZ_INFO_PHONE] = input(
            self.globalization.getTextWithColon("fz_info_phone"))
        info[Config.FZ_INFO_PWD] = input(
            self.globalization.getTextWithColon("fz_info_pwd"))
        sysConfig = self.sysConfig
        sysConfig.setConfigParam(Config.PARAM_FZ_INFO, info)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("config_info_saved"))

    def inputNewConfig(self) -> None:
        info = {}
        info[Config.FZ_INFO_PHONE] = input(
            self.globalization.getTextWithColon("fz_info_phone"))
        info[Config.FZ_INFO_PWD] = input(
            self.globalization.getTextWithColon("fz_info_pwd"))
        sysConfig = self.sysConfig
        sysConfig.setConfigParam(Config.PARAM_FZ_INFO, info)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("config_info_saved"))

    def getConfigInfoText(self) -> tuple:
        lines = list()
        info = self.getConfigInfo()
        lines.append(self.globalization.getTextWithParam(
            "fz_info_phone", info[Config.FZ_INFO_PHONE]))
        lines.append(self.globalization.getTextWithParam(
            "fz_info_pwd", info[Config.FZ_INFO_PWD]))
        return tuple(lines)
