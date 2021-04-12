# 几种公共图床Python调用

RT，因为发博客的需求，关注了一些免费图床。

之前一直用的sm.ms+CSDN，基本没啥问题，最近sm.ms的访问速度还有所加快？

> 对这个方案感兴趣的可以阅读[**教大家如何白嫖CSDN图床**](https://blog.icexmoon.xyz/?p=79)。

但是毕竟是白嫖，也不知道啥时候会出问题，这时候正好看到异次元的一篇文章[**16 个免费图床网站全收集 - 稳定国内可用支持外链图片服务推荐 (含测速对比)**](https://www.iplaysoft.com/free-image-hosting.html)。

今天花了一点时间挑了里边的几个图床进行了Python调用测试，算是多条路子。

直接上代码：

```python
import requests
import json
import time
import random
imgPath = 'test.png'


def uploadToVimCn(imgPath):
    '''上传到Vim-cn'''
    imgOpen = open(imgPath, 'rb')
    files = {'file': imgOpen}
    r = requests.post('https://img.vim-cn.com/',
                      data={'name': '@/path/to/image'}, files=files)
    imgOpen.close()
    return r.text


def uploadToRruu(imgPath):
    '''上传到如优图床和阿里图床'''
    imgOpen = open(imgPath, 'rb')
    files = {'image': imgOpen}
    apiType = 'ali'
    token = '<token>'
    r = requests.post('https://img.rruu.net/api/upload',
                      data={'apiType': apiType, 'privateStorage': '', 'token': token}, files=files)
    imgOpen.close()
    respJson = r.json()
    urls = {}
    if str(respJson['code']).strip() == '200' and str(respJson['msg']).strip() == 'success':
        urls['rruu'] = respJson['data']['url']['distribute']
        urls['ali'] = respJson['data']['url']['ali']
    return urls


# print(uploadToVimCn(imgPath))
print(uploadToRruu(imgPath))
```

目前只测试了[**Vim-CN**](https://img.vim-cn.com/)和[**如优图床**](https://img.rruu.net/)，不过如优图床本身是支持多种图床调用的。

![image-20210411165903626](https://img.rruu.net/image/607305172df44)

不过测试的时候发现并不是那么美好，比如bilibili就需要登录，否则会调用失败。

不过如优图床本身和阿里的存储都没啥问题。

需要说明的是使用如优图床API需要注册，使用注册后的token就可以调用，每个账户的图床容量是10G，不清楚容量满了影响不影响通过如优API调用其它图床。

![image-20210411170555232](https://img.rruu.net/image/6073052013eaa)

不过如优的注册很宽泛，只要邮箱，也就是说容量满了你可以再注册一个账号。

好了，以上。

有时间了我会更新Python编写的markdown图片处理程序，加入测试的这两种图床调用。

如果有其它好用的公共图床可以API调用的，欢迎补充~。