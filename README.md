# Markdown-img使用指南

## 项目地址

- pypi：<https://pypi.org/project/markdown-img-icexmoon/>
- github：<https://github.com/icexmoon/markdown-img>
- 个人博客：<https://blog.icexmoon.xyz/?p=99>

## 用途

本程序用于扫描工作目录下的markdown文件，查找其中的本地图片并自动上传到`sm.ms`图床，并生成一个使用网络图片替换本地图片的markdown副本，存放于`当前工作目录/markdown_image`目录下。

通过以上方式实现自动批量markdown图片处理工作，以方便之后把markdown内容在网络传播。

## 注意事项

- 本程序不会改变原始markdown文件，请放心使用。

- <del>对于已经生成副本的原始文件，本程序不会再次处理，如果需要重新生成副本，请手动删除相应的已生成副本。</del>此功能已添加，具体请查看功能：刷新图床副本。

- 本程序依赖于`sm.ms`图床，请自行注册账号并生成token。

  > 已加入其它图床支持，详情见功能，不过默认依然使用sm.ms图床。

- 因为`sm.ms`图床接口有调用限制，如果出现图片上传出错的情况，可能是上传频繁导致，请等待1分钟以上时间后重新使用本程序。

- 目前本程序只支持windows。

  > 理论上支持所有能运行Python的平台，但目前并没有在其它平台测试过。

- `sm.ms`国内访问不算友好，生成的markdown拷贝立即在网络上发布可能会显示防盗链等图片挂掉的情况，那是因为国内CDN比较慢，等一段时间就好了。

- 本程序使用Python编写，需要安装Python运行环境，如果不知道如何安装，可以阅读[**windows下的python环境安装**](https://blog.icexmoon.xyz/?p=101)。

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

1. 执行`python -m markdown_img -h`。

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

目前支持的图床有[**sm.ms**](https://sm.ms/)、阿里、[**如优**](https://img.rruu.net/)、[**Vim-CN**](https://img.vim-cn.com/)、[**遇见**](https://www.hualigs.cn/)。

1. 执行`python -m markdown_img -i ali`

> - 具体的图床标识可以查看帮助文档。
> - 需要访问令牌的图床服务切换后使用中会提示输入相应的访问令牌。

### 更新图床访问令牌

如果图床令牌设置错误，或者在图床官网重新生成了新的访问令牌，可以在程序中更新相应的访问令牌。

1. 执行`python -m markdown_img -c smms`

> 具体参数可以查看帮助文档。

### 扫描图片并创建索引

如果你需要将某个目录下的图片全部上传到网络图床，并创建一个markdown文件作为索引文件，那使用这个功能就没错了。

```shell
python -m markdown_img -s
```

> - 每次运行都会重新生成索引文件。
> - 生成的索引文件名为`markdown_img_index.md`，请确保不要自定义同名文件在目标目录下。

### 刷新图床副本

如果你的原始md文件已更新，不想手动删除相应的副本文件，想自动重新生成，可以使用此功能。

```shell
python -m markdown_img -m refresh
```

> 会扫描当前目录下的原始md文件，如果没有副本，直接创建。如果有副本，但是原始文件比副本"新"，则重新创建副本。

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