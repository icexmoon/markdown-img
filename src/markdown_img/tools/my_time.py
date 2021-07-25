import time


class MyTime:
    @classmethod
    def getCurrentTimeStr(cls, format: str = "%Y-%m-%d %H:%M:%S") -> str:
        return time.strftime(format, time.localtime())
