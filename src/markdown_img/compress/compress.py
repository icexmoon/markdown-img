from PIL import Image
from ..config import Config
import os
from ..tools.debug import Debug
from .compress_manager import CompressManager
from ..tools.file_tools import FileTools


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
        imageSize = FileTools.size(self.__imageFile)
        # 没有达到压缩门槛，不压缩
        if imageSize < self.__compressLimit:
            return self.__imageFile
        Debug.print("开始对{}进行压缩,压缩前大小{}kb".format(
            self.__imageFile, int(imageSize)))
        outPutFile = self.__getOutPutFile(self.__imageFile)
        CompressManager.getCompressService().compress(self.__imageFile, outPutFile)
        if os.path.exists(outPutFile):
            compressedSize = FileTools.size(outPutFile)
            Debug.print("{}压缩后的大小{}kb".format(
                self.__imageFile, int(compressedSize)))
            return outPutFile
        else:
            # 没有产生压缩图片，返回原图
            Debug.print("{}压缩失败".format(self.__imageFile))
            return self.__imageFile

    def __exit__(self, expType, expVal, expTrace):
        # 如果存在压缩后的临时文件，删除
        outPutFile = self.__getOutPutFile(self.__imageFile)
        if os.path.exists(outPutFile):
            os.remove(outPutFile)

    def __getOutPutFile(self, infile: str) -> str:
        """获取输出文件路径
        infile: 待处理文件路径
        return: 输出文件路径
        """
        fileName: str = os.path.basename(infile)
        sysConfig = Config.getInstance()
        return sysConfig.getTmpDir()+sysConfig.getPathSplit()+fileName
