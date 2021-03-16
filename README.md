# Markdown-img使用指南

## 用途

本程序用于扫描工作目录下的markdown文件，查找其中的本地图片并自动上传到`sm.ms`图床，并生成一个使用网络图片替换本地图片的markdown副本，存放于`当前工作目录/markdown_image`目录下。

通过以上方式实现自动批量markdown图片处理工作，以方便之后把markdown内容在网络传播。

## 注意事项

- 本程序不会改变原始markdown文件，请放心使用。
- 对于已经生成副本的原始文件，本程序不会再次处理，如果需要重新生成副本，请手动删除相应的已生成副本。
- 本程序依赖于`sm.ms`图床，请自行注册账号并生成token。
- 因为`sm.ms`图床接口有调用限制，如果出现图片上传出错的情况，可能是上传频繁导致，请等待1分钟以上时间后重新使用本程序。
- 目前本程序只支持windows。
- `sm.ms`国内访问不算友好，生成的markdown拷贝立即在网络上发布可能会显示防盗链等图片挂掉的情况，那是因为国内CDN比较慢，等一段时间就好了。

## 安装

```shell
pip install markdown-img-icexmoon
```

## 更新

```shell
pip install --upgrade markdown-img-icexmoon
```

## 使用方式

1. 使用CMD定位到将要处理的markdown文件目录。
2. 执行`python -m markdown_img`。
3. 第一次运行程序会提示你输入图床token。
4. 输入后再次执行步骤2。
5. 等待处理。
6. 完毕后查看`工作目录/markdown_img`目录。

> - 图床token存储在程序所在目录的`smms_token.config`文件中，如果需要修改的可以自行修改，也可以删除该配置文件后重新运行程序输入。
> - 稍后会丰富并完善程序的相关命令参数。




