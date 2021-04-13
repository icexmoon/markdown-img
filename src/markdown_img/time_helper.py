import os
class TimeHelper():
    @classmethod
    def getFileLastModifyTimeStamp(cls, file: str) -> float:
        '''获取文件的最后修改时间'''
        fileStat = os.stat(file)
        return fileStat.st_mtime

    @classmethod
    def compareTwoFilsLastModifyTime(cls, file1: str, file2: str) -> int:
        '''比较两个文件的最后修改时间，如果file1>file2 返回1，如果file1 = file2 返回0， 否则返回-1'''
        mTime1 = cls.getFileLastModifyTimeStamp(file1)
        mTime2 = cls.getFileLastModifyTimeStamp(file2)
        if mTime1 > mTime2:
            return 1
        elif mTime1 == mTime2:
            return 0
        else:
            return -1
