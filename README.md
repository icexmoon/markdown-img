# Markdown-img User's Guide

English | [**简体中文**](https://github.com/icexmoon/markdown-img/main/README_cn.md)

## Project Address

- pypi：<https://pypi.org/project/markdown-img-icexmoon/>
- github：<https://github.com/icexmoon/markdown-img>
- Personal Blog：<https://blog.icexmoon.xyz/?p=99>

## Usage

This program is used to scan the markdown files in the working directory, find the local images in them and upload them to the `sm.ms` image bed automatically, and generate a copy of the markdown using the network images to replace the local images, which is stored in the `current_working_directory/markdown_image` directory.

By the above way, we can realize the automatic batch markdown image processing work to facilitate the later dissemination of markdown contents on the web.

## Notes for details

- This program will not change the original markdown file, please feel free to use it.

- This program relies on `sm.ms` image bed, please register your account and generate token by yourself.

  > Support for other image beds has been added, see features for details, but the default is still using sm.ms image bed.

- Because the `sm.ms` image bed interface has a call limit, if there is a picture upload error, it may be caused by frequent uploads, please wait for more than 1 minute and reuse this program.

- Tencent Cloud Object Storage has been added as a image bed, when using it, you need to enter the corresponding mandatory parameters for connection, you can read the [**Tencent Cloud OSS User Guide**](https://blog.icexmoon.xyz/?p=151) for specific parameters, in addition, you need to set the object storage service to private write public read.

- Currently this program only supports windows.

  > Theoretically supports all platforms that can run Python, but has not been tested on other platforms at this time.

- `sm.ms` access is not considered friendly in China, generated markdown copy immediately published on the network may show anti-theft chain and other images hanging, that is because the domestic CDN is relatively slow, wait for a period of time on the good.

- This program is written in Python, you need to install the Python runtime environment, if you don't know how to install, you can read the [**python environment installation under windows**](https://blog.icexmoon.xyz/?p=101).

## Install

```shell
pip install markdown-img-icexmoon
```

## Update

```shell
pip install --upgrade markdown-img-icexmoon
```

## Function

> Added console short command support, all functions can be called quickly via `pymdimg`.
>
> For example, `pymdimg -h` is exactly the same as `python -m markdown_img -h`.

### View the help file

- Execute `python -m markdown_img -h`。

### View version and configuration information

Excute `pymdimg -v` or `pymdimg --version`.

### Generate a markdown copy of the image bed

The main function of this program, will scan the markdown file in the command line working directory, will replace the local image in it with a bed image and then generate a copy of the bed, the generated copy will be stored in the `markdown_img` folder in the working directory.

1. Use CMD to locate the directory where the markdown file will be processed.
2. Execute `python -m markdown_img`.
3. The first time you run the program you will be prompted to enter the markdown token.
4. Enter it and execute step 2 again.
5. Wait for processing.
6. When you are done, check the `working_directory/markdown_img` directory.

> - The token is stored in the `main.config` file in the directory where the program is located. You can modify it yourself if you need to, or you can delete the configuration file and run the program again to enter it.
> - The command parameters of the program will be enriched and refined later.
> - If the URL returned by the target image bed contains special characters such as Chinese or spaces, and your markdown text editor cannot preview the corresponding image properly, you may need to use URL ENCODE to process it, turn on this function by `pymdimg -u standard`, and regenerate the copy after turning on. This feature currently only works with Tencent OSS, because other image beds will not return Chinese URLs.

### Restore local gallery from the image bed

If the copy of the image bed is intact, but the local images associated with the native markdown file are missing, you can use this function to try to recover them.

1. Switch the command line working directory to the directory of the markdown file you want to restore.
2. Excute`python -m markdown_img -m img_recove`
3. Wait for processing.
4. Check if the local markdown file image is restored after it is finished.

> - Because the network image bed is unstable, although the program itself has a timeout reconnection mechanism, if too many images are recovered, it is likely that the processing will be interrupted and the program will simply need to be rerun.
> - The recovery logic is to compare the order of appearance of the images in the copy and the original, and recover them 1 to 1. So it is important to ensure that there is no difference between the two, and the program will interrupt when the number of both is different and prompt the user to confirm manually.

### Switching the image bed service

You can switch the image bed service in case a certain image bed is not available or the access is unstable.

Currently supported image beds are [**sm.ms**](https://sm.ms/), Ali, [**RuYu**](https://img.rruu.net/), [**Vim-CN**](https://img.vim-cn.com/), [**meet**](https://www.hualigs.cn/), [**Tencent cloud object storage**](https://curl.qcloud.com/empEScHz) (promotional link).

- Excute`python -m markdown_img -i ali`

> - You can check the help documentation for the specific image bed logo.
> - Access tokens are required to switch the bed service and will be prompted to enter the appropriate access token in use.
> - Some necessary information is required to use Tencent Cloud OSS, please read the notes for details.

### Update the image bed access token

If a wrong access token is set for the image bed token, or if a new access token is regenerated on the image bed website, you can update the corresponding access token in the program.

- Excute `python -m markdown_img -c smms`

> - You can check the help documentation for specific parameters.
>
> - Part of the image bed configuration if more than one, you can use subcommands to modify only a single configuration, for example, only modify the Tencent cloud storage directory: `pymdimg -c qcloud --des_dir image`, if there are spaces in the middle of the target directory, you need to give will be wrapped in English double quotes, such as this: `pymdimg -c qcloud --des_dir "我 love 你"`. After updating the configuration you can use `pymdimg -v` to confirm that the configuration has been set correctly.

### Scan images and create indexes

If you need to upload all the images in a directory to a webbed and create a markdown file as an index file, then this is the right function to use.

```shell
python -m markdown_img -s
```

> - The index file will be regenerated each time it is run.
> - The name of the generated index file is `markdown_img_index.md`, please make sure not to customize the file with the same name in the target directory.

### Refreshing a copy of the image bed

If your original md file has been updated and you don't want to delete the corresponding copy file manually and want to regenerate it automatically, you can use this function.

```shell
python -m markdown_img -m refresh
```

> Scans the current directory for the original md file, and if there is no copy, creates it directly. If there is a copy, but the original file is "newer" than the copy, the copy is recreated.

## Update Log

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