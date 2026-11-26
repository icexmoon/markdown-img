import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from markdown_img.config import Config
from markdown_img.main import Main
from markdown_img.qcloud_client import QcloudClient
from markdown_img.smms_img import SmmsImg


class ImagePathsWithSpacesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.main = Main.__new__(Main)

    def test_uploads_and_replaces_space_paths_with_qcloud(self):
        image = self.directory / "picture name.png"
        image.write_bytes(b"image contents")
        raw_path = str(image)
        encoded_path = raw_path.replace(" ", "%20")
        original = self.directory / "source.md"
        original.write_text(
            f"![one](<{raw_path}>) ![two]({encoded_path})\n"
            f'<img src="{encoded_path}" />',
            encoding="utf-8",
        )
        output = self.directory / "copy.md"

        client = QcloudClient.__new__(QcloudClient)
        client.bucket = "bucket-123"
        client.region = "region"
        client.client = Mock()
        client.client.head_object.return_value = {"ETag": '"etag"', "Content-Length": "14"}
        bodies = []
        def put_object(**kwargs):
            bodies.append((kwargs["Key"], kwargs["Body"].read()))
            return {"ETag": '"etag"'}
        client.client.put_object.side_effect = put_object

        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = Mock(
            side_effect=lambda path: client.upload(path, "folder name")
        )
        with patch("markdown_img.main.SmmsImg", return_value=server), patch.object(
            self.main, "getCopyFilePath", return_value=str(output)
        ):
            self.main.dealMdFile(str(original), self.main._Main__createWebImgCopy)

        url = "https://bucket-123.cos.region.myqcloud.com/folder%20name/picture%20name.png"
        self.assertEqual(
            output.read_text(encoding="utf-8"),
            f'![one](<{url}>) ![two]({url})\n<img src="{url}" />',
        )
        self.assertEqual(bodies, [("folder name/picture name.png", b"image contents")])
        server.uploadOne.assert_called_once_with(raw_path)

    def test_upload_urls_preserve_existing_encoding(self):
        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = Mock(side_effect=lambda path: {
            "plain": "https://example.com/image.png",
            "encoded": "https://example.com/already%20encoded.png",
            "space": "https://example.com/image name.png",
        }[path])
        results = {}
        server.multiUploadImage(["plain", "encoded", "space"], results)
        self.assertEqual(results, {
            "plain": "https://example.com/image.png",
            "encoded": "https://example.com/already%20encoded.png",
            "space": "https://example.com/image%20name.png",
        })

    def test_qcloud_standard_encoding_is_not_applied_twice(self):
        image = self.directory / "图片 name.png"
        image.write_bytes(b"image contents")
        client = QcloudClient.__new__(QcloudClient)
        client.bucket = "bucket-123"
        client.region = "region"
        client.client = Mock()
        client.client.put_object.return_value = {"ETag": '"etag"'}
        client.client.head_object.return_value = {"ETag": '"etag"', "Content-Length": "14"}
        server = SmmsImg.__new__(SmmsImg)
        server.uploadOne = Mock(
            side_effect=lambda path: client.upload(
                path, "folder name", Config.URL_ENCODE_MODE_STANDARD
            )
        )
        results = {}
        server.multiUploadImage([str(image)], results)
        self.assertEqual(
            results[str(image)],
            "https://bucket-123.cos.region.myqcloud.com/"
            "folder%20name/%E5%9B%BE%E7%89%87%20name.png",
        )

    def test_literal_percent_filename_takes_precedence(self):
        literal = self.directory / "picture%20name.png"
        literal.write_bytes(b"literal")
        (self.directory / "picture name.png").write_bytes(b"decoded")
        self.assertEqual(self.main.resolveImgPath(str(literal)), str(literal))

    def test_scans_last_markdown_line_without_newline(self):
        image = self.directory / "picture name.png"
        image.write_bytes(b"image contents")
        original = self.directory / "source.md"
        original.write_text(f"![image]({image})", encoding="utf-8")
        process = Mock()
        self.main.dealMdFile(str(original), process)
        process.assert_called_once_with({str(image)}, str(original))

    def test_relative_copy_uses_decoded_source_path(self):
        image = self.directory / "picture name.png"
        image.write_bytes(b"image contents")
        original = self.directory / "source.md"
        encoded_path = str(image).replace(" ", "%20")
        original.write_text(f"![image](<{encoded_path}>)", encoding="utf-8")
        images_dir = self.directory / "images"
        images_dir.mkdir()
        backup_dir = self.directory / "backup"
        backup_dir.mkdir()
        config = Mock()
        config.getImagesDirPath.return_value = str(images_dir)
        config.getBackUpDirPath.return_value = str(backup_dir)
        config.getPathSplit.return_value = os.sep
        with patch("markdown_img.main.Config", return_value=config):
            self.main.dealMdFile(
                str(original), self.main._Main__replaceWithRelativeMDFile
            )
        self.assertEqual(
            original.read_text(encoding="utf-8"), "![image](<./images/picture name.png>)"
        )
        self.assertEqual((images_dir / image.name).read_bytes(), b"image contents")
        self.assertEqual(
            (backup_dir / original.name).read_text(encoding="utf-8"),
            f"![image](<{encoded_path}>)",
        )

    def test_recovery_decodes_missing_paths(self):
        markdown_image = str(self.directory / "markdown image.png")
        html_image = str(self.directory / "html image.png")
        original = self.directory / "source.md"
        original.write_text(
            f'![image](<{markdown_image.replace(" ", "%20")}>)\n'
            f'<img src="{html_image.replace(" ", "%20")}" />',
            encoding="utf-8",
        )
        copy = self.directory / "copy.md"
        copy.write_text(
            '![image](<https://example.com/markdown.png>)\n'
            '<img src="https://example.com/html.png" />',
            encoding="utf-8",
        )
        downloader = Mock()
        with patch("markdown_img.main.DownloadHelp", return_value=downloader):
            self.assertTrue(self.main.recoveryImgsInMarkdown(str(copy), str(original)))
        self.assertEqual(
            downloader.chunkDownload.call_args_list,
            [
                unittest.mock.call(
                    "https://example.com/markdown.png", markdown_image, timeout=2
                ),
                unittest.mock.call("https://example.com/html.png", html_image, timeout=2),
            ],
        )


if __name__ == "__main__":
    unittest.main()
