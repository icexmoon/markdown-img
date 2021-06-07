import getopt
import sys
import os
from .main import Main


def getOptionVal(options, key):
    for optKey, optVal in options:
        if optKey == key:
            return optVal
    return None


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'm:hvi:c:su:', [
            'mode=', 'help', 'version', 'img_service=', 'change_token=', 'scan', 'des_dir=','url_encode='])
    except getopt.GetoptError as e:
        print("获取参数信息出错，错误提示：", e.msg)
        exit()
    mainProcess = Main()
    if len(opts) == 0:
        mainProcess.main()
    else:
        for opt in opts:
            argKey = opt[0]
            argVal = opt[1]
            if argKey == '--help' or argKey == '-h':
                mainProcess.outputHelpInfo()
            elif argKey == '--version' or argKey == '-v':
                mainProcess.printSysInfo()
            elif argKey == '--mode' or argKey == '-m':
                mode = argVal
                if mode == 'img_recove':
                    mainProcess.imgRecovery()
                elif mode == 'normal':
                    mainProcess.main()
                elif mode == 'refresh':
                    mainProcess.main(True)
                else:
                    print("错误的mode参数")
            elif argKey == '--img_service' or argKey == '-i':
                mainProcess.changeImgService(argVal)
            elif argKey == '--change_token' or argKey == '-c':
                optDesDirVal = getOptionVal(opts, '--des_dir')
                if argVal == 'qcloud' and optDesDirVal is not None:
                    mainProcess.changeImgServiceOption(
                        argVal, {'des_dir': optDesDirVal})
                else:
                    mainProcess.changeToken(argVal)
            elif argKey == '--scan' or argKey == '-s':
                mainProcess.scanAndCreateIndex()
            elif argKey == '--url_encode' or argKey == '-u':
                params = {'use_url_encode':argVal}
                mainProcess.changeMainPrams(params)
            else:
                mainProcess.main()
            break
    exit()


main()
