import os
import shutil
import psutil
import sys
import threading as th
from RunData import checkDir, makeDir, getSrcPath, getDstPath, getControlDataNames
from LoadingGUI import *


loadingEncryptCheck = 0
loadingDecryptCheck = 0

def securityThread(check):
    if check==0:
        # 파일 옮기기
        #fileMove(srcPath, dstPath)
        # 파일 암호화
        #encrypt_all_files(dstPath, nickname)
        print("encrypt!")
    elif check ==1:
        # 파일 복호화 
        #decrypt_all_files(dstPath, nickname)
        # 파일 옮기기
        #fileMove(dstPath, srcPath)
        print("decrypt!")
    
app = QApplication(sys.argv)
while(True):
    
    check = 0
    
    srcPath = getSrcPath()
    dstPath = getDstPath()
    

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1

    if(check == 1):
        # 파일 복호화 
        #decrypt_all_files(dstPath, nickname)

        # 파일 옮기기
        #fileMove(dstPath, srcPath)
        if loadingDecryptCheck == 0:
            loadingDecryptCheck =1
            loadingEncryptCheck =0
            decrypt = th.Thread(target = securityThread, args=[check])
            decrypt.start()
            decryptLoding = DecryptLoadingClass()
            decryptLoding.show()
            app.exec_()


    elif (check == 0):
        # 파일 옮기기
        #fileMove(srcPath, dstPath)

        #afterTimer = time.time()

        #if((int)(afterTimer - beginTimer) == 60):   # 타이머 설정
            # 파일 암호화
        #encrypt_all_files(dstPath, nickname) 
        if loadingEncryptCheck == 0:
            loadingEncryptCheck =1
            loadingDecryptCheck =0
            encrypt = th.Thread(target = securityThread, args = [check])
            encrypt.start()
            encryptLoding = EncryptLoadingClass()
            encryptLoding.show()
            app.exec_()