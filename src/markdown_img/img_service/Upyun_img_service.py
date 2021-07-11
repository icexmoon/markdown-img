from markdown_img.config import Config
from markdown_img.globalization import Globalization
from .img_service import ImgService
from ..user_exception import UserException
import upyun
import os
import urllib.parse


class UpyunImgService(ImgService):
    def __init__(self) -> None:
        super().__init__()
        self._client = None

    def upload(self, localImg: str) -> str:
        client = self.__getUpyunClient()
        fileName = os.path.basename(localImg)
        sysConfig = Config.getInstance()
        info = sysConfig.getConfigParam(Config.PARAM_UPYUN_INFO)
        savedDir = "image"
        if "dir" in info and len(info["dir"]) > 0:
            savedDir = info["dir"]
        domain = info[Config.UPYUN_INFO_DOMAIN]
        with open(localImg, 'rb') as f:
            res = client.put(
                '/{}/{}'.format(savedDir, fileName), f, checksum=False)
        domain = domain.rstrip("/")
        urlEncodeMode = sysConfig.getConfigParam(
            Config.PARAM_URL_ENCODE_MODE)
        if urlEncodeMode == Config.URL_ENCODE_MODE_STANDARD:
            savedDir = urllib.parse.quote(savedDir)
            fileName = urllib.parse.quote(fileName)
        elif urlEncodeMode == Config.URL_ENCODE_MODE_ONLY_SPACE:
            savedDir = savedDir.replace(' ', '%20')
            fileName = fileName.replace(' ', '%20')
        else:
            pass
        return "{}/{}/{}".format(domain, savedDir, fileName)

    def getConfigInfo(self) -> dict:
        sysConfig = Config.getInstance()
        info = sysConfig.getConfigParam(Config.PARAM_UPYUN_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return info

    def inputConfig(self) -> None:
        info = {}
        print(self.globalization.getTextWithColon("upyun_info_required"))
        info[Config.UPYUN_INFO_SERVICE] = input(
            self.globalization.getTextWithColon("upyun_service_input"))
        info[Config.UPYUN_INFO_USERNAME] = input(
            self.globalization.getTextWithColon("upyun_username_input"))
        info[Config.UPYUN_INFO_PASSWORD] = input(
            self.globalization.getTextWithColon("upyun_password_input"))
        info[Config.UPYUN_INFO_DOMAIN] = input(
            self.globalization.getTextWithColon("upyun_domain_input"))
        info[Config.UPYUN_INFO_DIR] = input(
            self.globalization.getTextWithColon("upyun_dir_input"))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_UPYUN_INFO, info)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("config_info_saved"))

    def inputNewConfig(self) -> None:
        info = {}
        info[Config.UPYUN_INFO_SERVICE] = input(
            self.globalization.getTextWithColon("upyun_new_service_input"))
        info[Config.UPYUN_INFO_USERNAME] = input(
            self.globalization.getTextWithColon("upyun_new_username_input"))
        info[Config.UPYUN_INFO_PASSWORD] = input(
            self.globalization.getTextWithColon("upyun_new_password_input"))
        info[Config.UPYUN_INFO_DOMAIN] = input(
            self.globalization.getTextWithColon("upyun_new_domain_input"))
        info[Config.UPYUN_INFO_DIR] = input(
            self.globalization.getTextWithColon("upyun_new_dir_input"))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_UPYUN_INFO, info)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("config_info_saved"))

    def getConfigInfoText(self) -> tuple:
        lines = list()
        info = self.getConfigInfo()
        lines.append(self.globalization.getTextWithParam(
            "upyun_service", info[Config.UPYUN_INFO_SERVICE]))
        lines.append(self.globalization.getTextWithParam(
            "upyun_username", info[Config.UPYUN_INFO_USERNAME]))
        lines.append(self.globalization.getTextWithParam(
            "upyun_password", info[Config.UPYUN_INFO_PASSWORD]))
        lines.append(self.globalization.getTextWithParam(
            "upyun_domain", info[Config.UPYUN_INFO_DOMAIN]))
        lines.append(self.globalization.getTextWithParam(
            "upyun_dir", info[Config.UPYUN_INFO_DIR]))
        return tuple(lines)

    def __getUpyunClient(self):
        info = self.getConfigInfo()
        service = info[Config.UPYUN_INFO_SERVICE]
        username = info[Config.UPYUN_INFO_USERNAME]
        password = info[Config.UPYUN_INFO_PASSWORD]
        if self._client == None:
            self._client = upyun.UpYun(
                service, username, password, timeout=30, endpoint=upyun.ED_AUTO)
        return self._client
