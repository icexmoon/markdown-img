class UserException (Exception):
    # 缺少配置文件
    CODE_NO_CONFIG = 1
    CODE_UPLOAD_ERROR = 2
    CODE_TIMEOUT = 3
    CODE_NO_SMMS_TOKEN = 4
    CODE_NO_RRUU_TOKEN = 5
    CODE_NO_YUJIAN_TOKEN = 6
    CODE_NO_QCLOUD_INFO = 7
    CODE_ERROR_INPUT = 8
    CODE_NO_QINIU_INFO = 9
    CODE_NO_IMG_SERVICE_CONFIG = 10
    CODE_NO_COMPRESS_SERVICE_CONFIG = 11
    CODE_OTHER = 12
    def __init__(self, errorCode: int, errorMsg: str = ""):
        self.errorCode = errorCode
        self.errorMsg = errorMsg

    def getErrorCode(self):
        return self.errorCode

    def getErrorMsg(self):
        return self.errorMsg
