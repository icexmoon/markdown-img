import os
import sys
part = __file__.rpartition('\\')
packageDirPath = part[0]
sys.path.append(packageDirPath)
from main import Main
mainProcess = Main()
mainProcess.main()
