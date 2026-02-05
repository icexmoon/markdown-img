import sys
import os


def main():
    # sys.path.insert(-2, "D:\software\coding\python\Lib\site-packages")
    sys.path.insert(-2, "D:\\workspace\\markdown-img\\src")
    from markdown_img.main import Main

    # print(sys.path)
    current_dir = os.getcwd()
    test_dir = current_dir + "\\tests"
    # 将工作目录切换到测试目录
    os.chdir(test_dir)
    # print(os.getcwd())
    testFile = ".\\markdown_img\\test_image.md"
    if os.path.exists(testFile):
        os.remove(testFile)
    main = Main()
    main.printSysInfo()
    # main.changeImgService("upyun")
    # main.changeMainPrams({"compress_engine": "tinyPNG"})
    # main.main(True)


if __name__ == "__main__":
    main()
