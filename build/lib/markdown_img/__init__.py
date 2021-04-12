import getopt
import sys
import os
from .main import Main
try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'm:hi:', ['mode=', 'help','img_service='])
except getopt.GetoptError as e:
    print("获取参数信息出错，错误提示：", e.msg)
    exit()
mainProcess = Main()
if len(opts) == 0:
    mainProcess.main()
else:
    # print(opts)
    for opt in opts:
        argKey = opt[0]
        argVal = opt[1]
        if argKey == '--help' or argKey == '-h':
            mainProcess.outputHelpInfo()
        elif argKey == '--mode' or argKey == '-m':
            mode = argVal
            if mode == 'img_recove':
                mainProcess.imgRecovery()
            elif mode == 'normal':
                mainProcess.main()
            else:
                print("错误的mode参数")
        elif argKey == '--img_service' or argKey == '-i':
            mainProcess.changeImgService(argVal)
        else:
            mainProcess.main()
        break
exit()
