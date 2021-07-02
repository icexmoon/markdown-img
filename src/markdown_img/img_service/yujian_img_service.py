from .img_service import ImgService
import requests
from ..config import Config
from ..user_exception import UserException
import json


class YujianImgService(ImgService):
    API_TYPE_YUJIAN = "this"
    API_TYPE_BILIBILI = "bilibili" # bilibili
    API_TYPE_SOUGOU = "sougou" # 搜狗
    API_TYPE_HULUXIA = "huluxia" # 葫芦
    API_TYPE_CATBOX = "catbox" # 猫盒
    API_TYPE_QIHOO = "qihoo" # 360
    API_TYPE_POSTIMAGES = "postimages" # 贴图
    API_TYPE_AI58 = "ai58" # 58
    API_TYPE_GTIMG = "gtimg" # 极图
    API_TYPE_BKIMG = "bkimg" # 佰书
    API_TYPE_MUKE = "muke" # 慕课
    API_TYPE_ALI = "ali" # 阿里

    def __init__(self, apiType: str = "this") -> None:
        super().__init__()
        self.__apiType = apiType

    def setApiType(self, apiType: str) -> None:
        self.__apiType = apiType

    def upload(self, localImg: str) -> str:
        '''上传到遇见图床'''
        imgOpen = open(localImg, 'rb')
        files = {'image': imgOpen}
        apiType = self.__apiType
        sysConfig = Config.getInstance()
        configInfo = self.getConfigInfo()
        token = configInfo[Config.PARAM_YUJIAN_TOKEN]
        r = requests.post('https://www.hualigs.cn/api/upload',
                          data={'apiType': apiType, 'privateStorage': '', 'token': token}, files=files)
        imgOpen.close()
        try:
            respJson = r.json()
        except json.decoder.JSONDecodeError as e:
            sysConfig.writeErrorLog("接口解析错误："+str(e)+"\n返回信息："+r.text)
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        except Exception as e:
            sysConfig.writeErrorLog("未知的接口调用错误:"+str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR)
        urls = {}
        if str(respJson['code']).strip() == '200' and str(respJson['msg']).strip() == 'success':
            urls = respJson['data']['url']
        else:
            return False
        if apiType == self.__class__.API_TYPE_YUJIAN or apiType == "":
            return urls["distribute"]
        if apiType in urls:
            return urls[apiType]
        return urls[YujianImgService.API_TYPE_YUJIAN]

    def getConfigInfo(self) -> dict:
        sysConfig = Config.getInstance()
        token = sysConfig.getConfigParam(Config.PARAM_YUJIAN_TOKEN)
        if token == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return {Config.PARAM_YUJIAN_TOKEN: token}

    def inputConfig(self) -> None:
        token = input("{}{}".format(self.globalization.getText("missing_meet_token"),
                                    self.globalization.getText("colon")))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_YUJIAN_TOKEN, token)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_has_saved"))

    def getConfigInfoText(self) -> tuple:
        configInfo = self.getConfigInfo()
        token = configInfo[Config.PARAM_YUJIAN_TOKEN]
        return ("\t{}{}{}".format(self.globalization.getText(
            "acess_token"), self.globalization.getText("colon"), token),)

    def inputNewConfig(self) -> None:
        token = input("{}{}".format(self.globalization.getText("new_token_input"),
                                    self.globalization.getText("colon")))
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_YUJIAN_TOKEN, token)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_changed_successfully"))

