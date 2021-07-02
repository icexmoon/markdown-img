from .img_service import ImgService
from ..config import Config
from ..user_exception import UserException
from ..qiniu_client import QiniuClient


class QiniuImgService(ImgService):
    def upload(self, localImg: str) -> str:
        "上传到七牛云"
        clientInfo = self.getConfigInfo()
        client = QiniuClient()
        dnsDomain = clientInfo[Config.QINIU_INFO_DNS_DOMAIN]
        accessKey = clientInfo[Config.QINIU_INFO_ACCESS_KEY]
        secretKey = clientInfo[Config.QINIU_INFO_SECRET_KEY]
        bucketName = clientInfo[Config.QINIU_INFO_BUCKET_NAME]
        sysConfig = Config.getInstance()
        try:
            url = client.upload(localImg, dnsDomain, accessKey,
                                secretKey, bucketName)
        except UserException as e:
            sysConfig.writeErrorLog(e.getErrorMsg())
            return False
        return url

    def getConfigInfo(self) -> dict:
        """获取七牛云的详细配置"""
        sysConfig = Config.getInstance()
        info = sysConfig.getConfigParam(Config.PARAM_QINIU_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return info

    def inputConfig(self) -> None:
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
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_QINIU_INFO, qiniuInfo)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("qiniu_info_saved"))

    def getConfigInfoText(self) -> tuple:
        lines = list()
        qiniuInfo = self.getConfigInfo()
        lines.append("\t{}{}{}".format(self.globalization.getText("qiniu_access_key"),
                                       self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_ACCESS_KEY]))
        lines.append("\t{}{}{}".format(self.globalization.getText("qiniu_secret_key"),
                                       self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_SECRET_KEY]))
        lines.append("\t{}{}{}".format(self.globalization.getText("qiniu_dns_domain"),
                                       self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_DNS_DOMAIN]))
        lines.append("\t{}{}{}".format(self.globalization.getText("qiniu_bucket_name"),
                                       self.globalization.getText("colon"), qiniuInfo[Config.QINIU_INFO_BUCKET_NAME]))
        return tuple(lines)

    def inputNewConfig(self) -> None:
        sysConfig = Config.getInstance()
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
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_changed_successfully"))

