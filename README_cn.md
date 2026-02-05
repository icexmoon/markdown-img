# Markdown-img使用指南

[**English**](https://github.com/icexmoon/markdown-img) | 简体中文

## 目录

- [**项目地址**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E9%A1%B9%E7%9B%AE%E5%9C%B0%E5%9D%80)
- [**用途**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E7%94%A8%E9%80%94)
- [**注意事项**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%B3%A8%E6%84%8F%E4%BA%8B%E9%A1%B9)
- [**支持的图床服务**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%94%AF%E6%8C%81%E7%9A%84%E5%9B%BE%E5%BA%8A%E6%9C%8D%E5%8A%A1)
- [**安装**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%AE%89%E8%A3%85)
- [**更新**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9B%B4%E6%96%B0)
- [**功能**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%8A%9F%E8%83%BD)
  - [**查看帮助文档**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9F%A5%E7%9C%8B%E5%B8%AE%E5%8A%A9%E6%96%87%E6%A1%A3)
  - [**查看版本及配置信息**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9F%A5%E7%9C%8B%E7%89%88%E6%9C%AC%E5%8F%8A%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)
  - [**选择工作语言**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E9%80%89%E6%8B%A9%E5%B7%A5%E4%BD%9C%E8%AF%AD%E8%A8%80)
  - [**生成图床markdown副本**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E7%94%9F%E6%88%90%E5%9B%BE%E5%BA%8Amarkdown%E5%89%AF%E6%9C%AC)
  - [**从图床恢复本地图库**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E4%BB%8E%E5%9B%BE%E5%BA%8A%E6%81%A2%E5%A4%8D%E6%9C%AC%E5%9C%B0%E5%9B%BE%E5%BA%93)
  - [**切换图库服务**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%88%87%E6%8D%A2%E5%9B%BE%E5%BA%8A%E6%9C%8D%E5%8A%A1)
  - [**更新图床访问令牌**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9B%B4%E6%96%B0%E5%9B%BE%E5%BA%8A%E8%AE%BF%E9%97%AE%E4%BB%A4%E7%89%8C)
  - [**扫描图片并创建索引**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%89%AB%E6%8F%8F%E5%9B%BE%E7%89%87%E5%B9%B6%E5%88%9B%E5%BB%BA%E7%B4%A2%E5%BC%95)
  - [**刷新图床副本**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%88%B7%E6%96%B0%E5%9B%BE%E5%BA%8A%E5%89%AF%E6%9C%AC)
  - [**备份系统配置**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%A4%87%E4%BB%BD%E7%B3%BB%E7%BB%9F%E9%85%8D%E7%BD%AE)
  - [**列出已保存的配置**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E5%88%97%E5%87%BA%E5%B7%B2%E4%BF%9D%E5%AD%98%E7%9A%84%E9%85%8D%E7%BD%AE)
  - [**替换配置**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9B%BF%E6%8D%A2%E9%85%8D%E7%BD%AE)
  - [**项对路径图片**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E7%9B%B8%E5%AF%B9%E8%B7%AF%E5%BE%84%E5%9B%BE%E7%89%87)
- [**致谢**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E8%87%B4%E8%B0%A2)
- [**更新日志**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97)

## 项目地址

- pypi：<https://pypi.org/project/markdown-img-icexmoon/>
- github：<https://github.com/icexmoon/markdown-img>
- 个人博客：<https://blog.icexmoon.xyz/?p=99>

## 用途

本程序用于扫描工作目录下的markdown文件，查找其中的本地图片并自动上传到<del>`sm.ms`</del>图床，并生成一个使用网络图片替换本地图片的markdown副本，存放于`当前工作目录/markdown_image`目录下。

通过以上方式实现自动批量markdown图片处理工作，以方便之后把markdown内容在网络传播。

## 注意事项

- 本程序不会改变原始markdown文件，请放心使用。

- <del>对于已经生成副本的原始文件，本程序不会再次处理，如果需要重新生成副本，请手动删除相应的已生成副本。</del>此功能已添加，具体请查看功能：刷新图床副本。

- 本程序依赖于`sm.ms`图床，请自行注册账号并生成token。

  > 已加入其它图床支持，详情见功能，不过默认依然使用sm.ms图床。

- 因为`sm.ms`图床接口有调用限制，如果出现图片上传出错的情况，可能是上传频繁导致，请等待1分钟以上时间后重新使用本程序。

- 已添加腾讯云对象存储作为图床，使用时需要输入相应的必须参数用于连接，具体参数获取可以阅读[**腾讯云OSS使用指南**](https://blog.icexmoon.xyz/?p=151)，此外还需要将对象存储服务设置为私有写公有读。

- <del>目前本程序只支持windows。</del>

  > 已在Linux平台验证，基本功能都可以正常使用。

- `sm.ms`国内访问不算友好，生成的markdown拷贝立即在网络上发布可能会显示防盗链等图片挂掉的情况，那是因为国内CDN比较慢，等一段时间就好了。

- 本程序使用Python编写，需要安装Python运行环境，如果不知道如何安装，可以阅读[**windows下的python环境安装**](https://blog.icexmoon.xyz/?p=101)。

## 支持的图床服务

| 图床名称                                          | 标识       | 图床性质 | 需要访问令牌 | 备注                                                         |
| ------------------------------------------------- | ---------- | -------- | ------------ | ------------------------------------------------------------ |
| [**sm.ms**](https://sm.ms/)                       | smms       | 公共     | 是           | 默认图床，国外的老牌公共图床服务商，值得信赖，缺点为国内访问不稳定。 |
| [**遇见**](https://www.hualigs.cn/)               | yujian     | 公共     | 是           | 国内的一家图床服务，除了自身提供图床服务，还支持通过其API调用其他图床服务。 |
| [**如优**](https://img.rruu.net/)                 | rruu       | 公共     | 是           | 可以看出和遇见用的是同一套网站代码，目前网站已关闭，服务不可用。 |
| 阿里图床                                          | ali        | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| [**Vim-CN**](https://img.vim-cn.com/)             | vimcn      | 公共     | 否           | 国外的一家图床服务商，据说同样是老牌服务商，缺点同样是国内访问不稳定。 |
| [**腾讯云COS**](https://curl.qcloud.com/empEScHz) | qcloud     | 私有     | 是           | 没啥好说的，几家私有云存储里最推荐的，缺点是目前只提供一年的免费额度，到期需要续费。 |
| [**七牛云**](https://www.qiniu.com/)              | qiniu      | 私有     | 是           | 提供永久的免费存储额度，缺点是不给存储的外链提供域名，需要自己拥有一个域名并进行绑定操作后才可以使用。 |
| bilibili                                          | bilibili   | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 搜狗                                              | sougou     | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 葫芦侠                                            | huluxia    | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 猫盒                                              | catbox     | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 360                                               | 360        | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 贴图                                              | postimages | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 58                                                | ai58       | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 极图                                              | gtimg      | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 佰图                                              | bkimg      | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| 慕课                                              | muke       | 公共     | 是           | 非正常服务，用遇见图床的API实现支持，谨慎使用。              |
| [**又拍云**](https://www.upyun.com/)              | upyun      | 私有     | 是           | 提供代金券，缺点是不给存储的外链提供域名，需要自己拥有一个域名并进行绑定操作后才可以使用。此外白嫖代金券需要加入[**又拍云联盟**](https://www.upyun.com/league)，且每年审核一次。 |
|[**风筝图床**](https://www.imgbed.link/index.html)|fz|公共|是|国内的一个公共图床（有备案），注册后提供1G免费空间，可以购买会员以扩容。

## 安装

```shell
pip install markdown-img-icexmoon
```

## 更新

```shell
pip install --upgrade markdown-img-icexmoon
```

## 功能

> 已添加控制台短命令支持，所有功能均可以通过`pymdimg`快速调用。
>
> 比如`pymdimg -h`和`python -m markdown_img -h`功能完全一致。

### 查看帮助文档

- 执行`python -m markdown_img -h`。

### 查看版本及配置信息

执行`pymdimg -v`或`pymdimg --version`。

### 选择工作语言

支持English和中文作为工作语言，默认为中文。

- 执行`pymdimg -l en`切换工作语言。

### 图片压缩

开启此功能后会对超过一定大小的图片进行压缩处理后上传到图床，以节约私人存储空间。压缩后的中间图片会自动从本地删除，并不会影响到本地的原图。

- 执行`pymdimg --compress`设置相关配置后进行开启。

### 切换图片压缩引擎

目前支持GIL和tinyPNG，前者为使用第三方Gillow包实现本地压缩，后者为使用在线服务tinyPNG.com进行在线压缩，推荐后者，因为后者为无损压缩，但后者需要先注册以生成访问令牌，并且免费用户有调用次数：500次/每月。

执行`pymdimg -e tinyPNG`进行切换。

### 生成图床markdown副本

本程序的主要功能，将扫描命令行工作目录下的markdown文件，会将其中的本地图片替换为图床图片后生成一个图床副本，生成的副本会存储在工作目录下的`markdown_img`文件夹中。

1. 使用CMD定位到将要处理的markdown文件目录。
2. 执行`python -m markdown_img`。
3. 第一次运行程序会提示你输入图床token。
4. 输入后再次执行步骤2。
5. 等待处理。
6. 完毕后查看`工作目录/markdown_img`目录。

> - 图床token存储在程序所在目录的`main.config`文件中，如果需要修改的可以自行修改，也可以删除该配置文件后重新运行程序输入。
> - <del>目前仍不支持根据文件新旧程度重新生成markdown副本的功能，如果原文件改变，需要手动删除副本后重新生成。</del>此功能已添加，详情见功能：刷新图床副本。
> - 稍后会丰富并完善程序的相关命令参数。
> - 如果目标图床返回的URL中包含中文或者空格等特殊字符，并且你的markdown文本编辑器无法正常预览相应的图片，则可能需要使用URL ENCODE进行处理，开启此功能的方法为`pymdimg -u standard`，开启后重新生成副本即可。此功能目前仅作用域腾讯云OSS，因为其他图床不会返回中文url。
> - 可以使用指定的配置来生成副本，比如`pymdimg --config normal`，通过此功能可以在特定情景，比如说希望本次任务中不适用压缩，或者使用大比例压缩时，在不修改当前配置的前提下可以使用定制的相关配置完成本次任务。具体制作相关配置的功能见【功能：备份系统配置】。

### 从图床恢复本地图库

如果图床副本完好，但本体markdown文件关联的本地图片丢失的，可以利用此功能尝试恢复。

1. 切换命令行工作目录到要恢复的markdown文件目录。
2. 执行`python -m markdown_img -m img_recove`
3. 等待处理。
4. 完毕后查看本地markdown文件图片是否恢复。

> - 因为网络图床不稳定，虽然程序本身有超时重连机制，但如果恢复的图片过多，很可能处理中断，只需要重新运行程序即可。
> - 恢复逻辑为对比副本和原本中的图片出现顺序，1对1恢复，所以务必保证两者没有差异，程序会在两者数量不同时中断并提示用户手动确认。

### 切换图床服务

可以切换图床服务，以备某个图床不可用或者访问不稳定。

<del>目前支持的图床有[**sm.ms**](https://sm.ms/)、<del>阿里、[**如优**](https://img.rruu.net/)、</del>[**Vim-CN**](https://img.vim-cn.com/)、[**遇见**](https://www.hualigs.cn/)，[**腾讯云对象存储**](https://curl.qcloud.com/empEScHz)（推广链接）、[**七牛云**](https://www.qiniu.com/)、[**又拍云**](https://www.upyun.com/)（计划支持）。</del>

支持的图床列表见[**支持的图床服务**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md#%E6%94%AF%E6%8C%81%E7%9A%84%E5%9B%BE%E5%BA%8A%E6%9C%8D%E5%8A%A1)。

1. 执行`python -m markdown_img -i ali`

> - 具体的图床标识可以查看帮助文档。
> - 需要访问令牌的图床服务切换后使用中会提示输入相应的访问令牌。
> - 使用腾讯云OSS需要一些必要信息，具体请阅读注意事项。
> - 使用七牛云存储的时候需要提供必要信息，其中DNS绑定域名需要包含协议，比如`http://example.domain.com`

### 更新图床访问令牌

如果图床令牌设置错误，或者在图床官网重新生成了新的访问令牌，可以在程序中更新相应的访问令牌。

1. 执行`python -m markdown_img -c smms`

> - 具体参数可以查看帮助文档。
>
> - 部分图床配置如果是多项，可以使用子命令仅修改其中单一配置，比如仅修改腾讯云的存储目录：`pymdimg -c qcloud --des_dir image`，如果目标目录中间有空格，需要给将其用英文双引号包起来，比如这样：`pymdimg -c qcloud --des_dir "我 love 你"`。更新完配置后可以使用`pymdimg -v`确认配置是否已经设置正确。

### 扫描图片并创建索引

如果你需要将某个目录下的图片全部上传到网络图床，并创建一个markdown文件作为索引文件，那使用这个功能就没错了。

```shell
python -m markdown_img -s
```

> - 每次运行都会重新生成索引文件。
> - 生成的索引文件名为`markdown_img_index.md`，请确保不要自定义同名文件在目标目录下。
> - 可以使用指定配置，如`pymdimg -s --config normal`，具体说明见【生成图床markdown副本】的相关条目。

### 刷新图床副本

如果你的原始md文件已更新，不想手动删除相应的副本文件，想自动重新生成，可以使用此功能。

```shell
python -m markdown_img -m refresh
```

> 会扫描当前目录下的原始md文件，如果没有副本，直接创建。如果有副本，但是原始文件比副本"新"，则重新创建副本。

### 备份系统配置

如果有需要，可以对系统配置进行备份：

```shell
pymdimg -m backup_config --name xxx
```

`--name`参数并非必须，如果不指定则会依据当前时间生成一个配置备份的文件名。

### 列出已保存的配置

```shell
pymdimg --list_config
```

会列出配置名称和创建时间

### 替换配置

可以使用已保存的配置替换当前配置：

```shell
pymdimg --change_config xxx
```

其中`xxx`为想替换的已保存配置的文件名，如果要查看有哪些已保存配置，请使用【功能：列出已保存的配置】。此外，使用此功能前最好先保存当前配置。

### 相对路径图片

可以将使用绝对路径图片的md文件统一处理成使用相对路径图片，程序会将原始图片拷贝到当前目录的`images`子目录下作为相对路径图片。

该功能的目的是为某些跨平台、多设备的用户提供方便，使用相对路径后，原始图片和md文件就可以很方便的移动，或者使用类似坚果云的同步服务进行多设备同步。

```shell
pymdimg -m relative_img
```

> - 为避免程序出错导致的原始md文件损坏，会保留一个原始文件备份到`backup`子目录中。
> - 因为Windows和Linux平台分隔符的区别，并不能保证两者的相对目录都表现正常。

## 二次开发

开发工具链已经迁移到 uv，关于 uv 的安装和使用，可以参考[Python 包管理工具 UV](https://blog.icexmoon.cn/archives/805.html)。

可以在项目根目录下通过以下命令执行测试代码：

```
uv run test.py
```

测试目录位于`tests`，需要自行准备测试文件和数据。作为参考，可以参考`tests_example`。



## 致谢

本应用开发者获得了[**又拍云联盟**](https://www.upyun.com/?utm_source=lianmeng&utm_medium=referral)的帮助和支持，获得了其提供的免费CDN加速和云存储服务，如果您也想获取同样的帮助和支持，可以点击[**这里**](https://www.upyun.com/?utm_source=lianmeng&utm_medium=referral)加入。

## 更新日志

### 0.0.6

新增命令行参数功能，具体情况可使用`python -m markdown_img --help`进行查看。

新增使用图床备份恢复本地图片库的功能，具体使用方法见帮助信息。

### 0.1.1

加入阿里图床、Vim-CN图床、如优图床的调用支持。

其中阿里图床和如优图床通过如优的API调用实现，需要在如优图床官网申请账号并获取token。

> 如优图床的容量为单账号10G，不过注册只需要邮箱，可以注册多个账号。

加入从图床副本恢复本地markdown图片的功能，具体使用方式见帮助文档。

### 0.1.2

修复了某些情况下配置文件为空会导致JSON解析异常的bug。

添加了更新图床访问令牌的功能。

### 0.1.3

添加扫描图片并创建网络图床索引的功能。

### 0.1.4

添加刷新图床副本的功能。

### 0.1.6

修复rruu图床接口挂掉导致直接输出异常到控制台的问题。

### 0.1.7

加入短命令支持。

在生成的图片索引中加入换行以区分图片。

加入引用模块检测，安装时如果缺少相应模块会自动安装。

### 0.1.8

加入遇见图床支持。

阿里图床的API调用替换为遇见图床。

### 0.1.9

修复了只能处理png，不能识别并处理其他格式的图片的问题。

### 0.2.0

修复了不能识别html`<img/>`标签的问题，现在对img标签中的图片也可以正常处理了。

### 0.2.1

添加了阿里图床（如优线路）。

### 0.2.2

用futures实现多线程。

### 0.2.3

- 修复了目录下有无图片的md文件会导致异常的问题。
- 添加版本显示功能。

### 0.2.4

添加了腾讯云对象存储作为图床。

### 0.2.5

- 添加了修改腾讯云图床的子命令。
- 修改查看版本命令，增加程序相关配置信息的显示。
- 修改帮助文档。

### 0.2.6

增加使用URL ENCODE处理图片url的功能。

### 0.2.7

修改URL ENCODE功能，增加仅对空格进行处理的模式。

### 0.2.8

添加国际化，增加英语作为工作语言。

### 0.2.9

添加七牛云作为新的可选图床。

### 0.3.0

- 代码重构
- 添加bilibili作为新图床
- 修复部分bug

### 0.3.1

添加又拍云作为新的可选图床。

### 0.3.2

- 添加图片压缩功能
- 添加debug模式

### 0.3.3

添加TinyPNG作为新的压缩引擎

### 0.3.4

压缩引擎切换选项增加 none，可以更方便的关闭压缩功能。

### 0.3.5

增加系统配置备份功能。

### 0.3.6

增加使用指定配置的功能。

### 0.3.7

修复了因为使用Futures模块导致的安装失败的问题。

### 0.3.8

修复了在Linux下不能正常生成处理后的目录的bug。

### 0.3.9

添加了将md文件中的绝对路径图片修改为相对路径的功能。


### 0.4.0

添加对风筝图床的支持。

### 1.0.0

将 md 文件中图片绝对路径修改为相对路径时，使用`/`而非`\`作为分隔符，后者无法用于 Github Readme 文件。

修复 md 文件中包含 gif 图片且启动了图片压缩时，处理 md 文件会出现 bug 的问题。

### 2.0.0

将开发工作链迁移到 uv。

优化 WIndows 下终端显示结果，显示处理前和处理后的文件名，并且可以点击文件名跳转到对应文件。