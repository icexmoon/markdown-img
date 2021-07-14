from markdown_img.tools.file_tools import FileTools
from .compress_service import CompressService
from PIL import Image
from ..tools.debug import Debug
from ..config import Config


class PillowCompressService(CompressService):
    def _checkOtherConfig(self, info: dict) -> None:
        return super()._checkOtherConfig(info)

    def _inputOtherConfig(self, info: dict) -> None:
        return super()._inputOtherConfig(info)

    def compress(self, reginalImg: str, destImg: str) -> None:
        _, _, ext = reginalImg.rpartition(".")
        if ext == "png":
            self.__compressPng(reginalImg, destImg)
        else:
            self.__compressImage(reginalImg, destImg)

    def __compressPng(self, infile: str, destImg: str) -> None:
        """压缩png图片到输出目录
        infile: 待压缩图片
        """
        im: Image.Image = Image.open(infile)
        newIm = im.quantize(colors=256)
        newIm.save(destImg)

    def __compressImage(self, infile, destImg, step=10, quality=80) -> None:
        """对图片进行多轮压缩以达到压缩门槛(仅限JPG图片)
        infile: 压缩源文件
        step: 每一轮压缩增加的压缩率差值
        quality: 起始压缩率
        """
        info = self.getCompressInfo()
        maxSize = int(info[Config.COMPRESS_INFO_LIMIT])
        o_size = FileTools.size(infile)
        if o_size <= maxSize:
            return
        outfile = destImg
        im = Image.open(infile)
        while o_size > maxSize:
            im.save(outfile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = FileTools.size(outfile)
        return

    def _addCompressEngineInfo(self, lines: list) -> None:
        pass
