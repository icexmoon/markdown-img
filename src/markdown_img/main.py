from qiniu import config
from .globalization import Globalization
from .config import Config
import os
from .smms_img import SmmsImg
from .user_exception import UserException
from .download_help import DownloadHelp
from .time_helper import TimeHelper
import re


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
        return SysConfig.getMarkdownImgDirPath()+'\\'+copyFileName

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
            token = input("{}{}".format(self.globalization.getText(
                "missing_smms_token", self.globalization.getText("colon"))))
            sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
            sysConfig.writeMainConfig()
            print(self.globalization.getText("token_has_saved"))
        elif userExp.getErrorCode() == UserException.CODE_NO_RRUU_TOKEN:
            token = input("{}{}".format(self.globalization.getText("missing_ruyu_token"),
                                        self.globalization("colon")))
            sysConfig.setConfigParam(Config.PARAM_RRUU_TOKEN, token)
            sysConfig.writeMainConfig()
            print(self.globalization.getText("token_has_saved"))
        elif userExp.getErrorCode() == UserException.CODE_UPLOAD_ERROR:
            currentImgService = sysConfig.getConfigParam(
                Config.PARAM_IMG_SERVICE)
            print(self.globalization.getText("update_image_fail").format(currentImgService),
                  sysConfig.getErrorLogFilePath())
        elif userExp.getErrorCode() == UserException.CODE_TIMEOUT:
            print(userExp.getErrorMsg())
        elif userExp.getErrorCode() == UserException.CODE_NO_YUJIAN_TOKEN:
            token = input("{}{}".format(self.globalization.getText("missing_meet_token"),
                                        self.globalization.getText("colon")))
            sysConfig.setConfigParam(Config.PARAM_YUJIAN_TOKEN, token)
            sysConfig.writeMainConfig()
            print(self.globalization.getText("token_has_saved"))
        elif userExp.getErrorCode() == UserException.CODE_NO_QCLOUD_INFO:
            qcloudInfo = {}
            print("{}{}".format(self.globalization("missing_tencent_oss_info"),
                                self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_SECRET_ID] = input("{}{}".format(self.globalization.getText("secret_id_input"),
                                                                           self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_SECRET_KEY] = input(
                "{}{}".format(self.globalization.getText("secret_key_input"),
                              self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_REGION] = input("{}{}".format(self.globalization.getText("region_input"),
                                                                        self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_BUCKET] = input("{}{}".format(
                self.globalization.getText("bucket_input"), self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_DES_DIR] = input("{}{}".format(self.globalization.getText("storage_dir_input"),
                                                                         self.globalization.getText("colon")))
            sysConfig.setConfigParam(Config.PARAM_QCLOUD_INFO, qcloudInfo)
            sysConfig.writeMainConfig()
            print(self.globalization.getText("tencent_oss_info_saved"))
        elif userExp.getErrorCode() == UserException.CODE_ERROR_INPUT:
            print(userExp.getErrorMsg())
        elif userExp.getErrorCode() == UserException.CODE_NO_QINIU_INFO:
            qiniuInfo = {}
            print("{}{}".format(self.globalization.getText("qiniu_info_required"),
                                self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_ACCESS_KEY] = input("{}{}".format(self.globalization.getText("qiniu_access_key_input"),
                                                                          self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_SECRET_KEY] = input("{}{}".format(self.globalization.getText("qiniu_secret_key_input"),
                                                                          self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_DNS_DOMAIN] = input("{}{}".format(self.globalization.getText("qiniu_dns_domain_input"),
                                                                          self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_BUCKET_NAME] = input("{}{}".format(self.globalization.getText("qiniu_bucket_name_input"),
                                                                           self.globalization.getText("colon")))
            sysConfig.setConfigParam(Config.PARAM_QINIU_INFO, qiniuInfo)
            sysConfig.writeMainConfig()
            print(self.globalization.getText("qiniu_info_saved"))
        else:
            print(self.globalization.getText("undefined_error_info"))
        exit()

    def main(self, refresh=False):
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
        supportedService = {'smms', 'ali', 'rruu',
                            'vimcn', 'yujian', 'ali2', 'qcloud', 'qiniu'}
        if selectedService not in supportedService:
            print(self.globalization.getText(
                "not_support_img_service"), selectedService)
            return False
        sysConfig = Config()
        if selectedService == 'rruu':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_RRUU)
        elif selectedService == 'ali':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_ALI)
        elif selectedService == 'ali2':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_ALI2)
        elif selectedService == 'vimcn':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_VIMCN)
        elif selectedService == 'yujian':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_YUJIAN)
        elif selectedService == 'qcloud':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_QCLOUD)
        elif selectedService == 'qiniu':
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_QINIU)
        else:
            sysConfig.setConfigParam(
                Config.PARAM_IMG_SERVICE, Config.IMG_SERVICE_SMMS)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("image_bed_changed"))
        return True

    def changeToken(self, imgService):
        tokenImgServices = {'rruu', 'smms', 'yujian', 'qcloud', 'qiniu'}
        if imgService not in tokenImgServices:
            print(self.globalization.getText("invalid_image_bed"), imgService)
            return False
        sysConfig = Config()
        if imgService == 'qcloud':
            qcloudInfo = {}
            qcloudInfo[Config.QCLOUD_INFO_SECRET_ID] = input("{}{}".format(self.globalization.getText("new_secret_id_input"),
                                                                           self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_SECRET_KEY] = input(
                "{}{}".format(self.globalization.getText("new_secret_key_input"),
                              self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_REGION] = input("{}{}".format(self.globalization.getText("new_region_input"),
                                                                        self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_BUCKET] = input("{}{}".format(self.globalization.getText("new_bucket_input"),
                                                                        self.globalization.getText("colon")))
            qcloudInfo[Config.QCLOUD_INFO_DES_DIR] = input("{}{}".format(self.globalization.getText("new_storage_dir_input"),
                                                                         self.globalization.getText("colon")))
            sysConfig.setConfigParam(Config.PARAM_QCLOUD_INFO, qcloudInfo)
        elif imgService == 'qiniu':
            qiniuInfo = {}
            qiniuInfo[Config.QINIU_INFO_ACCESS_KEY] = input("{}{}".format(self.globalization.getText(
                "qiniu_new_access_key_input"), self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_SECRET_KEY] = input("{}{}".format(self.globalization.getText(
                "qiniu_new_secret_key_input"), self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_DNS_DOMAIN] = input("{}{}".format(self.globalization.getText(
                "qiniu_new_dns_domain_input"), self.globalization.getText("colon")))
            qiniuInfo[Config.QINIU_INFO_BUCKET_NAME] = input("{}{}".format(self.globalization.getText(
                "qiniu_new_bucket_name_input"), self.globalization.getText("colon")))
            sysConfig.setConfigParam(Config.PARAM_QINIU_INFO, qiniuInfo)
        else:
            token = input("{}{}".format(self.globalization.getText("new_token_input"),
                                        self.globalization.getText("colon")))
            if imgService == 'rruu':
                sysConfig.setConfigParam(Config.PARAM_RRUU_TOKEN, token)
            elif imgService == 'smms':
                sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
            elif imgService == 'yujian':
                sysConfig.setConfigParam(Config.PARAM_YUJIAN_TOKEN, token)
            else:
                pass
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_changed_successfully"))
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
            print("{}{}".format(self.globalization.getText(
                "image_bed_configs"), self.globalization.getText("colon")))
            if imgService == Config.IMG_SERVICE_QCLOUD:
                # 显示腾讯云相关配置信息
                qcloudInfo = sysConfig.getQCloudInfo()
                print("\t{}{}{}".format(self.globalization.getText("storage_bucket"),
                      self.globalization.getText("colon"), qcloudInfo[Config.QCLOUD_INFO_BUCKET]))
                print("\tsecret_id:{}".format(
                    qcloudInfo[Config.QCLOUD_INFO_SECRET_ID]))
                print("\tsecret_key:{}".format(
                    qcloudInfo[Config.QCLOUD_INFO_SECRET_KEY]))
                print("\t{}{}{}".format(self.globalization.getText(
                    "region"), self.globalization.getText("colon"), qcloudInfo[Config.QCLOUD_INFO_REGION]))
                print("\t{}{}{}".format(self.globalization.getText("storage_directory"),
                                        self.globalization.getText("colon"),
                                        qcloudInfo[Config.QCLOUD_INFO_DES_DIR]))
            elif imgService == Config.IMG_SERVICE_QINIU:
                # 显示七牛云相关配置信息
                qiniuInfo = sysConfig.getQiniuInfo()
                print("\t{}{}{}".format(self.globalization.getText("qiniu_access_key"),
                      self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_ACCESS_KEY]))
                print("\t{}{}{}".format(self.globalization.getText("qiniu_secret_key"),
                      self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_SECRET_KEY]))
                print("\t{}{}{}".format(self.globalization.getText("qiniu_dns_domain"),
                      self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_DNS_DOMAIN]))
                print("\t{}{}{}".format(self.globalization.getText("qiniu_bucket_name"),
                      self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_BUCKET_NAME]))
            else:
                if imgService == Config.IMG_SERVICE_ALI or imgService == Config.IMG_SERVICE_YUJIAN:
                    token = sysConfig.getYujianToken()
                elif imgService == Config.IMG_SERVICE_ALI2 or imgService == Config.IMG_SERVICE_RRUU:
                    token = sysConfig.getRruuToken()
                elif imgService == Config.IMG_SERVICE_SMMS:
                    token = sysConfig.getSmmsToken()
                else:
                    token = ''
                print("\t{}{}{}".format(self.globalization.getText(
                    "acess_token"), self.globalization.getText("colon"), token))
        except UserException as e:
            self.dealUserException(e)
