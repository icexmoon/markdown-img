from abc import ABC, abstractmethod
from ..globalization import Globalization


class ImgService(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.globalization = Globalization()

    "图床服务抽象基类"
    @abstractmethod
    def upload(self, localImg: str) -> str:
        "上传图片到图床，并返回url"
        pass

    @abstractmethod
    def getConfigInfo(self) -> dict:
        "获取图床相关配置"
        pass

    @abstractmethod
    def inputConfig(self) -> None:
        """用户输入配置信息"""
        pass

    @abstractmethod
    def inputNewConfig(self) -> None:
        """用户输入新的配置信息"""
        pass

    @abstractmethod
    def getConfigInfoText(self)->tuple:
        """获取配置的文本信息"""
        pass

    def printConfigInfo(self)->None:
        """打印图床的配置信息"""
        for line in self.getConfigInfoText():
            print(line)
