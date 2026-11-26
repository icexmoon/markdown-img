import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.parse import unquote

from qcloud_cos import CosConfig
from qcloud_cos.cos_exception import CosClientError, CosServiceError

from markdown_img.config import Config
from markdown_img.globalization import Globalization
from markdown_img.img_service.qcloud_img_service import QcloudImgService
from markdown_img.main import Main
from markdown_img.qcloud_client import QcloudClient
from markdown_img.smms_img import SmmsImg
from markdown_img.user_exception import UserException


class QcloudUploadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.image = self.directory / "picture.png"
        self.image.write_bytes(b"image")
        self.client = QcloudClient.__new__(QcloudClient)
        self.client.bucket = "bucket-123"
        self.client.region = "region"
        self.client.client = Mock()
        self.client.client.put_object.return_value = {"etag": '"etag"'}
        self.client.client.head_object.return_value = {
            "ETag": '"etag"', "Content-Length": "5"
        }

    def test_special_key_is_preserved_and_url_is_safe_in_all_modes(self):
        directory = '菜市场"芹菜三姐妹"：90% 的人分不清，连 AI 都会认错'
        for mode in (Config.URL_ENCODE_MODE_NONE, Config.URL_ENCODE_MODE_ONLY_SPACE,
                     Config.URL_ENCODE_MODE_STANDARD):
            with self.subTest(mode=mode):
                url = self.client.upload(str(self.image), directory, mode)
                key = directory + "/picture.png"
                self.assertEqual(self.client.client.put_object.call_args.kwargs["Key"], key)
                self.assertTrue(self.client.client.put_object.call_args.kwargs["EnableMD5"])
                self.client.client.head_object.assert_called_with(
                    Bucket="bucket-123", Key=key
                )
                self.assertEqual(unquote(url.split(".myqcloud.com/", 1)[1]), key)
                self.assertNotIn('"', url)
                self.assertNotIn(" ", url)
                self.assertIn("%25", url)

    def test_empty_directory_uses_root_key(self):
        url = self.client.upload(str(self.image), "")
        self.assertEqual(url, "https://bucket-123.cos.region.myqcloud.com/picture.png")
        self.client.client.head_object.assert_called_once_with(
            Bucket="bucket-123", Key="picture.png"
        )

    def test_sdk_encodes_special_characters_in_request_path(self):
        key = '菜市场"芹菜三姐妹"：90% 的人分不清/picture.png'
        config = CosConfig(Region="ap-guangzhou", SecretId="id", SecretKey="key")
        request_url = config.uri(bucket="bucket-123", path=key)
        self.assertIn("%22", request_url)
        self.assertIn("%25", request_url)
        self.assertEqual(unquote(request_url.split(".myqcloud.com/", 1)[1]), key)

    def test_verification_rejects_mismatched_or_missing_metadata(self):
        for metadata in (
            {"ETag": '"other"', "Content-Length": "5"},
            {"ETag": '"etag"', "Content-Length": "4"},
            {"Content-Length": "5"},
        ):
            with self.subTest(metadata=metadata):
                self.client.client.head_object.return_value = metadata
                with self.assertRaises(RuntimeError):
                    self.client.upload(str(self.image), "folder")
        self.client.client.put_object.return_value = {}
        self.client.client.head_object.return_value = {"ETag": '"etag"', "Content-Length": "5"}
        with self.assertRaises(RuntimeError):
            self.client.upload(str(self.image), "folder")

    def test_service_reports_sdk_failures_including_head(self):
        service = QcloudImgService()
        service.qclient = self.client
        info = {
            Config.QCLOUD_INFO_SECRET_ID: "id",
            Config.QCLOUD_INFO_SECRET_KEY: "key",
            Config.QCLOUD_INFO_REGION: "region",
            Config.QCLOUD_INFO_BUCKET: "bucket-123",
            Config.QCLOUD_INFO_DES_DIR: "folder",
        }
        config = Mock()
        config.getConfigParam.return_value = Config.URL_ENCODE_MODE_NONE
        with patch.object(service, "getConfigInfo", return_value=info), patch(
            "markdown_img.img_service.qcloud_img_service.Config.getInstance", return_value=config
        ):
            for operation, error in (
                ("put_object", CosServiceError("PUT", "Access denied", 403)),
                ("head_object", CosClientError("head timed out")),
            ):
                with self.subTest(operation=operation):
                    method = getattr(self.client.client, operation)
                    method.side_effect = error
                    with self.assertRaises(UserException) as raised:
                        service.upload(str(self.image))
                    self.assertEqual(raised.exception.getErrorCode(), UserException.CODE_UPLOAD_ERROR)
                    self.assertIn(str(error), raised.exception.getErrorMsg())
                    if operation == "put_object":
                        self.assertIn("403", raised.exception.getErrorMsg())
                    else:
                        self.assertIn("HeadObject", raised.exception.getErrorMsg())
                    method.side_effect = None

    def test_cos_errors_report_status_specific_possible_causes(self):
        cases = (
            (400, "对象键"),
            (403, "密钥"),
            (404, "存储桶"),
            (503, "稍后重试"),
        )
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]):
            for status, hint in cases:
                with self.subTest(status=status):
                    self.client.client.put_object.side_effect = CosServiceError("PUT", "error", status)
                    with self.assertRaises(RuntimeError) as raised:
                        self.client.upload(str(self.image), "folder")
                    self.assertIn(f"HTTP {status}", str(raised.exception))
                    self.assertIn(hint, str(raised.exception))

    def test_partial_config_is_reported_for_every_image_without_creating_copy(self):
        images = [self.image, self.directory / "another.png"]
        images[1].write_bytes(b"image")
        original = self.directory / "source.md"
        original.write_text("\n".join(f"![image]({p})" for p in images), encoding="utf-8")
        output = self.directory / "copy.md"
        info = {
            Config.QCLOUD_INFO_SECRET_ID: "id",
            Config.QCLOUD_INFO_SECRET_KEY: "key",
            Config.QCLOUD_INFO_REGION: "region",
            Config.QCLOUD_INFO_BUCKET: "bucket-123",
        }
        config = Mock()
        config.getConfigParam.side_effect = lambda key: {
            Config.PARAM_IMG_SERVICE: Config.IMG_SERVICE_QCLOUD,
            Config.PARAM_QCLOUD_INFO: info,
        }[key]
        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = QcloudImgService().upload
        main = Main()
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]), \
             patch("markdown_img.smms_img.Config.getInstance", return_value=config), \
             patch("markdown_img.main.SmmsImg", return_value=server), \
             patch.object(main, "getCopyFilePath", return_value=str(output)):
            with self.assertRaises(UserException) as raised:
                main.dealMdFile(str(original), main._Main__createWebImgCopy)
        text = raised.exception.getErrorMsg()
        self.assertIn("成功 0，失败 2", text)
        self.assertEqual(text.count("des_dir"), 2)
        for image in images:
            self.assertIn(str(image), text)
        self.assertFalse(output.exists())
        config.writeErrorLog.assert_called_once_with(text)

    def test_invalid_config_fields_and_root_directory(self):
        service = QcloudImgService()
        service.qclient = Mock()
        service.qclient.upload.return_value = "https://example.com/image.png"
        info = {
            Config.QCLOUD_INFO_SECRET_ID: "id",
            Config.QCLOUD_INFO_SECRET_KEY: "key",
            Config.QCLOUD_INFO_REGION: "region",
            Config.QCLOUD_INFO_BUCKET: "bucket-123",
            Config.QCLOUD_INFO_DES_DIR: "",
        }
        config = Mock()
        config.getConfigParam.return_value = Config.URL_ENCODE_MODE_NONE
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]), \
             patch("markdown_img.img_service.qcloud_img_service.Config.getInstance", return_value=config):
            for key in info:
                with self.subTest(missing=key), patch.object(service, "getConfigInfo", return_value={
                    k: v for k, v in info.items() if k != key
                }):
                    with self.assertRaises(UserException) as raised:
                        service.upload(str(self.image))
                    self.assertEqual(raised.exception.getErrorCode(), UserException.CODE_UPLOAD_ERROR)
                    self.assertIn(key, raised.exception.getErrorMsg())
            with patch.object(service, "getConfigInfo", return_value={**info, Config.QCLOUD_INFO_REGION: None}):
                with self.assertRaises(UserException) as raised:
                    service.upload(str(self.image))
                self.assertIn(Config.QCLOUD_INFO_REGION, raised.exception.getErrorMsg())
            with patch.object(service, "getConfigInfo", return_value=info):
                self.assertEqual(service.upload(str(self.image)), "https://example.com/image.png")
        service.qclient.upload.assert_called_once_with(str(self.image), "", Config.URL_ENCODE_MODE_NONE)

    def test_success_and_empty_batches_are_reported(self):
        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = Mock(return_value="https://example.com/image.png")
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]):
            for images in (["image.png"], []):
                with self.subTest(images=images), contextlib.redirect_stdout(io.StringIO()) as output:
                    server.multiUploadImage(images, {})
                text = output.getvalue()
                self.assertIn(f"成功 {len(images)}，失败 0", text)
                self.assertIn("成功：image.png" if images else "未找到可上传的本地图片", text)

    def test_batch_report_starts_with_qcloud_destination(self):
        server = SmmsImg.__new__(SmmsImg)
        directory = '菜市场"芹菜三姐妹"：90% 的人'
        config = Mock()
        config.getConfigParam.side_effect = lambda key: {
            Config.PARAM_IMG_SERVICE: Config.IMG_SERVICE_QCLOUD,
            Config.PARAM_QCLOUD_INFO: {
                Config.QCLOUD_INFO_BUCKET: "bucket-123",
                Config.QCLOUD_INFO_DES_DIR: directory,
            },
        }[key]

        def upload(image):
            if image == "failed.png":
                raise UserException(UserException.CODE_UPLOAD_ERROR, "COS denied")
            return "https://example.com/image.png"

        server.uploadOne = Mock(side_effect=upload)
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]), \
             patch("markdown_img.smms_img.Config.getInstance", return_value=config):
            for images in (["good.png"], ["good.png", "failed.png"]):
                with self.subTest(images=images), contextlib.redirect_stdout(io.StringIO()) as output:
                    if len(images) == 1:
                        server.multiUploadImage(images, {})
                        text = output.getvalue()
                    else:
                        with self.assertRaises(UserException) as raised:
                            server.multiUploadImage(images, {})
                        text = raised.exception.getErrorMsg()
                lines = text.splitlines()
                self.assertEqual(lines[0], f"腾讯云上传目标：存储桶 bucket-123，文件夹 {directory}")
                self.assertIn("图片上传结果", lines[1])
                self.assertIn("成功：good.png", text)
                if len(images) > 1:
                    self.assertIn("失败：failed.png：COS denied", text)

    def test_batch_reports_root_folder_in_english(self):
        server = SmmsImg.__new__(SmmsImg)
        config = Mock()
        config.getConfigParam.side_effect = lambda key: {
            Config.PARAM_IMG_SERVICE: Config.IMG_SERVICE_QCLOUD,
            Config.PARAM_QCLOUD_INFO: {
                Config.QCLOUD_INFO_BUCKET: "bucket-123",
                Config.QCLOUD_INFO_DES_DIR: "",
            },
        }[key]
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textEN[key]), \
             patch("markdown_img.smms_img.Config.getInstance", return_value=config), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            server.multiUploadImage([], {})
        self.assertEqual(
            output.getvalue().splitlines()[0],
            "Tencent Cloud upload destination: bucket bucket-123, folder (root)",
        )

    def test_batch_failure_reports_successes_errors_and_log_failure(self):
        server = SmmsImg.__new__(SmmsImg)
        def upload(image):
            if image == "two":
                raise UserException(UserException.CODE_UPLOAD_ERROR)
            if image == "three":
                raise OSError("permission denied")
            return "https://example.com/image.png"
        server.uploadOne = Mock(side_effect=upload)
        config = Mock()
        config.writeErrorLog.side_effect = OSError("log denied")
        with patch.object(Globalization, "getText", lambda self, key: Globalization.textCN[key]), \
             patch("markdown_img.smms_img.Config.getInstance", return_value=config):
            with self.assertRaises(UserException) as raised:
                server.multiUploadImage(["one", "two", "three"], {})
            text = raised.exception.getErrorMsg()
            self.assertIn("成功 1，失败 2", text)
            self.assertIn("成功：one", text)
            self.assertIn("失败：two", text)
            self.assertIn("未提供详细错误", text)
            self.assertIn("失败：three", text)
            self.assertIn("permission denied", text)
            self.assertIn("无法写入错误日志：log denied", text)
            main = Main()
            with contextlib.redirect_stdout(io.StringIO()) as output, self.assertRaises(SystemExit):
                main.dealUserException(raised.exception)
            self.assertIn(text, output.getvalue())

    def test_head_failure_reaches_batch_and_does_not_create_copy(self):
        original = self.directory / "source.md"
        original.write_text(f"![image]({self.image})", encoding="utf-8")
        output = self.directory / "copy.md"
        self.client.client.head_object.side_effect = CosClientError("head timed out")
        service = QcloudImgService()
        service.qclient = self.client
        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = service.upload
        config = Mock()
        config.getConfigParam.return_value = Config.URL_ENCODE_MODE_NONE
        main = Main()
        info = {
            Config.QCLOUD_INFO_SECRET_ID: "id",
            Config.QCLOUD_INFO_SECRET_KEY: "key",
            Config.QCLOUD_INFO_REGION: "region",
            Config.QCLOUD_INFO_BUCKET: "bucket-123",
            Config.QCLOUD_INFO_DES_DIR: "folder",
        }
        with patch.object(service, "getConfigInfo", return_value=info), \
             patch("markdown_img.main.SmmsImg", return_value=server), \
             patch.object(main, "getCopyFilePath", return_value=str(output)), \
             patch("markdown_img.img_service.qcloud_img_service.Config.getInstance", return_value=config), \
             patch("markdown_img.smms_img.Config.getInstance", return_value=config):
            with self.assertRaises(UserException) as raised:
                main.dealMdFile(str(original), main._Main__createWebImgCopy)
        self.assertIn(str(self.image), raised.exception.getErrorMsg())
        self.assertIn("head timed out", raised.exception.getErrorMsg())
        self.assertFalse(output.exists())

    def test_batch_reports_all_failures_without_creating_copy(self):
        images = [self.directory / f"picture{i}.png" for i in range(12)]
        for image in images:
            image.write_bytes(b"image")
        original = self.directory / "source.md"
        original.write_text("\n".join(f"![image]({p})" for p in images), encoding="utf-8")
        output = self.directory / "copy.md"
        server = SmmsImg.__new__(SmmsImg)

        def upload(path):
            if path in (str(images[0]), str(images[11])):
                raise UserException(UserException.CODE_UPLOAD_ERROR, "COS denied")
            return "https://example.com/image.png"

        server.uploadOne = Mock(side_effect=upload)
        config = Mock()
        main = Main()
        with patch("markdown_img.main.SmmsImg", return_value=server), patch.object(
            main, "getCopyFilePath", return_value=str(output)
        ), patch("markdown_img.smms_img.Config.getInstance", return_value=config):
            with self.assertRaises(UserException) as raised:
                main.dealMdFile(str(original), main._Main__createWebImgCopy)
        message = raised.exception.getErrorMsg()
        self.assertIn("10", message)
        self.assertIn("2", message)
        for image in (images[0], images[11]):
            self.assertIn(str(image), message)
        self.assertEqual(message.count("COS denied"), 2)
        self.assertFalse(output.exists())
        config.writeErrorLog.assert_called_once_with(message)
        self.assertEqual(server.uploadOne.call_count, 12)

    def test_refresh_failure_preserves_existing_copy_and_fails(self):
        original = self.directory / "source.md"
        copy = self.directory / "copy.md"
        original.write_text("source", encoding="utf-8")
        copy.write_text("previous copy", encoding="utf-8")
        main = Main()
        error = UserException(UserException.CODE_UPLOAD_ERROR, "image: failed")
        with patch.object(main, "_Main__loadConfigFromFile"), patch.object(
            main, "getCopyFilePath", return_value=str(copy)
        ), patch.object(main, "dealMdFile", side_effect=error), patch(
            "markdown_img.main.os.listdir", return_value=[str(original)]
        ), patch("markdown_img.main.TimeHelper.compareTwoFilsLastModifyTime", return_value=1):
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
                main.main(refresh=True)
        self.assertEqual(raised.exception.code, 1)
        self.assertEqual(copy.read_text(encoding="utf-8"), "previous copy")


if __name__ == "__main__":
    unittest.main()
