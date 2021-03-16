import os
from user_exception import UserException


class Config():
    smmsTokenFile = ""

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

    def getSmmsToken(self):
        if not os.path.exists(self.getSmmsTokenFile()):
            raise UserException(UserException.CODE_NO_CONFIG)
        configFileOpen = open(file=self.getSmmsTokenFile(), mode='r')
        token = configFileOpen.readline()
        configFileOpen.close()
        if len(token) <= 4:
            raise UserException(UserException.CODE_NO_CONFIG)
        token = token[0:len(token)-1]
        return token

    def writeSmmsToken(self, token: str):
        with open(file=self.getSmmsTokenFile(), mode='w') as configFileOpen:
            print(token, file=configFileOpen)

    def getErrorLogFilePath(self):
        return self.getCurrentDirPath()+'\\error.log'

    def writeErrorLog(self, msg: str):
        errorLogFilePath = self.getErrorLogFilePath()
        with open(file=errorLogFilePath, mode='a', encoding='UTF-8') as logOpen:
            print(msg, file=logOpen)
