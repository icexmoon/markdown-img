from .config import Config
from .img_service.img_service import ImgService
from .img_service.none_img_service import NoneImgService
from .img_service.vimcn_img_service import VimcnImgService
from .img_service.yujian_img_service import YujianImgService
from .img_service.qcloud_img_service import QcloudImgService
from .img_service.qiniu_img_service import QiniuImgService
from .img_service.smms_img_service import SmmsImgService
from .img_service.Upyun_img_service import UpyunImgService


class ImgServiceManager:
    @classmethod
    def getImgService(cls) -> ImgService:
        if not hasattr(cls, "__imgservice"):
            setattr(cls, "__imgservice", cls.__getImgServiceByConfig())
        return getattr(cls, "__imgservice")

    @classmethod
    def updateImgService(cls) -> None:
        if hasattr(cls, "__imgservice"):
            setattr(cls, "__imgservice", cls.__getImgServiceByConfig())

    @classmethod
    def __getImgServiceByConfig(cls) -> ImgService:
        """根据当前系统配置返回合适的图片服务"""
        sysConfig = Config.getInstance()
        imgService = sysConfig.getConfigParam(
            Config.PARAM_IMG_SERVICE)
        return cls.getImgServiceByFlag(imgService)

    @classmethod
    def getImgServiceByFlag(cls, flag: str) -> ImgService:
        """根据图片服务标识获取相应的图片服务
        flag: 图片服务标识
        """
        webImage: ImgService
        imgService = flag
        if imgService == Config.IMG_SERVICE_ALI:
            webImage = YujianImgService(YujianImgService.API_TYPE_ALI)
        elif imgService == Config.IMG_SERVICE_ALI2:
            webImage = YujianImgService(YujianImgService.API_TYPE_ALI)
        elif imgService == Config.IMG_SERVICE_RRUU:
            webImage = NoneImgService()
        elif imgService == Config.IMG_SERVICE_VIMCN:
            webImage = VimcnImgService()
        elif imgService == Config.IMG_SERVICE_YUJIAN:
            webImage = YujianImgService()
        elif imgService == Config.IMG_SERVICE_QCLOUD:
            webImage = QcloudImgService()
        elif imgService == Config.IMG_SERVICE_QINIU:
            webImage = QiniuImgService()
        elif imgService == Config.IMG_SERVICE_BILIBILI:
            webImage = YujianImgService(YujianImgService.API_TYPE_BILIBILI)
        elif imgService == Config.IMG_SERVICE_360:
            webImage = YujianImgService(YujianImgService.API_TYPE_QIHOO)
        elif imgService == Config.IMG_SERVICE_AI58:
            webImage = YujianImgService(YujianImgService.API_TYPE_AI58)
        elif imgService == Config.IMG_SERVICE_SOUGOU:
            webImage = YujianImgService(YujianImgService.API_TYPE_SOUGOU)
        elif imgService == Config.IMG_SERVICE_HULUXIA:
            webImage = YujianImgService(YujianImgService.API_TYPE_HULUXIA)
        elif imgService == Config.IMG_SERVICE_CATBOX:
            webImage = YujianImgService(YujianImgService.API_TYPE_CATBOX)
        elif imgService == Config.IMG_SERVICE_POSTIMAGES:
            webImage = YujianImgService(YujianImgService.API_TYPE_POSTIMAGES)
        elif imgService == Config.IMG_SERVICE_GTIMG:
            webImage = YujianImgService(YujianImgService.API_TYPE_GTIMG)
        elif imgService == Config.IMG_SERVICE_BKIMG:
            webImage = YujianImgService(YujianImgService.API_TYPE_BKIMG)
        elif imgService == Config.IMG_SERVICE_MUKE:
            webImage = YujianImgService(YujianImgService.API_TYPE_MUKE)
        elif imgService == Config.IMG_SERVICE_UPYUN:
            webImage = UpyunImgService()
        else:
            webImage = SmmsImgService()
        return webImage

    @classmethod
    def isValidImgServiceFlag(cls, flag: str) -> bool:
        """是否为合法的图片服务标识
        flag: 图片服务标识
        """
        supportedService = {Config.IMG_SERVICE_SMMS, Config.IMG_SERVICE_ALI, Config.IMG_SERVICE_RRUU,
                            Config.IMG_SERVICE_VIMCN, Config.IMG_SERVICE_YUJIAN, Config.IMG_SERVICE_ALI2,
                            Config.IMG_SERVICE_QCLOUD, Config.IMG_SERVICE_QINIU, Config.IMG_SERVICE_BILIBILI,
                            Config.IMG_SERVICE_SOUGOU, Config.IMG_SERVICE_HULUXIA, Config.IMG_SERVICE_CATBOX,
                            Config.IMG_SERVICE_360, Config.IMG_SERVICE_POSTIMAGES, Config.IMG_SERVICE_AI58,
                            Config.IMG_SERVICE_GTIMG, Config.IMG_SERVICE_BKIMG, Config.IMG_SERVICE_MUKE, Config.IMG_SERVICE_UPYUN}
        if flag in supportedService:
            return True
        return False
