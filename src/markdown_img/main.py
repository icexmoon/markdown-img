from .img_service.img_service import ImgService
from .globalization import Globalization
from .config import Config
import os
from .smms_img import SmmsImg
from .user_exception import UserException
from .download_help import DownloadHelp
from .time_helper import TimeHelper
from .img_service_manager import ImgServiceManager
import re
from .compress.compress_manager import CompressManager
from .config_backup import ConfigBackup


class Main():
    def __init__(self):
        self.globalization: Globalization = Globalization()

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
        return SysConfig.getMarkdownImgDirPath()+SysConfig.getPathSplit()+copyFileName

    def isImgFileName(self, file):
        imgExts = ('.png', '.gif', '.jpg', '.jpeg', '.svg', '.bmp')
        for imgExt in imgExts:
            if file.endswith(imgExt):
                return True
        return False

    def findHtmlImg(self, line, onlyLocal) -> list:
        '''从字符串中查找html标签中的本地图片'''
        findImgs = []
        pattern = re.compile(r"<img src=\"(.+?)\"(.*)/>")
        for matched in pattern.finditer(line):
            imgFile = matched.group(1)
            if self.isImgFileName(imgFile):
                if not onlyLocal:
                    findImgs.append(imgFile)
                elif os.path.exists(imgFile):
                    findImgs.append(imgFile)
                else:
                    pass
        return findImgs

    def findLocalImageFile(self, line: str, localImages: set):
        '''递归查找某段字符串中中括号包裹的内容是否为本地图片'''
        htmlImgs = self.findHtmlImg(line, True)
        if htmlImgs:
            localImages.update(htmlImgs)
        linePart = line.partition('(')
        if len(linePart[2]) > 0:
            secondPart = linePart[2].partition(')')
            content = secondPart[0]
            if len(content) > 0:
                if self.isImgFileName(content) and os.path.exists(content):
                    localImages.add(content)
                    self.findLocalImageFile(content, localImages)

    def findImagesInStr(self, line: str, localImages: list):
        '''递归查找某段字符串中中括号包裹的内容是否为本地图片'''
        htmlImgs = self.findHtmlImg(line, False)
        if htmlImgs:
            localImages.update(htmlImgs)
        linePart = line.partition('(')
        if len(linePart[2]) > 0:
            secondPart = linePart[2].partition(')')
            content = secondPart[0]
            if len(content) > 0:
                if self.isImgFileName(content):
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
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_NO_RRUU_TOKEN:
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_UPLOAD_ERROR:
            currentImgService = sysConfig.getConfigParam(
                Config.PARAM_IMG_SERVICE)
            print(self.globalization.getText("update_image_fail").format(currentImgService),
                  sysConfig.getErrorLogFilePath())
        elif userExp.getErrorCode() == UserException.CODE_TIMEOUT:
            print(userExp.getErrorMsg())
        elif userExp.getErrorCode() == UserException.CODE_NO_YUJIAN_TOKEN:
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_NO_QCLOUD_INFO:
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_NO_IMG_SERVICE_CONFIG:
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_ERROR_INPUT:
            print(userExp.getErrorMsg())
        elif userExp.getErrorCode() == UserException.CODE_NO_QINIU_INFO:
            ImgServiceManager.getImgService().inputConfig()
        elif userExp.getErrorCode() == UserException.CODE_NO_COMPRESS_SERVICE_CONFIG:
            CompressManager.getCompressService().inputConfig()
        else:
            print(self.globalization.getText("undefined_error_info"))
        exit()

    def main(self, refresh=False, configFileName: str = None):
        """生成markdown副本
        refresh: 如果原文件已更新，是否刷新副本
        configFileName: 从指定的配置文件进行加载系统配置
        """
        self.__loadConfigFromFile(configFileName)
        # 检索当前目录中的markdown文件
        for dir in os.listdir():
            if os.path.isfile(dir):
                if self.isOrigMdFile(dir):
                    # 如果副本存在，刷新模式下且原md文件更新过的，删除副本，重新生成，否则不处理
                    copyFilePath = self.getCopyFilePath(dir)
                    if os.path.exists(copyFilePath):
                        if refresh and TimeHelper.compareTwoFilsLastModifyTime(dir, copyFilePath) > 0:
                            os.remove(copyFilePath)
                        else:
                            continue
                    try:
                        self.dealMdFile(dir)
                    except UserException as e:
                        self.dealUserException(e)
                    print(self.globalization.getText("deal_success"), dir)
        print(self.globalization.getText("all_file_done"))

    def outputHelpInfo(self):
        sysConfig = Config()
        helpFilePath = sysConfig.getHelpFilePath()
        with open(file=helpFilePath, mode='r', encoding='UTF-8') as helpFileOpen:
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
                            # print("已成功还原markdown文件", dir, "的本地图库")
                            print(self.globalization.getText(
                                "recove_markdown_file").format(dir))
                    except UserException as e:
                        self.dealUserException(e)
        print(self.globalization.getText("all_file_done"))

    def copyImgFromWeb(self, webImg, localImgPath):
        if localImgPath[0:4] == 'http' or webImg[0:4] != 'http':
            return
        if not os.path.exists(localImgPath):
            downloader = DownloadHelp()
            downloader.chunkDownload(webImg, localImgPath, timeout=2)

    def recoveryImgsInMarkdown(self, copyFilePath: str, orignalFile: str):
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
            # print('文件', orignalFile, '中的图片数目与备份中的数目不相符，请自行确认')
            print(self.globalization.getText(
                "images_number_is_not_equal").format(orignalFile))
            return False

    def changeImgService(self, selectedService):
        if not ImgServiceManager.isValidImgServiceFlag(selectedService):
            print(self.globalization.getText(
                "not_support_img_service"), selectedService)
            return False
        sysConfig = Config()
        sysConfig.setConfigParam(Config.PARAM_IMG_SERVICE, selectedService)
        sysConfig.writeMainConfig()
        ImgServiceManager.updateImgService()
        print(self.globalization.getText("image_bed_changed"))
        return True

    def changeToken(self, imgService):
        if imgService != "this" and (not ImgServiceManager.isValidImgServiceFlag(imgService)):
            print(self.globalization.getText("invalid_image_bed"), imgService)
            return False
        service: ImgService
        if imgService == 'this':
            service = ImgServiceManager.getImgService()
        else:
            service = ImgServiceManager.getImgServiceByFlag(imgService)
        service.inputNewConfig()
        return True

    def __loadConfigFromFile(self, configFileName: str) -> None:
        """从指定的配置文件名称加载系统配置
        configFileName: 配置文件名称
        """
        sysConfig = Config.getInstance()
        if configFileName is not None:
            # 根据文件名获取对应的配置文件
            configFile: str = ConfigBackup.getConfigBackupFile(
                sysConfig, configFileName)
            if not os.path.exists(configFile):
                print(self.globalization.getText("no_config_file"))
                return
            else:
                sysConfig.loadConfigFile(configFile)

    def scanAndCreateIndex(self, configFileName: str = None):
        '''扫描图片并构建图床索引
        configFileName: 配置文件名称
        '''
        self.__loadConfigFromFile(configFileName)
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
            print(self.globalization.getText("no_find_local_image"))
            return True
        imgService = SmmsImg()
        results = {}
        try:
            imgService.multiUploadImage(images, results)
        except UserException as e:
            self.dealUserException(e)
        with open(file='markdown_img_index.md', mode='w', encoding='UTF-8') as fopen:
            for imgName, imgFile in imageFiles:
                webImgUrl = results[imgFile]
                print("!["+imgName+"]("+webImgUrl+")\n", file=fopen)
        print(self.globalization.getText("index_file_created"))
        return True

    def changeImgServiceOption(self, imgServiceFlag, options):
        '''修改图床服务的部分配置'''
        sysConfig = Config()
        if imgServiceFlag == Config.IMG_SERVICE_QCLOUD:
            try:
                qCloudInfo = sysConfig.getQCloudInfo()
            except UserException as e:
                self.dealUserException(e)
            if Config.QCLOUD_INFO_DES_DIR in options and options[Config.QCLOUD_INFO_DES_DIR]:
                qCloudInfo[Config.QCLOUD_INFO_DES_DIR] = options[Config.QCLOUD_INFO_DES_DIR]
            sysConfig.setConfigParam(Config.PARAM_QCLOUD_INFO, qCloudInfo)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("image_web_configs_changed"))

    def changeMainPrams(self, params: dict):
        '''用户修改主配置参数'''
        sysConfig = Config()
        for key, value in params.items():
            if key == Config.PARAM_URL_ENCODE_MODE:
                if value in (Config.URL_ENCODE_MODE_NONE, Config.URL_ENCODE_MODE_ONLY_SPACE, Config.URL_ENCODE_MODE_STANDARD):
                    sysConfig.setConfigParam(
                        Config.PARAM_URL_ENCODE_MODE, value)
                else:
                    exp = UserException(
                        UserException.CODE_ERROR_INPUT, self.globalization.getText("input_error_and_hint").format(value))
                    self.dealUserException(exp)
            elif key == Config.PARAM_LANGUAGE:
                if value in (Config.LANGUAGE_CN, Config.LANGUAGE_EN):
                    sysConfig.setConfigParam(Config.PARAM_LANGUAGE, value)
                else:
                    exp = UserException(
                        UserException.CODE_ERROR_INPUT, self.globalization.getText("input_error_and_hint").format(value))
                    self.dealUserException(exp)
            elif key == Config.PARAM_DEBUG:
                if value in (Config.DEBUG_ON, Config.DEBUG_OFF):
                    sysConfig.setConfigParam(Config.PARAM_DEBUG, value)
                else:
                    exp = UserException(
                        UserException.CODE_ERROR_INPUT, self.globalization.getText("input_error_and_hint").format(value))
                    self.dealUserException(exp)
            elif key == Config.PARAM_COMPRESS_ENGINE:
                if value in (Config.COMPRESS_ENGINE_GIL, Config.COMPRESS_ENGINE_TIYPNG, Config.COMPRESS_ENGINE_NONE):
                    sysConfig.setConfigParam(
                        Config.PARAM_COMPRESS_ENGINE, value)
                else:
                    exp = UserException(UserException.CODE_ERROR_INPUT, self.globalization.getText(
                        "input_error_and_hint"))
            else:
                pass
        sysConfig.writeMainConfig()
        print(self.globalization.getText("related_configs_changed"))

    def printSysInfo(self):
        '''打印当前系统相关信息'''
        sysConfig = Config()
        import pkg_resources
        version = pkg_resources.get_distribution(
            'markdown-img-icexmoon').version
        print("{}{}{}".format(self.globalization.getText(
            "program_version"), self.globalization.getText("colon"), version))
        try:
            language = sysConfig.getConfigParam(Config.PARAM_LANGUAGE)
            languageText = ""
            if language == Config.LANGUAGE_EN:
                languageText = "English"
            elif language == Config.LANGUAGE_CN:
                languageText = "中文"
            else:
                pass
            print("{}{}{}".format(self.globalization.getText(
                "working_language"), self.globalization.getText("colon"), languageText))
            print("DEBUG{}{}".format(self.globalization.getText(
                "colon"), sysConfig.getConfigParam(Config.PARAM_DEBUG)))
            imgService = sysConfig.getConfigParam(Config.PARAM_IMG_SERVICE)
            print("{}{}{}".format(self.globalization.getText(
                "current_used_image_bed"), self.globalization.getText("colon"), imgService))
            urlEncodeMode = sysConfig.getConfigParam(
                Config.PARAM_URL_ENCODE_MODE)
            urlEncodeModeText = ''
            if urlEncodeMode == Config.URL_ENCODE_MODE_NONE:
                urlEncodeModeText = self.globalization.getText("no_use")
            elif urlEncodeMode == Config.URL_ENCODE_MODE_ONLY_SPACE:
                urlEncodeModeText = self.globalization.getText(
                    "use_only_for_spaces")
            else:
                urlEncodeModeText = self.globalization.getText(
                    "encoding_all_non_ascii_characters")
            print("{}{}{}".format(self.globalization.getText(
                "whether_to_use_url_encoding"), self.globalization.getText("colon"), urlEncodeModeText))
            # 输出图片压缩相关设置
            lines = CompressManager.getCompressService().getCompressInfoLInes()
            for line in lines:
                print(line)
            print("{}{}".format(self.globalization.getText(
                "image_bed_configs"), self.globalization.getText("colon")))
            ImgServiceManager.getImgService().printConfigInfo()
        except UserException as e:
            self.dealUserException(e)

    def inputCompressInfo(self):
        CompressManager.getCompressService().inputConfig()
        return

    def backupConfig(self, fileName=None) -> None:
        """对配置文件进行备份"""
        sysConfig = Config.getInstance()
        result = False
        if fileName is None:
            # 未指定文件名，直接复制
            result = ConfigBackup.backupConfig(sysConfig)
        else:
            fileName = str(fileName)
            desPath = ConfigBackup.getConfigBackupFile(sysConfig, fileName)
            if os.path.exists(desPath):
                choice = input(self.globalization.getText(
                    "same_config_backup_exist"))
                if choice == "n":
                    print(self.globalization.getText(
                        "backup_operate_canceled"))
                    return
            result = ConfigBackup.backupConfig(
                sysConfig, fileName, override=True)
        if result is False:
            print(self.globalization.getText("config_backup_error"))
        else:
            print(self.globalization.getText(
                "config_backup_success").format(result))

    def listConfigBackup(self) -> None:
        """列出已保存的自定义配置"""
        sysConfig = Config.getInstance()
        configBackups: list = ConfigBackup.getConfigBackup(sysConfig)
        print("{:<25s} {:<10s}".format(self.globalization.getText("config_name"),self.globalization.getText("create_time")))
        for configName, ctime, absPath in configBackups:
            print("{:<25s} {:<10s}".format(configName, ctime))

    def changeConfig(self, configFileName: str) -> None:
        """使用指定配置覆盖当前配置"""
        sysConfig = Config.getInstance()
        configFile: str = ConfigBackup.getConfigBackupFile(
            sysConfig,  configFileName)
        if not os.path.exists(configFile):
            print(self.globalization.getText("no_config_file"))
            return
        if input(self.globalization.getText("config_change_confirm")) != 'y':
            print(self.globalization.getText("current_operation_canceld"))
            return
        sysConfig.replaceConfigFile(configFile)
        print(self.globalization.getText("current_operation_success"))
