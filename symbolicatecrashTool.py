#coding=utf-8

import os
import shutil
import time

toolFilePath = os.getcwd() + "/"

def symbolicateMethod(crashFileName,dSYMFileName):
    spaceStr = " "
    symbolicatecrashStr = "./symbolicatecrash"
    arrowStr = ">"

    timeStr = time.strftime("%Y年%m月%d日%H时%M分%S秒",time.localtime())
    symbolicateFileName = crashFileName + "_" + timeStr + ".Crash"
    if "." in crashFileName:
        symbolicateFileName = str(crashFileName).split(".")[0] + "_" + timeStr + ".Crash"

    # ./symbolicatecrash Bind.txt Bind.app.dSYM > B.crash
    cmdStr  = 'cd ' + toolFilePath
    cmdStr  = cmdStr + ' && ' + "export DEVELOPER_DIR=\"/Applications/XCode.app/Contents/Developer\""
    toolStr = cmdStr + ' && ' + symbolicatecrashStr + spaceStr + crashFileName + spaceStr + dSYMFileName + spaceStr + arrowStr + spaceStr + symbolicateFileName
    cmdStr  = cmdStr + ' && ' + toolStr
    print(cmdStr)
    os.system(cmdStr)
    os.system("open " + toolFilePath + symbolicateFileName)
    print("解析完成")

def mycopyfile(srcfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
        return False
    else:
        fpath,fname=os.path.split(srcfile)
        if not os.path.exists(toolFilePath):
            os.makedirs(toolFilePath)
        shutil.copy(srcfile, toolFilePath + fname)
        print ("copy %s -> %s"%(srcfile, toolFilePath + fname))
        return True

def myCopyTree(srcfile,dirName):
    if not os.path.isdir(srcfile):
        print ("%s not exist!"%(srcfile))
        return False
    else:
        fpath,fname=os.path.split(srcfile)
        if not os.path.exists(toolFilePath):
            os.makedirs(toolFilePath)
        shutil.copytree(srcfile, toolFilePath+"/"+fname)
        print ("copytree %s -> %s"%(srcfile, toolFilePath + fname))
        return True

def start(copyCrashFileIsOK,copyDSYMFileIsOK,crashFileName,dSYMFileName):
    if not copyCrashFileIsOK:
        copyCrashFileResult,crashFileName = copyCrashFile()
        if not copyCrashFileResult:
            print(".crash 文件复制失败, 请检查文件路径")
            start(copyCrashFileResult,copyDSYMFileIsOK,crashFileName,dSYMFileName)
            return
        else:
            start(copyCrashFileResult,copyDSYMFileIsOK,crashFileName,dSYMFileName)
            return
    
    if not copyDSYMFileIsOK:
        copyDSYMFileResult,dSYMFileName = copyDSYMFile()
        if not copyDSYMFileResult:
            print(".dSYM 文件复制失败, 请检查文件路径")
            start(copyCrashFileIsOK,copyDSYMFileResult,crashFileName,dSYMFileName)
            return
        else:
            start(copyCrashFileIsOK,copyDSYMFileResult,crashFileName,dSYMFileName)
            return

    if copyCrashFileIsOK and copyDSYMFileIsOK:
        symbolicateMethod(crashFileName=crashFileName,dSYMFileName=dSYMFileName)

def copyDSYMFile():
    dirlist = os.listdir(toolFilePath)
    for fileName in dirlist:
        if ".dSYM" in fileName:
            print("工具文件夹内已存在 .dSYM 文件")
            return True,fileName

    dSYMLogPath  = raw_input("请拖入 .dSYM 文件:")
    if ' ' in dSYMLogPath:
        dSYMLogPath = str(dSYMLogPath).replace(" ","")
    fpath,fname=os.path.split(dSYMLogPath)
    moveResult = myCopyTree(dSYMLogPath,fname)
    if moveResult:
        return True,fname
    else:
        return False,""

def copyCrashFile():
    # 复制 crash 文件，可以为 .Crash .crash .txt 格式
    supportType = [".Crash",".crash",".txt"]
    crashLogPath  = raw_input("请拖入崩溃日志，支持" + str(supportType) + "类型:")
    if ' ' in crashLogPath:
        crashLogPath = str(crashLogPath).replace(" ","")
    fpath,fname=os.path.split(crashLogPath)

    fileExt = os.path.splitext(fname)[-1]
    if fileExt not in supportType:
        print("crash 文件类型错误")
        return False,""

    copyResult = mycopyfile(crashLogPath)
    if copyResult:
        return True,fname
    else:
        return False,""

start(False,False,"","")