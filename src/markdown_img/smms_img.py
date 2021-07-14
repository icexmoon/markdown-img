from .config import Config
from .user_exception import UserException
from concurrent import futures
from .img_service_manager import ImgServiceManager
from .compress.compress import Compress


class SmmsImg():
    def __init__(self):
        self.sysConfig = Config.getInstance()

    def multiUploadImage(self, images: list, results: dict):
        '''批量上传图片'''
        MAX_SAME_TIME_DEAL = 10
        if len(images) <= MAX_SAME_TIME_DEAL:
            maxThreadWorks = min(len(images), MAX_SAME_TIME_DEAL)
            # fixed 如果有没有图片的md文件，直接不做处理。
            if maxThreadWorks > 0:
                with futures.ThreadPoolExecutor(max_workers=maxThreadWorks) as futuresExecutor:
                    futureMap = {}
                    for localImg in images:
                        future = futuresExecutor.submit(
                            self.uploadOne, localImg)
                        futureMap[future] = localImg
                    futureDone = futures.as_completed(futureMap)
                    for future in futureDone:
                        try:
                            webImage = future.result()
                        except UserException as e:
                            raise e
                        if webImage == False:
                            raise UserException(
                                UserException.CODE_UPLOAD_ERROR, "文件上传出错")
                        else:
                            results[futureMap[future]] = webImage
        else:
            self.multiUploadImage(images[0:MAX_SAME_TIME_DEAL], results)
            self.multiUploadImage(
                images[MAX_SAME_TIME_DEAL:len(images)], results)

    def uploadOne(self, localImg):
        # 如果设置了压缩选项，进行压缩
        info = self.sysConfig.getCompressInfo()
        if(info[Config.COMPRESS_INFO_STATUS] == "on"):
            compressLimit = int(info[Config.COMPRESS_INFO_LIMIT])
            with Compress(localImg, compressLimit) as compressedImg:
                imgService = ImgServiceManager.getImgService()
                return imgService.upload(compressedImg)
        else:
            imgService = ImgServiceManager.getImgService()
            return imgService.upload(localImg)
