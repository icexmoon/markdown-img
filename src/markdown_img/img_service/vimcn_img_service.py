import requests
from .img_service import ImgService


class VimcnImgService(ImgService):
    def getConfigInfo(self) -> dict:
        return dict()

    def upload(self, localImg: str) -> str:
        '''上传到Vim-cn'''
        imgOpen = open(localImg, 'rb')
        files = {'file': imgOpen}
        r = requests.post('https://img.vim-cn.com/',
                          data={'name': '@/path/to/image'}, files=files)
        imgOpen.close()
        return r.text

    def inputConfig(self) -> None:
        pass

    def getConfigInfoText(self) -> tuple:
        return (" ",)

    def inputNewConfig(self) -> None:
        pass
