import os
import shutil
import psutil
import sys
import threading as th

from RunData import checkDir, makeDir, getSrcPath, getDstPath, getControlDataNames
from CustomCrypto import encrypt_all_files, decrypt_all_files
from LoadingGUI import *


def initCheck():
    if not(checkDir()):
        makeDir()


def securityThread(check, nickname):
    if check==0:
        # 파일 옮기기
        fileMove(getSrcPath, getDstPath)
        # 파일 암호화
        encrypt_all_files(getDstPath, nickname)
        print("encrypt!")
    elif check ==1:
        # 파일 복호화 
        decrypt_all_files(getDstPath, nickname)
        # 파일 옮기기
        fileMove(getDstPath, getSrcPath)
        print("decrypt!")

def run(beginTimer, nickname,loadingEncryptCheck, loadingDecryptCheck):
    check = 0
    srcPath = getSrcPath()
    dstPath = getDstPath()

    print("run method!")
    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1

    if(check == 1):
        if loadingDecryptCheck == 0:
            loadingDecryptCheck =1
            loadingEncryptCheck =0
            decrypt = th.Thread(target = securityThread, args=[check, nickname])
            decrypt.start()
            decryptLoding = DecryptLoadingClass()
            decryptLoding.exec()
        return loadingEncryptCheck,loadingDecryptCheck
            #app.exec_()
    elif (check == 0):
        if loadingEncryptCheck == 0:
            loadingEncryptCheck =1
            loadingDecryptCheck =0
            encrypt = th.Thread(target = securityThread, args = [check, nickname])
            encrypt.start()
            encryptLoding = EncryptLoadingClass()
            encryptLoding.exec()
            #app.exec_()
        return loadingEncryptCheck,loadingDecryptCheck

def fileMove(srcPath, dstPath):
    filenames = getControlDataNames()

    for filename in filenames:
        if(os.path.isfile(srcPath + filename)):
            if(os.path.exists(dstPath + filename)):
                os.remove(dstPath + filename)
            shutil.move(srcPath + filename, dstPath + filename)

        elif(os.path.isdir(srcPath + filename)):
            if(os.path.exists(dstPath + filename)):
                shutil.rmtree(dstPath + filename)
            shutil.move(srcPath + filename, dstPath + filename)
