from qiniu import Auth, put_file, etag
import os

from .user_exception import UserException


class QiniuClient:
    def upload(self, path: str, domain: str, access_key: str, secret_key: str, bucket_name: str) -> str:
        """上传图片到七牛云
        path: 图片本地路径
        domain: CDN域名
        access_key: AK
        secret_key: SK
        bucket_name: 存储名称
        """
        # 删除末尾可能存在的"/"
        domain = domain.rstrip("/")
        fileName: str = os.path.basename(path)
        # -*- coding: utf-8 -*-
        # flake8: noqa

        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 上传后保存的文件名
        key = fileName

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name, key, 3600)

        # 要上传文件的本地路径
        localfile = path

        ret, info = put_file(token, key, localfile, version='v2')
        # print(info)
        # assert ret['key'] == key
        # assert ret['hash'] == etag(localfile)
        if ret == None:
            raise UserException(UserException.CODE_UPLOAD_ERROR, str(info))
        return "{}/{}".format(domain, fileName)
