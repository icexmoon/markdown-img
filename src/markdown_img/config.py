import os
from typing import Any
from .user_exception import UserException
import json


class Config():
    PARAM_SMMS_TOKEN = 'smms_token'
    PARAM_RRUU_TOKEN = 'rruu_token'
    PARAM_IMG_SERVICE = 'img_service'
    PARAM_YUJIAN_TOKEN = 'yujian_token'
    PARAM_QCLOUD_INFO = 'qcloud_info'
    PARAM_QINIU_INFO = "qiniu_info"
    PARAM_UPYUN_INFO = "upyun_info"
    PARAM_URL_ENCODE_MODE = 'url_encode_mode'
    PARAM_LANGUAGE = 'language'
    LANGUAGE_CN = 'cn'
    LANGUAGE_EN = 'en'
    URL_ENCODE_MODE_NONE = 'none'
    URL_ENCODE_MODE_ONLY_SPACE = 'only_space'
    URL_ENCODE_MODE_STANDARD = 'standard'
    QCLOUD_INFO_SECRET_KEY = 'secret_key'
    QCLOUD_INFO_SECRET_ID = 'secret_id'
    QCLOUD_INFO_REGION = 'region'
    QCLOUD_INFO_BUCKET = 'bucket'
    QCLOUD_INFO_DES_DIR = 'des_dir'
    QINIU_INFO_ACCESS_KEY = "access_key"
    QINIU_INFO_SECRET_KEY = "secret_key"
    QINIU_INFO_DNS_DOMAIN = "dns_domain"
    QINIU_INFO_BUCKET_NAME = "bucket_name"
    UPYUN_INFO_SERVICE = "service"
    UPYUN_INFO_USERNAME = "username"
    UPYUN_INFO_PASSWORD = "password"
    UPYUN_INFO_DIR = "dir"
    UPYUN_INFO_DOMAIN = "domain"
    IMG_SERVICE_YUJIAN = 'yujian'
    IMG_SERVICE_SMMS = 'smms'
    IMG_SERVICE_RRUU = 'rruu'
    IMG_SERVICE_ALI = 'ali'
    IMG_SERVICE_ALI2 = 'ali2'
    IMG_SERVICE_VIMCN = 'vimcn'
    IMG_SERVICE_QCLOUD = 'qcloud'
    IMG_SERVICE_QINIU = "qiniu"
    IMG_SERVICE_BILIBILI = 'bilibili'
    IMG_SERVICE_SOUGOU = "sougou"
    IMG_SERVICE_HULUXIA = "huluxia"
    IMG_SERVICE_CATBOX = "catbox"
    IMG_SERVICE_360 = "360"
    IMG_SERVICE_POSTIMAGES = "postimages"
    IMG_SERVICE_AI58 = "ai58"
    IMG_SERVICE_GTIMG = "gtimg"
    IMG_SERVICE_BKIMG = "bkimg"
    IMG_SERVICE_MUKE = "muke"
    IMG_SERVICE_UPYUN = "upyun"
    smmsTokenFile = ""
    configFile = ""
    mainConfig = {}

    def __new__(cls) -> Any:
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__new__(cls))
        return getattr(cls, "__instance")

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls) -> "Config":
        "获取Config的实例"
        # if not cls.__instance:
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", cls())
        return getattr(cls, "__instance")

    def getCurrentDirPath(self):
        part = __file__.rpartition('\\')
        return part[0]

    def getCurrentWorkDirPath(self):
        return os.getcwd()

    def getHelpFilePath(self):
        language = self.getConfigParam(Config.PARAM_LANGUAGE)
        filePath: str = ""
        if language == Config.LANGUAGE_EN:
            filePath = self.getCurrentDirPath()+"\\help_en.info"
        elif language == Config.LANGUAGE_CN:
            filePath = self.getCurrentDirPath()+"\\help.info"
        else:
            filePath = self.getCurrentDirPath()+"\\help.info"
        return filePath

    def getMarkdownImgDirPath(self):
        '''返回当前工作目录对应的markdown_img目录'''
        markdownImgDirPath = self.getCurrentWorkDirPath()+"\\markdown_img"
        if not os.path.exists(markdownImgDirPath):
            os.mkdir(markdownImgDirPath)
        return markdownImgDirPath

    def getSmmsTokenFile(self):
        if Config.smmsTokenFile == "":
            Config.smmsTokenFile = self.getCurrentDirPath()+'\\smms_token.config'
        return Config.smmsTokenFile

    def __getConfigFile(self):
        if Config.configFile == "":
            Config.configFile = self.getCurrentDirPath()+'\\main.config'
        return Config.configFile

    def __getDefaultConfigParams(self):
        if not hasattr(self, "__defaultConfigParams"):
            self.__defaultConfigParams = {Config.PARAM_IMG_SERVICE: Config.IMG_SERVICE_SMMS,
                                          Config.PARAM_URL_ENCODE_MODE: Config.URL_ENCODE_MODE_NONE,
                                          Config.PARAM_LANGUAGE: Config.LANGUAGE_CN}
        return self.__defaultConfigParams

    def __resetMainConfig(self):
        '''重置主配置为默认值'''
        defaultConfigParams = self.__getDefaultConfigParams()
        for key, value in defaultConfigParams.items():
            Config.mainConfig[key] = value

    def __getMainConfig(self, real=False):
        if len(Config.mainConfig) == 0 or real == True:
            if os.path.exists(self.__getConfigFile()):
                try:
                    with open(file=self.__getConfigFile(), mode='r', encoding='UTF-8') as fopen:
                        Config.mainConfig = json.loads(fopen.read())
                except json.decoder.JSONDecodeError:
                    # json解析异常的，设置为默认并重写配置文件
                    self.__resetMainConfig()
                    self.writeMainConfig()
            else:
                # 不存在配置文件的，给予默认配置
                self.__resetMainConfig()
        return Config.mainConfig

    def getConfigParam(self, param):
        '''获取配置参数'''
        mainConfig = self.__getMainConfig()
        if param in mainConfig:
            return mainConfig[param]
        else:
            value = ''
            defaultConfigParams = self.__getDefaultConfigParams()
            if param in defaultConfigParams:
                defaultValue = defaultConfigParams[param]
                self.setConfigParam(param, defaultValue)
                value = defaultValue
            return value

    def setConfigParam(self, param, value):
        '''设置配置参数'''
        mainConfig = self.__getMainConfig()
        mainConfig[param] = value

    def writeMainConfig(self):
        fopen = open(file=self.__getConfigFile(), mode='w', encoding='UTF-8')
        mainConfig = self.__getMainConfig()
        print(json.dumps(mainConfig), file=fopen)
        fopen.close()

    def getRruuToken(self):
        token = self.getConfigParam(Config.PARAM_RRUU_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_RRUU_TOKEN)
        return token

    def getYujianToken(self):
        token = self.getConfigParam(Config.PARAM_YUJIAN_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_YUJIAN_TOKEN)
        return token

    def getSmmsToken(self):
        token = self.getConfigParam(Config.PARAM_SMMS_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_SMMS_TOKEN)
        return token

    def getQCloudInfo(self):
        info = self.getConfigParam(Config.PARAM_QCLOUD_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_QCLOUD_INFO)
        return info

    def getQiniuInfo(self):
        """获取七牛云的详细配置"""
        info = self.getConfigParam(Config.PARAM_QINIU_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_QINIU_INFO)
        return info

    def writeSmmsToken(self, token: str):
        with open(file=self.getSmmsTokenFile(), mode='w') as configFileOpen:
            print(token, file=configFileOpen)

    def getErrorLogFilePath(self):
        return self.getCurrentDirPath()+'\\error.log'

    def writeErrorLog(self, msg: str):
        errorLogFilePath = self.getErrorLogFilePath()
        with open(file=errorLogFilePath, mode='a', encoding='UTF-8') as logOpen:
            print(msg, file=logOpen)
