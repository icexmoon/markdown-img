from ..config import Config


class Debug:
    @classmethod
    def print(cls, *args: tuple) -> None:
        """如果是debug模式,输出过程信息到屏幕"""
        sysConfig = Config.getInstance()
        # print(args)
        if sysConfig.getConfigParam(Config.PARAM_DEBUG) == Config.DEBUG_ON:
            print(*args)
