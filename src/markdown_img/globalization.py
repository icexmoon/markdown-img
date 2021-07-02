from typing import Any
from .config import Config


class Globalization:
    """国际化类"""
    textCN = {"program_version": "软件版本",
              "colon": "：",
              "working_language": "工作语言",
              "current_used_image_bed": "当前使用的图床",
              "whether_to_use_url_encoding": "是否使用URL ENCODE",
              "no_use": "不使用",
              "use_only_for_spaces": "仅对空格使用",
              "encoding_all_non_ascii_characters": "对非ASCII字符均进行编码",
              "image_bed_configs": "图床的相关配置信息",
              "access_token": "访问令牌",
              "storage_bucket": "存储桶",
              "region": "地域",
              "storage_directory": "存储目录",
              "missing_smms_token": "缺少你的sm.ms访问令牌，请输入",
              "token_has_saved": "访问令牌已保存，请重新运行程序",
              "missing_ruyu_token": "缺少你的如优图床访问令牌，请输入",
              "update_image_fail": "上传图片到{}失败，请检查日志文件",
              "missing_meet_token": "缺少你的遇见图床访问令牌，请输入",
              "missing_tencent_oss_info": "缺少腾讯云OSS必须的连接信息，请按提示逐一输入",
              "secret_id_input": "请输入secret_id",
              "secret_key_input": "请输入secret_key",
              "region_input": "请输入region",
              "bucket_input": "请输入bucket",
              "storage_dir_input": "请输入目标存储目录",
              "new_secret_id_input": "请输入新的secret_id",
              "new_secret_key_input": "请输入新的secret_key",
              "new_region_input": "请输入新的region",
              "new_bucket_input": "请输入新的bucket",
              "new_storage_dir_input": "请输入新的目标存储目录",
              "tencent_oss_info_saved": "腾讯云OSS信息已保存，请重新运行程序",
              "undefined_error_info": "未定义错误，请联系开发者",
              "deal_success": "已成功处理markdown文件",
              "all_file_done": "所有markdown文档已处理完毕",
              "recove_markdown_file": "已成功还原markdown文件{}的本地图库",
              "images_number_is_not_equal": "文件{}中的图片数目与备份中的数目不相符，请自行确认",
              "not_support_img_service": "不支持的图床服务",
              "image_bed_changed": "图床已切换",
              "invalid_image_bed": "不是合法的图床",
              "new_token_input": "请输入新的访问令牌",
              "token_changed_successfully": "已成功更新访问令牌",
              "no_find_local_image": "没有找到可以处理的图片",
              "index_file_created": "已成功生成网络图床索引文件：markdown_img_index.md",
              "image_web_configs_changed": "图床配置已更新",
              "input_error_and_hint": "输入的值{}不合法，请阅读帮助文档。",
              "related_configs_changed": "相关配置已更新",
              "qiniu_info_saved": "七牛云的相关信息已保存，请重新运行程序",
              "qiniu_info_required": "缺少七牛云的相关配置，请按提示输入",
              "qiniu_access_key_input": "请输入七牛云存储的access_key",
              "qiniu_secret_key_input": "请输入七牛云存储的secret_key",
              "qiniu_dns_domain_input": "请输入七牛云DNS绑定的域名",
              "qiniu_bucket_name_input": "请输入七牛云存储的名称",
              "qiniu_new_access_key_input": "请输入新的七牛云存储access_key",
              "qiniu_new_secret_key_input": "请输入新的七牛云存储secret_key",
              "qiniu_new_dns_domain_input": "请输入新的七牛云DNS绑定的域名",
              "qiniu_new_bucket_name_input": "请输入新的七牛云存储名称",
              "qiniu_access_key": "七牛云存储access_key",
              "qiniu_secret_key": "七牛云存储secret_key",
              "qiniu_dns_domain": "七牛云DNS绑定的域名",
              "qiniu_bucket_name": "七牛云存储的名称",
              }
    textEN = {"program_version": "program version",
              "colon": ":",
              "working_language": "working language",
              "current_used_image_bed": "current used image bed",
              "whether_to_use_url_encoding": "whether to use URL ENCODE",
              "no_use": "no use",
              "use_only_for_spaces": "use only for spaces",
              "encoding_all_non_ascii_characters": "encoding of all non-ASCII characters",
              "image_bed_configs": "relevant configuration information for the image bed",
              "access_token": "Access Token",
              "storage_bucket": "storage bucket",
              "region": "region",
              "storage_directory": "storage directory",
              "missing_smms_token": "Missing your sm.ms access token, please enter",
              "token_has_saved": "The access token has been saved, please re-run the program",
              "missing_ruyu_token": "Missing your RuYu image bed access token, please enter",
              "update_image_fail": "Uploading images to {} failed, please check the log file",
              "missing_meet_token": "Missing your meet image bed access token, please enter",
              "missing_tencent_oss_info": "Missing connection information required by Tencent Cloud OSS, please enter one by one as prompted",
              "secret_id_input": "Please enter the secret_id",
              "secret_key_input": "Please enter the secret_key",
              "region_input": "Please enter the region",
              "bucket_input": "Please enter the bucket",
              "storage_dir_input": "Please enter the storage directory",
              "new_secret_id_input": "Please enter the new secret_id",
              "new_secret_key_input": "Please enter the new secret_key",
              "new_region_input": "Please enter the new region",
              "new_bucket_input": "Please enter the new bucket",
              "new_storage_dir_input": "Please enter the new storage directory",
              "tencent_oss_info_saved": "Tencent Cloud OSS information has been saved, please re-run the program",
              "undefined_error_info": "Undefined error, please contact the developer",
              "deal_success": "Successfully processed markdown files",
              "all_file_done": "All markdown documents have been processed",
              "recove_markdown_file": "The local gallery of markdown file {} has been successfully restored",
              "images_number_is_not_equal": "The number of images in file {} does not match the number in the backup, please check yourself",
              "not_support_img_service": "Unsupported image bed services",
              "image_bed_changed": "The image bed has been switched",
              "invalid_image_bed": "Not a legal image bed",
              "new_token_input": "Please enter a new access token",
              "token_changed_successfully": "Access token has been successfully updated",
              "no_find_local_image": "No images found that can be processed",
              "index_file_created": "The webbed index file has been successfully generated: markdown_img_index.md",
              "image_web_configs_changed": "The image bed configuration has been updated",
              "input_error_and_hint": "The entered value {} is not legal, please read the help documentation.",
              "related_configs_changed": "Related configurations have been updated",
              "qiniu_info_saved": "The information about the qiniu cloud has been saved, please re-run the program",
              "qiniu_info_required": "Missing configuration of the qiniu cloud, please follow the prompts to enter",
              "qiniu_access_key_input": "Please enter the access_key of the qiniu cloud storage",
              "qiniu_secret_key_input": "Please enter the secret_key of the qiniu cloud storage",
              "qiniu_dns_domain_input": "Please enter the domain name of the DNS binding of the qiniu cloud",
              "qiniu_bucket_name_input": "Please enter the name of the qiniu cloud storage",
              "qiniu_new_access_key_input": "Please enter the new qiniu cloud storage access_key",
              "qiniu_new_secret_key_input": "Please enter the new qiniu cloud storage secret_key",
              "qiniu_new_dns_domain_input": "Please enter the domain name of the new qiniu cloud DNS binding",
              "qiniu_new_bucket_name_input": "Please enter a new name for the qiniu cloud storage",
              "qiniu_access_key": "Qiniu Cloud Storage access_key",
              "qiniu_secret_key": "Qiniu Cloud Storage secret_key",
              "qiniu_dns_domain": "The domain of Qiniu Cloud DNS bunding",
              "qiniu_bucket_name": "Qiniu Cloud Storage name",
              }

    def __new__(cls) -> Any:
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__new__(cls))
        return getattr(cls, "__instance")

    def __init__(self) -> None:
        pass

    def getText(self, textKey: str) -> str:
        languageDict: dict
        sysConfig = Config()
        language = sysConfig.getConfigParam(Config.PARAM_LANGUAGE)
        if language == Config.LANGUAGE_CN:
            languageDict = self.__class__.textCN
        elif language == Config.LANGUAGE_EN:
            languageDict = self.__class__.textEN
        else:
            languageDict = self.__class__.textCN
        text: str
        if textKey in languageDict:
            text = languageDict[textKey]
        else:
            defaultLanguageDict = self.__class__.textCN
            if textKey in defaultLanguageDict:
                text = defaultLanguageDict[textKey]
            else:
                text = textKey
        return text
