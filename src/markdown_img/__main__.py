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
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'm:hvi:c:su:l:e:', [
            'mode=', 'help', 'version', 'img_service=', 'change_token=', 'scan', 'des_dir=', 'url_encode=', 'language=', 'compress', 'debug=', 'engine=', 'name=', 'config=', 'list_config', 'change_config='])
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
                    configFileName = getOptionVal(opts, '--config')
                    mainProcess.main(configFileName=configFileName)
                    break
                elif mode == 'refresh':
                    configFileName = getOptionVal(opts, '--config')
                    mainProcess.main(True, configFileName=configFileName)
                    break
                elif mode == 'backup_config':
                    name = getOptionVal(opts, '--name')
                    mainProcess.backupConfig(name)
                    break
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
                configFileName = getOptionVal(opts, '--config')
                mainProcess.scanAndCreateIndex(configFileName)
            elif argKey == '--url_encode' or argKey == '-u':
                params = {'url_encode_mode': argVal}
                mainProcess.changeMainPrams(params)
            elif argKey == '--language' or argKey == '-l':
                params = {'language': argVal}
                mainProcess.changeMainPrams(params)
            elif argKey == '--compress':
                mainProcess.inputCompressInfo()
            elif argKey == '--debug':
                params = {'debug': argVal}
                mainProcess.changeMainPrams(params)
            elif argKey == '--engine' or argKey == '-e':
                params = {"compress_engine": argVal}
                mainProcess.changeMainPrams(params)
            elif argKey == '--list_config':
                mainProcess.listConfigBackup()
            elif argKey == '--change_config':
                mainProcess.changeConfig(argVal)
            else:
                configFileName = getOptionVal(opts, '--config')
                mainProcess.main(configFileName=configFileName)
            break
    exit()


main()
