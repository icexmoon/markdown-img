from .img_service import ImgService
from .yujian_img_service import YujianImgService
class BilibiliImgService(ImgService):
    def __init__(self) -> None:
        super().__init__()
        yujianImgService = YujianImgService()
        yujianImgService.setApiType(YujianImgService.API_TYPE_BILIBILI)
        self.__proxyImgService: ImgService = yujianImgService

    def upload(self, localImg: str) -> str:
        return self.__proxyImgService.upload(localImg)

    def getConfigInfo(self) -> dict:
        return self.__proxyImgService.getConfigInfo()

    def inputConfig(self) -> None:
        self.__proxyImgService.inputConfig()

    def getConfigInfoText(self) -> tuple:
        return self.__proxyImgService.getConfigInfoText()

    def inputNewConfig(self) -> None:
        return self.__proxyImgService.inputNewConfig()