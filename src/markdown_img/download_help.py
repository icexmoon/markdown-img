import sys
from urllib import request
import requests
from .user_exception import UserException


class DownloadHelp():
    def processReport(self, a, b, c):
        per = 100.0*a*b/c
        if per > 100:
            per = 1
        # sys.stdout.write(" "+"%.2f%% 已经下载的大小：%1d 文件大小：%1d"%(per,a*b,c)+'\r')
        # sys.stdout.flush()

    def download(self, url, fileName):
        request.urlretrieve(url, filename=fileName,
                            reporthook=self.processReport)

    def chunkDownload(self, url, fileName, timeout=5):
        i = 0
        while True:
            try:
                r = requests.get(url, stream=True, timeout=timeout)
                with open(fileName, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=32):
                        f.write(chunk)
                return
            except requests.exceptions.RequestException:
                #链接超时重试三次
                i += 1
                if i < 3:
                    continue
                else:
                    raise UserException(UserException.CODE_TIMEOUT,"下载"+url+"超时，请重新再试")
