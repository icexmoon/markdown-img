import requests
from .img_service import ImgService
from ..config import Config
from ..user_exception import UserException


class SmmsImgService(ImgService):
    def upload(self, localImg: str) -> str:
        '''上传本地图片到smms,并返回网络图片地址'''
        sysConfig = Config.getInstance()
        configInfo = self.getConfigInfo()
        token = configInfo[Config.PARAM_SMMS_TOKEN]
        headers = {'Authorization': token}
        files = {'smfile': open(localImg, 'rb')}
        url = 'https://sm.ms/api/v2/upload'
        res = requests.post(url, files=files, headers=headers).json()
        if res['success']:
            return res['data']['url']
        elif res['code'] == 'image_repeated':
            return res['images']
        else:
            pass
        sysConfig.writeErrorLog(str(res))
        return False

    def getConfigInfo(self) -> dict:
        sysConfig = Config.getInstance()
        token = sysConfig.getConfigParam(Config.PARAM_SMMS_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return {Config.PARAM_SMMS_TOKEN: token}

    def inputConfig(self) -> None:
        token = input("{}{}".format(self.globalization.getText(
            "missing_smms_token"), self.globalization.getText("colon")))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_has_saved"))

    def getConfigInfoText(self) -> tuple:
        configInfo = self.getConfigInfo()
        token = configInfo[Config.PARAM_SMMS_TOKEN]
        return ("\t{}{}{}".format(self.globalization.getText(
            "acess_token"), self.globalization.getText("colon"), token),)

    def inputNewConfig(self) -> None:
        token = input("{}{}".format(self.globalization.getText("new_token_input"),
                                    self.globalization.getText("colon")))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_SMMS_TOKEN, token)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_changed_successfully"))

