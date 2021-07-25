import os
import shutil
from .tools.debug import Debug
from .tools.my_time import MyTime
from random import randint
from .tools.file_tools import FileTools


class ConfigBackup:
    """配置备份相关"""
    @classmethod
    def backupConfig(cls, sysConfig: "Config", fileName: str = None, override: bool = False):
        """对当前系统配置进行备份, 会覆盖同名备份
        sysConfig: 系统配置
        fileName: 文件名，如果为None则自动依据当前时间生成文件名
        override: 如果存在同名配置，是否覆盖，默认为否
        return: 如果成功备份，返回文件地址，否则返回false
        """
        mainConfigPath = sysConfig.getConfigFile()
        if not os.path.exists(mainConfigPath):
            Debug.print("著配置文件{}不存在".format(mainConfigPath))
            return False
        if fileName is None:
            fileName = "{}{:0>3d}".format(
                MyTime.getCurrentTimeStr("%Y%m%d%H%M%S"), randint(1, 999))
        # 复制
        desConfigBackupFile = cls.getConfigBackupFile(sysConfig, fileName)
        if (override is False) and os.path.exists(desConfigBackupFile):
            Debug.print("存在同名配置{}".format(desConfigBackupFile))
            return False
        shutil.copyfile(mainConfigPath, desConfigBackupFile)
        return desConfigBackupFile

    @classmethod
    def getConfigBackupFile(cls, sysConfig: "Config", fileName: str) -> str:
        """获取配置备份文件路径
        sysConfig: 系统配置
        fileName: 配置备份名称
        return: 配置备份文件路径
        """
        backupDir: str = cls.getConifgBackupDir(sysConfig)
        return "{}{}{}.config".format(backupDir, sysConfig.getPathSplit(), fileName)

    @classmethod
    def getConifgBackupDir(cls, sysConfig: "Config") -> str:
        """获取配置备份目录路径
        sysConfig: 系统配置
        return: 配置备份目录路径
        """
        sysHome = sysConfig.getCurrentDirPath()
        dirPath: str = "{}{}config_backup".format(
            sysHome, sysConfig.getPathSplit())
        if not os.path.exists(dirPath):
            os.mkdir(dirPath)
        return dirPath

    @classmethod
    def getConfigBackup(cls, sysConfig: "Config") -> list[tuple]:
        """获取配置备份的信息
        sysConfig: 系统配置
        return: 配置备份列表
        """
        files = []
        backupDir: str = cls.getConifgBackupDir(sysConfig)
        for path in os.listdir(backupDir):
            absPath = "{}{}{}".format(
                backupDir, sysConfig.getPathSplit(), path)
            if os.path.isfile(absPath) and path.endswith(".config"):
                fileName, _, _ = path.rpartition('.')
                ctime = FileTools.getCreateTime(absPath)
                info = (fileName, ctime, absPath)
                files.append(info)
        return files
