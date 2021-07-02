from .img_service import ImgService
class NoneImgService(ImgService):
    "空的图片服务，用于占位"
    def upload(self, localImg: str) -> str:
        return ""

    def getConfigInfo(self) -> dict:
        return dict()

    def inputConfig(self) -> None:
        pass

    def getConfigInfoText(self) -> tuple:
        return (" ",)

    def inputNewConfig(self) -> None:
        pass