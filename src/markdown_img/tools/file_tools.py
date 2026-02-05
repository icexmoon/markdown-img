import os
import time
from ..config import Config


class FileTools:
    SIZE_KB = "KB"
    SIZE_MB = "MB"
    SIZE_GB = "GB"

    @classmethod
    def size(cls, file, unit="KB") -> float:
        """返回文件的大小
        file: 文件路径
        unit: 容量单位，默认kb
        """
        size = os.path.getsize(file)
        if unit == cls.SIZE_KB:
            size = size / 1024
        elif unit == cls.SIZE_MB:
            size = size / 1024 / 1024
        elif unit == cls.SIZE_GB:
            size = size / 1024 / 1024 / 1024
        return size

    @classmethod
    def getCreateTime(cls, file: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """返回文件创建时间(字符串形式)
        file: 文件路径
        format: 时间格式
        """
        ctime = os.path.getctime(file)
        return time.strftime(format, time.localtime(ctime))

    @classmethod
    def getFileName(cls, path: str) -> str:
        """返回路径中的文件名
        path: 绝对路径或相对路径
        """
        if path is None:
            return None
        config = Config()
        parts = path.split(config.getPathSplit())
        return parts[-1]

    @classmethod
    def getWindowsTerminalPathLink(cls, name: str, path: str) -> str:
        """返回Windows终端的快捷方式路径
        name: 路径名称
        path: 路径
        """
        return "\033]8;;{}\033\\{}\033]8;;\033\\".format(path, name)
    
    @classmethod
    def getAbsolutePath(cls, path: str) -> str:
        """返回绝对路径
        path: 相对路径
        """
        return os.path.abspath(path)
