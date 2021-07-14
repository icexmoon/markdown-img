from posixpath import basename
from PIL import Image
from ..config import Config
import os
from ..tools.debug import Debug


class Compress:
    def __init__(self, imageFile: str, compressLimit: int = 500) -> None:
        """初始化压缩上下文管理器
        imageFile: 用于压缩的原图片路径
        compressLimit: 压缩门槛（高于该值的图片才会被压缩，单位kb）
        """
        self.__imageFile = imageFile
        self.__compressLimit: int = compressLimit

    def __enter__(self):
        # 对png图片使用quantize压缩
        basename = os.path.basename(self.__imageFile)
        _, _, ext = basename.rpartition(".")
        imageSize = self.__class__.getSize(self.__imageFile)
        # 没有达到压缩门槛，不压缩
        if imageSize < self.__compressLimit:
            return self.__imageFile
        Debug.print("开始对{}进行压缩,压缩前大小{}kb".format(
            self.__imageFile, int(imageSize)))
        if ext == "png":
            self.__compressPng(self.__imageFile)
        else:
            self.__compressImage(self.__imageFile)
        outPutFile = self.__getOutPutFile(self.__imageFile)
        if os.path.exists(outPutFile):
            return outPutFile
        else:
            # 没有产生压缩图片，返回原图
            return self.__imageFile

    def __exit__(self, expType, expVal, expTrace):
        # 如果存在压缩后的临时文件，删除
        outPutFile = self.__getOutPutFile(self.__imageFile)
        if os.path.exists(outPutFile):
            os.remove(outPutFile)

    @classmethod
    def getSize(cls, file):
        # 获取文件大小:KB
        size = os.path.getsize(file)
        return size / 1024

    def __getOutPutFile(self, infile: str) -> str:
        """获取输出文件路径
        infile: 待处理文件路径
        return: 输出文件路径
        """
        fileName: str = os.path.basename(infile)
        sysConfig = Config.getInstance()
        return sysConfig.getTmpDir()+sysConfig.getPathSplit()+fileName

    def __compressPng(self, infile: str) -> None:
        """压缩png图片到输出目录
        infile: 待压缩图片
        """
        im: Image.Image = Image.open(infile)
        new_im = im.quantize(colors=256)
        new_im.save(self.__getOutPutFile(infile))
        pressedSize = self.__class__.getSize(self.__getOutPutFile(infile))
        Debug.print("{}压缩后的大小{}kb".format(infile, int(pressedSize)))

    def __compressImage(self, infile, step=10, quality=80) -> None:
        """对图片进行多轮压缩以达到压缩门槛(仅限JPG图片)
        infile: 压缩源文件
        step: 每一轮压缩增加的压缩率差值
        quality: 起始压缩率
        """
        maxSize = self.__compressLimit
        o_size = self.__class__.getSize(infile)
        if o_size <= maxSize:
            return
        outfile = self.__getOutPutFile(infile)
        im = Image.open(infile)
        while o_size > maxSize:
            im.save(outfile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.__class__.getSize(outfile)
        Debug.print("{}压缩后的大小{}kb".format(infile, int(o_size)))
        return
