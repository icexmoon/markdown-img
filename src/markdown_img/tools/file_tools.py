import os
import time


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
            size = size/1024/1024
        elif unit == cls.SIZE_GB:
            size = size/1024/1024/1024
        return size

    @classmethod
    def getCreateTime(cls, file: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        """返回文件创建时间(字符串形式)
        file: 文件路径
        format: 时间格式
        """
        ctime = os.path.getctime(file)
        return time.strftime(format, time.localtime(ctime))
