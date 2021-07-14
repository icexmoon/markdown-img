
from typing import Sequence
import tinify

from ..user_exception import UserException
from .compress_service import CompressService


class TinypngCompressService(CompressService):
    TINYPNG_KEY = "tinypng_key"

    def _checkOtherConfig(self, info: dict) -> None:
        if self.__class__.TINYPNG_KEY in info:
            key = info[self.__class__.TINYPNG_KEY]
            if isinstance(key, Sequence) and len(key) > 0:
                return
            else:
                raise UserException(
                    UserException.CODE_NO_COMPRESS_SERVICE_CONFIG)
        else:
            raise UserException(
                UserException.CODE_NO_COMPRESS_SERVICE_CONFIG)

    def _inputOtherConfig(self, info: dict) -> None:
        info[self.__class__.TINYPNG_KEY] = input(
            self.globalization.getTextWithColon("tinypng_key_input"))

    def compress(self, reginalImg, destImg) -> None:
        info = self.getCompressInfo()
        tinify.key = info[self.__class__.TINYPNG_KEY]
        source = tinify.from_file(reginalImg)
        source.to_file(destImg)

    def _addCompressEngineInfo(self, lines: list) -> None:
        info = self.getCompressInfo()
        # tinyPNGKey = ""
        # if self.__class__.TINYPNG_KEY in info:
        tinyPNGKey = info[self.__class__.TINYPNG_KEY]
        lines.append(self.globalization.getTextWithParam(
            "tinypng_key", tinyPNGKey))
