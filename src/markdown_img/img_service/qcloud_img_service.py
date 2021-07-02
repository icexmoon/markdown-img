from .img_service import ImgService
from ..config import Config
from ..user_exception import UserException
from ..qcloud_client import QcloudClient
import qcloud_cos.cos_exception


class QcloudImgService(ImgService):
    def __init__(self) -> None:
        super().__init__()

    def upload(self, localImg: str) -> str:
        '''上传到腾讯云'''
        clientInfo = self.getConfigInfo()
        if not hasattr(self, "qclient"):
            self.qclient = QcloudClient(clientInfo[Config.QCLOUD_INFO_SECRET_ID],
                                        clientInfo[Config.QCLOUD_INFO_SECRET_KEY],
                                        clientInfo[Config.QCLOUD_INFO_REGION],
                                        clientInfo[Config.QCLOUD_INFO_BUCKET])
        sysConfig = Config.getInstance()
        try:
            urlEncodeMode = sysConfig.getConfigParam(
                Config.PARAM_URL_ENCODE_MODE)
            url = self.qclient.upload(
                localImg, clientInfo[Config.QCLOUD_INFO_DES_DIR], urlEncodeMode)
        except qcloud_cos.cos_exception.CosServiceError as e:
            sysConfig.writeErrorLog(str(e))
            return False
        return url

    def getConfigInfo(self) -> dict:
        sysConfig = Config.getInstance()
        info = sysConfig.getConfigParam(Config.PARAM_QCLOUD_INFO)
        if info == '':
            raise UserException(UserException.CODE_NO_IMG_SERVICE_CONFIG)
        return info

    def inputConfig(self) -> None:
        sysConfig = Config.getInstance()
        qcloudInfo = {}
        print("{}{}".format(self.globalization.getText("missing_tencent_oss_info"),
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

    def getConfigInfoText(self) -> tuple:
        lines: list = list()
        qcloudInfo = self.getConfigInfo()
        lines.append("\t{}{}{}".format(self.globalization.getText("storage_bucket"),
                                       self.globalization.getText("colon"), qcloudInfo[Config.QCLOUD_INFO_BUCKET]))
        lines.append("\tsecret_id:{}".format(
            qcloudInfo[Config.QCLOUD_INFO_SECRET_ID]))
        lines.append("\tsecret_key:{}".format(
            qcloudInfo[Config.QCLOUD_INFO_SECRET_KEY]))
        lines.append("\t{}{}{}".format(self.globalization.getText(
            "region"), self.globalization.getText("colon"), qcloudInfo[Config.QCLOUD_INFO_REGION]))
        lines.append("\t{}{}{}".format(self.globalization.getText("storage_directory"),
                                       self.globalization.getText("colon"),
                                       qcloudInfo[Config.QCLOUD_INFO_DES_DIR]))
        return tuple(lines)

    def inputNewConfig(self) -> None:
        sysConfig = Config.getInstance()
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
        sysConfig.writeMainConfig()
        print(self.globalization.getText("token_changed_successfully"))

