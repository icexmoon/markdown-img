from abc import ABC, abstractmethod
from ..globalization import Globalization
from ..config import Config


class CompressService(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.globalization = Globalization()

    def inputConfig(self) -> None:
        """输入压缩服务的相关配置,此方法不应该被子类重写"""
        print(self.globalization.getTextWithColon("compress_info_input_tips"))
        info = {}
        # info[Config.COMPRESS_ENGINE] = input(
        #     self.globalization.getTextWithColon("compress_engine"))
        info[Config.COMPRESS_INFO_STATUS] = input(
            self.globalization.getTextWithColon("compress_status_input"))
        info[Config.COMPRESS_INFO_LIMIT] = input(
            self.globalization.getTextWithColon("compress_limit_input"))
        self._inputOtherConfig(info)
        sysConfig = Config.getInstance()
        sysConfig.setConfigParam(Config.PARAM_COMPRESS, info)
        sysConfig.writeMainConfig()
        print(self.globalization.getText("config_info_saved"))

    def getCompressInfo(self) -> None:
        info = Config.getInstance().getCompressInfo()
        self._checkOtherConfig(info)
        return info

    @abstractmethod
    def _checkOtherConfig(self, info: dict) -> None:
        """子类通过此方法检查是否包含必要配置"""

    @abstractmethod
    def _inputOtherConfig(self, info: dict) -> None:
        """子类通过此方法输入定制化参数"""
        pass

    @abstractmethod
    def compress(self, reginalImg: str, destImg: str) -> None:
        """压缩图片
        reginalImg: 原始图片路径
        destImg: 目标图片路径
        """
        pass

    def getCompressInfoLInes(self) -> tuple:
        """获取图片压缩功能相关信息"""
        sysConfig = Config.getInstance()
        compressInfo = sysConfig.getCompressInfo()
        lines = []
        lines.append(self.globalization.getTextWithParam(
            "compress_engine_text", sysConfig.getConfigParam(Config.PARAM_COMPRESS_ENGINE)))
        lines.append(self.globalization.getTextWithParam(
            "compress_status", compressInfo[Config.COMPRESS_INFO_STATUS]))
        lines.append(self.globalization.getTextWithParam(
            "compress_limit", compressInfo[Config.COMPRESS_INFO_LIMIT]))
        self._addCompressEngineInfo(lines)
        return tuple(lines)

    @abstractmethod
    def _addCompressEngineInfo(self, lines: list) -> None:
        """子类通过此方法添加特殊的图片压缩服务相关配置信息"""
        pass
