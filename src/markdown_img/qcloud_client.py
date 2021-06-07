from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import os
import qcloud_cos
import urllib.parse
from .config import Config


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
        with open(path, 'rb') as fp:
            try:
                response = self.client.put_object(
                    Bucket=self.bucket,
                    Body=fp,
                    Key="{}/{}".format(desPath, fileName),
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
            except qcloud_cos.cos_exception.CosServiceError as e:
                raise e
        if urlEncodeMod == Config.URL_ENCODE_MODE_STANDARD:
            desPath = urllib.parse.quote(desPath)
            fileName = urllib.parse.quote(fileName)
        elif urlEncodeMod == Config.URL_ENCODE_MODE_ONLY_SPACE:
            desPath = desPath.replace(' ','%20')
            fileName = fileName.replace(' ','%20')
        else:
            pass
        url = "https://{}.cos.{}.myqcloud.com/{}/{}".format(
                self.bucket, self.region, desPath, fileName)
        return url
