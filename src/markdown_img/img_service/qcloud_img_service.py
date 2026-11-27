from .img_service import ImgService
from ..config import Config
from ..user_exception import UserException
from ..qcloud_client import QcloudClient
import qcloud_cos.cos_exception


class QcloudImgService(ImgService):
    def __init__(self) -> None:
        super().__init__()

    def getClient(self, clientInfo=None):
        if clientInfo is None:
            clientInfo = self.getConfigInfo()
        required = (
            Config.QCLOUD_INFO_SECRET_ID, Config.QCLOUD_INFO_SECRET_KEY,
            Config.QCLOUD_INFO_REGION, Config.QCLOUD_INFO_BUCKET,
            Config.QCLOUD_INFO_DES_DIR,
        )
        if not isinstance(clientInfo, dict):
            raise UserException(
                UserException.CODE_UPLOAD_ERROR,
                self.globalization.getText("qcloud_invalid_config"),
            )
        invalid = [
            key for key in required
            if not isinstance(clientInfo.get(key), str)
            or (key != Config.QCLOUD_INFO_DES_DIR and not clientInfo[key])
        ]
        if invalid:
            raise UserException(
                UserException.CODE_UPLOAD_ERROR,
                self.globalization.getText("qcloud_invalid_fields").format(", ".join(invalid)),
            )
        if not hasattr(self, "qclient"):
            self.qclient = QcloudClient(clientInfo[Config.QCLOUD_INFO_SECRET_ID],
                                        clientInfo[Config.QCLOUD_INFO_SECRET_KEY],
                                        clientInfo[Config.QCLOUD_INFO_REGION],
                                        clientInfo[Config.QCLOUD_INFO_BUCKET])
        return self.qclient

    def upload(self, localImg: str) -> str:
        '''上传到腾讯云'''
        sysConfig = Config.getInstance()
        try:
            clientInfo = self.getConfigInfo()
            client = self.getClient(clientInfo)
            urlEncodeMode = sysConfig.getConfigParam(
                Config.PARAM_URL_ENCODE_MODE)
            url = client.upload(
                localImg, clientInfo[Config.QCLOUD_INFO_DES_DIR], urlEncodeMode)
        except OSError as e:
            raise UserException(UserException.CODE_UPLOAD_ERROR,
                                self.globalization.getText("upload_file_error").format(str(e))) from e
        except qcloud_cos.cos_exception.CosException as e:
            raise UserException(
                UserException.CODE_UPLOAD_ERROR,
                QcloudClient._errorText("qcloud_client_failed", e)
            ) from e
        except RuntimeError as e:
            raise UserException(UserException.CODE_UPLOAD_ERROR, str(e)) from e
        return url

    def delete(self, key: str) -> None:
        try:
            self.getClient().delete(key)
        except qcloud_cos.cos_exception.CosException as e:
            raise UserException(
                UserException.CODE_UPLOAD_ERROR,
                QcloudClient._errorText("qcloud_delete_failed", e)
            ) from e
        except RuntimeError as e:
            raise UserException(UserException.CODE_UPLOAD_ERROR, str(e)) from e

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

