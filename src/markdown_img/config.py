import os
from .user_exception import UserException
import json


class Config():
    PARAM_SMMS_TOKEN = 'smms_token'
    PARAM_RRUU_TOKEN = 'rruu_token'
    PARAM_IMG_SERVICE = 'img_service'
    IMG_SERVICE_SMMS = 'smms'
    IMG_SERVICE_RRUU = 'rruu'
    IMG_SERVICE_ALI = 'ali'
    IMG_SERVICE_VIMCN = 'vimcn'
    smmsTokenFile = ""
    configFile = ""
    mainConfig = {}

    def __init__(self):
        pass

    def getCurrentDirPath(self):
        part = __file__.rpartition('\\')
        return part[0]

    def getCurrentWorkDirPath(self):
        return os.getcwd()

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

    def __getMainConfig(self, real=False):
        if len(Config.mainConfig) == 0 or real == True:
            if os.path.exists(self.__getConfigFile()):
                try:
                    with open(file=self.__getConfigFile(), mode='r', encoding='UTF-8') as fopen:
                            Config.mainConfig = json.loads(fopen.read())
                except json.decoder.JSONDecodeError:
                    #json解析异常的，设置为默认并重写配置文件
                    Config.mainConfig['img_service'] = 'smms'
                    self.writeMainConfig()
            else:
                # 不存在配置文件的，给予默认配置
                Config.mainConfig['img_service'] = 'smms'
        return Config.mainConfig

    def getConfigParam(self, param):
        '''获取配置参数'''
        mainConfig = self.__getMainConfig()
        if param in mainConfig:
            return mainConfig[param]
        else:
            return ''

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

    def getSmmsToken(self):
        token = self.getConfigParam(Config.PARAM_SMMS_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_SMMS_TOKEN)
        return token
        # if not os.path.exists(self.getSmmsTokenFile()):
        #     raise UserException(UserException.CODE_NO_CONFIG)
        # configFileOpen = open(file=self.getSmmsTokenFile(), mode='r')
        # token = configFileOpen.readline()
        # configFileOpen.close()
        # if len(token) <= 4:
        #     raise UserException(UserException.CODE_NO_CONFIG)
        # token = token[0:len(token)-1]
        # return token

    def writeSmmsToken(self, token: str):
        with open(file=self.getSmmsTokenFile(), mode='w') as configFileOpen:
            print(token, file=configFileOpen)

    def getErrorLogFilePath(self):
        return self.getCurrentDirPath()+'\\error.log'

    def writeErrorLog(self, msg: str):
        errorLogFilePath = self.getErrorLogFilePath()
        with open(file=errorLogFilePath, mode='a', encoding='UTF-8') as logOpen:
            print(msg, file=logOpen)
