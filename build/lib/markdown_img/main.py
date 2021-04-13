from .config import Config
import os
from .smms_img import SmmsImg
from .user_exception import UserException
from .download_help import DownloadHelp
from .time_helper import TimeHelper


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

    def findImagesInStr(self, line: str, localImages: list):
        '''递归查找某段字符串中中括号包裹的内容是否为本地图片'''
        linePart = line.partition('(')
        if len(linePart[2]) > 0:
            secondPart = linePart[2].partition(')')
            content = secondPart[0]
            if len(content) > 0:
                # print(content)
                if content.endswith('.png'):
                    localImages.append(content)
                    self.findImagesInStr(content, localImages)

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

    def findImgsInMdFile(self, mdFile):
        '''查找markdown文件中的图片列表'''
        localImages = list()
        # 逐行扫描，查找本地图片
        with open(file=mdFile, mode='r', encoding='UTF-8') as fopen:
            for line in fopen:
                # 去除行尾的换行
                subLine = line[0:len(line)-1]
                self.findImagesInStr(subLine, localImages)
        return localImages

    def dealUserException(self, userExp: UserException):
        sysConfig = Config()
        if userExp.getErrorCode() == UserException.CODE_NO_SMMS_TOKEN:
            token = input("缺少你的sm.ms访问令牌，请输入：")
            sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
            sysConfig.writeMainConfig()
            # sysConfig.writeSmmsToken(token)
            print("访问令牌已保存，请重新运行程序")
        elif userExp.getErrorCode() == UserException.CODE_NO_RRUU_TOKEN:
            token = input("缺少你的如优图床访问令牌，请输入：")
            sysConfig.setConfigParam(Config.PARAM_RRUU_TOKEN, token)
            sysConfig.writeMainConfig()
            print("访问令牌已保存，请重新运行程序")
        elif userExp.getErrorCode() == UserException.CODE_UPLOAD_ERROR:
            print("上传图片到sm.ms失败，请检查日志文件", sysConfig.getErrorLogFilePath())
        elif userExp.getErrorCode() == UserException.CODE_TIMEOUT:
            print(userExp.getErrorMsg())
        else:
            print("未定义错误，请联系开发者")
        exit()

    def main(self, refresh = False):
        # 检索当前目录中的markdown文件
        for dir in os.listdir():
            if os.path.isfile(dir):
                if self.isOrigMdFile(dir):
                    # 如果副本存在，刷新模式下且原md文件更新过的，删除副本，重新生成，否则不处理
                    copyFilePath = self.getCopyFilePath(dir)
                    if os.path.exists(copyFilePath):
                        if refresh and TimeHelper.compareTwoFilsLastModifyTime(dir,copyFilePath) > 0:
                            os.remove(copyFilePath)
                        else:
                            continue
                    try:
                        self.dealMdFile(dir)
                    except UserException as e:
                        self.dealUserException(e)
                    print("已成功处理markdown文件", dir)
        print("所有markdown文档已处理完毕")

    def outputHelpInfo(self):
        sysConfig = Config()
        dirPath = sysConfig.getCurrentDirPath()
        with open(file=dirPath+'\\help.info', mode='r', encoding='UTF-8') as helpFileOpen:
            content = helpFileOpen.read()
            print(content)

    def imgRecovery(self):
        '''使用图床备份中的图片来修复本地的图片库'''
        # 检索当前目录的markdown原始文件
        for dir in os.listdir():
            if os.path.isfile(dir) and self.isOrigMdFile(dir):
                copyFilePath = self.getCopyFilePath(dir)
                if os.path.exists(copyFilePath):
                    # 如果存在图床备份，进行还原操作
                    try:
                        if self.recoveryImgsInMarkdown(copyFilePath, dir):
                            print("已成功还原markdown文件", dir, "的本地图库")
                    except UserException as e:
                        self.dealUserException(e)
        print("所有markdown文档已处理完毕")

    def copyImgFromWeb(self, webImg, localImgPath):
        if localImgPath[0:4] == 'http' or webImg[0:4] != 'http':
            return
        if not os.path.exists(localImgPath):
            downloader = DownloadHelp()
            downloader.chunkDownload(webImg, localImgPath, timeout=2)

    def recoveryImgsInMarkdown(self, copyFilePath: 'copied markdown file path', orignalFile: 'orignal markdown file'):
        '''使用图床图片还原本地图库'''
        # 读取图床备份图片列表
        copyImages = self.findImgsInMdFile(copyFilePath)
        # 读取本地markdown文件原始地址列表
        orignalImages = self.findImgsInMdFile(orignalFile)
        # 还原本地图片库
        if len(copyImages) == len(orignalImages):
            # 如果图片数目正好对等，处理
            imgLength = len(copyImages)
            for i in range(0, imgLength):
                self.copyImgFromWeb(copyImages[i], orignalImages[i])
            return True
        else:
            # 输出错误信息
            print('文件', orignalFile, '中的图片数目与备份中的数目不相符，请自行确认')
            return False

    def changeImgService(self, selectedService):
        supportedService = {'smms', 'ali', 'rruu', 'vimcn'}
        if selectedService not in supportedService:
            print('不支持的图床服务', selectedService)
            return False
        sysConfig = Config()
        if selectedService == 'rruu':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_RRUU)
        elif selectedService == 'ali':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_ALI)
        elif selectedService == 'vimcn':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_VIMCN)
        else:
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_SMMS)
        sysConfig.writeMainConfig()
        print('图床已切换')
        return True

    def changeToken(self, imgService):
        tokenImgServices = {'rruu', 'smms'}
        if imgService not in tokenImgServices:
            print('不是合法的图床', imgService)
            return False
        token = input("请输入新的访问令牌：")
        sysConfig = Config()
        if imgService == 'rruu':
            sysConfig.setConfigParam(Config.PARAM_RRUU_TOKEN, token)
        elif imgService == 'smms':
            sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
        else:
            pass
        sysConfig.writeMainConfig()
        print("已成功更新访问令牌")
        return True

    def scanAndCreateIndex(self):
        '''扫描图片并构建图床索引'''
        imgExt = {'jpg', 'png', 'gif', 'jpeg', 'svg', 'bmp'}
        imageFiles = []
        images = []
        for dir in os.listdir():
            if os.path.isfile(dir):
                fileName, _, fileExt = dir.rpartition('.')
                if fileExt in imgExt:
                    imageFiles.append((fileName, dir))
                    images.append(dir)
        if len(imageFiles) == 0:
            print("没有找到可以处理的图片")
            return True
        imgService = SmmsImg()
        results = {}
        imgService.multiUploadImage(images, results)
        with open(file='markdown_img_index.md', mode='w', encoding='UTF-8') as fopen:
            for imgName, imgFile in imageFiles:
                webImgUrl = results[imgFile]
                print("!["+imgName+"]("+webImgUrl+")", file=fopen)
        print("已成功生成网络图床索引文件：markdown_img_index.md")
        return True
