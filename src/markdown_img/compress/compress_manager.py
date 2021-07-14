from .pillow_compress_service import PillowCompressService
from .tinypng_compress_service import TinypngCompressService
from .none_compress_service import NoneCompressService
from .compress_service import CompressService
from ..config import Config


class CompressManager:
    @classmethod
    def getCompressService(cls) -> CompressService:
        sysConfig = Config.getInstance()
        info = sysConfig.getCompressInfo()
        serviceFlag = sysConfig.getConfigParam(Config.PARAM_COMPRESS_ENGINE)
        compressService: CompressService
        if serviceFlag == Config.COMPRESS_ENGINE_GIL:
            compressService = PillowCompressService()
        elif serviceFlag == Config.COMPRESS_ENGINE_TIYPNG:
            compressService = TinypngCompressService()
        else:
            compressService = NoneCompressService()
        return compressService
