from .compress_service import CompressService
class NoneCompressService(CompressService):
    def _checkOtherConfig(self, info: dict) -> None:
        pass

    def _inputOtherConfig(self, info: dict) -> None:
        pass

    def compress(self, reginalImg: str, destImg: str) -> None:
        pass

    def _addCompressEngineInfo(self, lines: list) -> None:
        pass