# Markdown-img User's Guide

English | [**简体中文**](https://github.com/icexmoon/markdown-img/blob/master/README_cn.md)

## Contents

- [**Project Address**](https://github.com/icexmoon/markdown-img#project-address)
- [**Usage**](https://github.com/icexmoon/markdown-img#usage)
- [**Notes for details**](https://github.com/icexmoon/markdown-img#notes-for-details)
- [**Supported image bed services**](https://github.com/icexmoon/markdown-img#supported-image-bed-services)
- [**Install**](https://github.com/icexmoon/markdown-img#install)
- [**Update**](https://github.com/icexmoon/markdown-img#update)
- [**Function**](https://github.com/icexmoon/markdown-img#function)
  - [**View the help file**](https://github.com/icexmoon/markdown-img#view-the-help-file)
  - [**View the version and configuration information**](https://github.com/icexmoon/markdown-img#view-version-and-configuration-information)
  - [**Select working language**](https://github.com/icexmoon/markdown-img#select-working-language)
  - [**Generate a markdown copy of the image bed**](https://github.com/icexmoon/markdown-img#generate-a-markdown-copy-of-the-image-bed)
  - [**Restore local gallery from the image bed**](https://github.com/icexmoon/markdown-img#restore-local-gallery-from-the-image-bed)
  - [**Switching the image bed service**](https://github.com/icexmoon/markdown-img#switching-the-image-bed-service)
  - [**Update the image bed acess token**](https://github.com/icexmoon/markdown-img#update-the-image-bed-access-token)
  - [**Scan images and create indexes**](https://github.com/icexmoon/markdown-img#scan-images-and-create-indexes)
  - [**Refreshing a copy of the image bed**](https://github.com/icexmoon/markdown-img#refreshing-a-copy-of-the-image-bed)
- [**Acknowledgements**](https://github.com/icexmoon/markdown-img#acknowledgements)
- [**Update Log**](https://github.com/icexmoon/markdown-img#update-log)

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

##  Supported image bed services

| Image bed name                                            | Flag       | Bed nature | Access token required | Notes                                                        |
| --------------------------------------------------------- | ---------- | ---------- | --------------------- | ------------------------------------------------------------ |
| [**sm.ms**](https://sm.ms/)                               | smms       | Public     | Yes                   | Default image bed, foreign old public image bed service provider, trustworthy, the disadvantage of domestic access is unstable. |
| [**yujian**](https://www.hualigs.cn/)                     | yujian     | Public     | Yes                   | A domestic image bed service, in addition to providing its own image bed service, also supports calling other image bed services through its API. |
| [**ruyou**](https://img.rruu.net/)                        | rruu       | Public     | Yes                   | As you can see and met with the same set of website code, the site is currently closed, the service is not available. |
| ali                                                       | ali        | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| [**Vim-CN**](https://img.vim-cn.com/)                     | vimcn      | Public     | No                    | A foreign bed service provider, said to be the same old service provider, the same disadvantage of domestic access is unstable. |
| [**Tencent Cloud COS**](https://curl.qcloud.com/empEScHz) | qcloud     | Private    | Yes                   | There is nothing to say, several private cloud storage in the most recommended, the disadvantage is that currently only provides a year of free credit, the expiration of the need to renew. |
| [**Qiniu Cloud**](https://www.qiniu.com/)                 | qiniu      | Private    | Yes                   | Provide permanent free storage quota, the disadvantage is not to provide a domain name for the stored external links, you need to own a domain name and binding operation before you can use it. |
| bilibili                                                  | bilibili   | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Sougou                                                    | sougou     | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Huluxia                                                   | huluxia    | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Catbox                                                    | catbox     | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| 360                                                       | 360        | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Tietu                                                     | postimages | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| 58                                                        | ai58       | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Jitu                                                      | gtimg      | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Baitu                                                     | bkimg      | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| Muke                                                      | muke       | Public     | Yes                   | Unusual service, supported by the API implementation of yujian image bed, used with caution. |
| [**Upay Cloud**](https://www.upyun.com/)                  | upyun      | Private    | Yes                   | Provide vouchers, the disadvantage is not to provide a domain name for the stored external links, you need to own a domain name and binding operation before you can use it. In addition, white whoring vouchers need to join the [**Alliance**](https://www.upyun.com/league), and once a year audit. |

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

### Select working language

English and Chinese are supported as working languages, the default is Chinese.

- Execute `pymdimg -l en` to switch the working language.

### Image Compression

Enabling this feature will compress images over a certain size and then upload them to the image bed to save private storage space. The compressed intermediate images will be automatically deleted from the local area and will not affect the original local images.

- Execute `pymdimg --compress` to set the relevant configuration and then turn it on.

### Switching image compression engines

GIL and tinyPNG are currently supported, the former for local compression using a third-party Gillow package, and the latter for online compression using the online service tinyPNG.com, the latter is recommended because the latter is lossless compression, but the latter requires registration to generate an access token first, and free users have the number of calls: 500 per month.

Execute `pymdimg -e tinyPNG` to switch.

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

<del>Currently supported image beds are [**sm.ms**](https://sm.ms/), Ali, [**RuYu**](https://img.rruu.net/), [**Vim-CN**](https://img.vim-cn.com/), [**meet**](https://www.hualigs.cn/), [**Tencent cloud object storage**](https://curl.qcloud.com/empEScHz) (promotional link),[**Qiniu Cloud**](https://www.qiniu.com/).</del>

For a list of supported image beds, see [**Supported Image Bed Services**](https://github.com/icexmoon/markdown-img#supported-image-bed-services).

- Excute`python -m markdown_img -i ali`

> - You can check the help documentation for the specific image bed logo.
> - Access tokens are required to switch the bed service and will be prompted to enter the appropriate access token in use.
> - Some necessary information is required to use Tencent Cloud OSS, please read the notes for details.
> - You need to provide the necessary information when using Qiniu Cloud Storage, where the DNS binding domain name needs to include the protocol, such as `http://example.domain.com`

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

## Acknowledgements

The developer of this application has received help and support from [**upyun**](https://www.upyun.com/?utm_source=lianmeng&utm_medium=referral) for its free CDN acceleration and cloud storage services, if you want to get the same help and support, you can Click [**here**](https://www.upyun.com/?utm_source=lianmeng&utm_medium=referral) to join.

## Update Log

### 0.2.8

Add globalization support. add English as a new working language.

### 0.2.9

Add Qiniu Cloud as a new optional image bed.

### 0.3.0

- Code refactoring
- Add bilibili as new image bed
- Fix some bugs

### 0.3.1

Add UPYun Cloud as a new optional image bed.

### 0.3.2

Add image compression feature.

### 0.3.3

Add TinyPNG as a new image compression engine.

### 0.3.4

Compression engine switch option add none, can be more convenient to turn off the compression function.