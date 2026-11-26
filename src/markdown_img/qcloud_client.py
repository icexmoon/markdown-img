from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosException, CosServiceError
import sys
import logging
import os
import urllib.parse
from requests.structures import CaseInsensitiveDict
from .config import Config
from .globalization import Globalization


class QcloudClient():
    def __init__(self, secretId, secretKey, region, bucket) -> None:
        # -*- coding=utf-8
        # appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
        # 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
        logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
        secret_id = secretId      # 替换为用户的 secretId
        secret_key = secretKey     # 替换为用户的 secretKey
        self.region = region     # 替换为用户的 Region
        token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=self.region, SecretId=secret_id,
                           SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        self.client = CosS3Client(config)
        # 参照下文的描述。或者参照 Demo 程序，详见 https://github.com/tencentyun/cos-python-sdk-v5/blob/master/qcloud_cos/demo.py
        self.bucket = bucket

    def upload(self, path: str, desPath: str, urlEncodeMod: str = Config.URL_ENCODE_MODE_NONE):
        # 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
        # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
        fileName = os.path.basename(path)
        key = "{}/{}".format(desPath, fileName) if desPath else fileName
        with open(path, 'rb') as fp:
            size = os.fstat(fp.fileno()).st_size
            try:
                response = CaseInsensitiveDict(self.client.put_object(
                    Bucket=self.bucket,
                    Body=fp,
                    Key=key,
                    StorageClass='STANDARD',
                    EnableMD5=True
                ))
            except CosException as e:
                raise RuntimeError(self._errorText("qcloud_put_failed", e)) from e
        try:
            metadata = CaseInsensitiveDict(self.client.head_object(
                Bucket=self.bucket, Key=key
            ))
        except CosException as e:
            raise RuntimeError(self._errorText("qcloud_head_failed", e)) from e
        etag = response.get("ETag")
        if not etag or metadata.get("ETag") != etag:
            raise RuntimeError(Globalization().getText("qcloud_etag_mismatch"))
        if metadata.get("Content-Length") != str(size):
            raise RuntimeError(Globalization().getText("qcloud_size_mismatch"))
        if urlEncodeMod == Config.URL_ENCODE_MODE_STANDARD:
            encodedKey = urllib.parse.quote(key, safe="/")
        else:
            encodedKey = "".join(
                urllib.parse.quote(char, safe="/") if char.isascii() else char
                for char in key
            )
        url = "https://{}.cos.{}.myqcloud.com/{}".format(
                self.bucket, self.region, encodedKey)
        return url

    @staticmethod
    def _errorText(message: str, error: CosException) -> str:
        language = Globalization()
        detail = str(error)
        if isinstance(error, CosServiceError):
            status = error.get_status_code()
            detail = "HTTP {}: {}".format(status, detail)
            if status == 400:
                hint = "qcloud_hint_bad_request"
            elif status in (401, 403):
                hint = "qcloud_hint_permission"
            elif status == 404:
                hint = "qcloud_hint_not_found"
            elif status in (408, 429) or 500 <= status < 600:
                hint = "qcloud_hint_temporary"
            else:
                hint = "qcloud_hint_other"
        else:
            hint = "qcloud_hint_client"
        return "{} {}".format(
            language.getText(message).format(detail), language.getText(hint)
        )
