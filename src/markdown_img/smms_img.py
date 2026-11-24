from .config import Config
from .user_exception import UserException
from concurrent import futures
from requests.exceptions import RequestException
from .img_service_manager import ImgServiceManager
from .compress.compress import Compress
from .globalization import Globalization


class SmmsImg():
    def __init__(self):
        self.sysConfig = Config.getInstance()

    def multiUploadImage(self, images: list, results: dict):
        '''批量上传图片'''
        MAX_SAME_TIME_DEAL = 10
        failures = {}
        succeeded = []
        language = Globalization()
        for start in range(0, len(images), MAX_SAME_TIME_DEAL):
            batch = images[start:start + MAX_SAME_TIME_DEAL]
            with futures.ThreadPoolExecutor(max_workers=len(batch)) as executor:
                futureMap = {executor.submit(self.uploadOne, image): image for image in batch}
                for future in futures.as_completed(futureMap):
                    image = futureMap[future]
                    try:
                        webImage = future.result()
                    except UserException as e:
                        if e.getErrorCode() not in (UserException.CODE_UPLOAD_ERROR, UserException.CODE_TIMEOUT):
                            raise
                        failures[image] = e.getErrorMsg() or language.getText("upload_no_detail")
                        continue
                    except (OSError, RequestException) as e:
                        failures[image] = language.getText("upload_io_error").format(str(e))
                        continue
                    if not webImage:
                        failures[image] = language.getText("upload_no_url")
                    else:
                        results[image] = webImage.replace(" ", "%20")
                        succeeded.append(image)
        config = Config.getInstance()
        text = language.getText("upload_summary").format(len(succeeded), len(failures))
        if config.getConfigParam(Config.PARAM_IMG_SERVICE) == Config.IMG_SERVICE_QCLOUD:
            info = config.getConfigParam(Config.PARAM_QCLOUD_INFO)
            if (isinstance(info, dict) and Config.QCLOUD_INFO_BUCKET in info
                    and Config.QCLOUD_INFO_DES_DIR in info):
                directory = info[Config.QCLOUD_INFO_DES_DIR] or language.getText("upload_root_directory")
                destination = language.getText("qcloud_upload_destination").format(
                    info[Config.QCLOUD_INFO_BUCKET], directory
                )
            else:
                destination = language.getText("qcloud_destination_unavailable")
            text = destination + "\n" + text
        for image in sorted(succeeded):
            text += "\n" + language.getText("upload_image_success").format(image)
        for image in sorted(failures):
            text += "\n" + language.getText("upload_image_failure").format(image, failures[image])
        if not images:
            text += "\n" + language.getText("upload_no_images")
        if failures:
            try:
                config.writeErrorLog(text)
            except OSError as e:
                text += "\n" + language.getText("upload_log_error").format(str(e))
            raise UserException(UserException.CODE_UPLOAD_ERROR, text)
        print(text)

    def uploadOne(self, localImg):
        # 如果是 gif 而非静态图片，不压缩
        if (localImg.endswith(".gif")):
            imgService = ImgServiceManager.getImgService()
            return imgService.upload(localImg)
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
