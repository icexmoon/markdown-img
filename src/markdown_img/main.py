from config import Config
import os
from smms_img import SmmsImg
from user_exception import UserException


class Main():

    def __init__(self):
        pass

    def isMarkdownFile(self, fileName: str):
        filePart = fileName.rpartition('.')
        fileExt = filePart[-1]
        return fileExt == 'md'

    def isOrigMdFile(self, fileName: str):
        '''判断是否为原始markdown文件'''
        if not self.isMarkdownFile(fileName):
            return False
        # 检查文件后缀是否为_image
        specialMark = "_image"
        filePart = fileName.rpartition('.')
        # 如果文件名长度过小，肯定是原始文件
        if len(filePart[0]) <= len(specialMark):
            return True
        # 后缀是否能完全匹配
        if filePart[0].endswith(specialMark):
            return False
        return True

    def getCopyFileName(self, fileName: str):
        filePart = fileName.rpartition('.')
        fileExt = filePart[-1]
        newFileName = filePart[0]+'_image.'+fileExt
        return newFileName

    def getCopyFilePath(self, fileName: str):
        copyFileName = self.getCopyFileName(fileName)
        SysConfig = Config()
        return SysConfig.getMarkdownImgDirPath()+'\\'+copyFileName

    def findLocalImageFile(self, line: str, localImages: set):
        '''递归查找某段字符串中中括号包裹的内容是否为本地图片'''
        linePart = line.partition('(')
        if len(linePart[2]) > 0:
            secondPart = linePart[2].partition(')')
            content = secondPart[0]
            if len(content) > 0:
                # print(content)
                if content.endswith('.png') and os.path.exists(content):
                    localImages.add(content)
                    self.findLocalImageFile(content, localImages)

    def dealMdFile(self, mdFile: str):
        imgDict = dict()
        localImages = set()
        # 逐行扫描，查找本地图片
        with open(file=mdFile, mode='r', encoding='UTF-8') as fopen:
            for line in fopen:
                # 去除行尾的换行
                subLine = line[0:len(line)-1]
                self.findLocalImageFile(subLine, localImages)
        # 上传本地图片，建立图片映射表
        imgServer = SmmsImg()
        imgServer.multiUploadImage(list(localImages), imgDict)
        # 替换本地图片
        # copyFileName = self.getCopyFileName(mdFile)
        copyFilePath = self.getCopyFilePath(mdFile)
        copyFileOpen = open(file=copyFilePath, mode='w', encoding='UTF-8')
        with open(file=mdFile, mode='r', encoding='UTF-8') as fwrite:
            for line in fwrite:
                for localImg, webImg in imgDict.items():
                    line = line.replace(localImg, webImg)
                copyFileOpen.write(line)
        copyFileOpen.close()

    def dealUserException(self, userExp: UserException):
        sysConfig = Config()
        if userExp.getErrorCode() == UserException.CODE_NO_CONFIG:
            token = input("缺少你的sm.ms访问令牌，请输入：")
            sysConfig.writeSmmsToken(token)
            print("访问令牌已保存，请重新运行程序")
            exit()
        elif userExp.getErrorCode() == UserException.CODE_UPLOAD_ERROR:
            print("上传图片到sm.ms失败，请检查日志文件", sysConfig.getErrorLogFilePath())
            exit()
        else:
            print("未定义错误，请联系开发者")
            exit()

    def main(self):
        # 检索当前目录中的markdown文件
        for dir in os.listdir():
            # print(dir)
            if os.path.isfile(dir):
                if self.isOrigMdFile(dir):
                    # 复制一份拷贝，如果有，则不覆盖
                    # copyFileName = self.getCopyFileName(dir)
                    copyFilePath = self.getCopyFilePath(dir)
                    if not os.path.exists(copyFilePath):
                        # 对拷贝进行处理
                        try:
                            self.dealMdFile(dir)
                        except UserException as e:
                            self.dealUserException(e)
                        print("已成功处理markdown文件", dir)
        print("所有markdown文档已处理完毕")
        exit()
