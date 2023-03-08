import os
import psutil
import time
import webbrowser
from PyQt5.QtWidgets import *

from CustomCrypto import encrypt_all_files, decrypt_all_files
from RunData import getSrcPath, getDstPath, memberFileMove, guestFileRemove
from LoadingGUI import DecryptLoadingClass, EncryptLoadingClass, preGuestClass, focusOnThread


def runGuest(beginTimer, flag):
    check = 0
    srcPath = getSrcPath()

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1
            break
    if(check == 0 and flag == False):
        
        afterTimer = time.time()

        if((int)(afterTimer - beginTimer) >= 2):   # 타이머 설정
            preGuestThread = preGuestClass(srcPath)
            preGuestThread.exec()

            return beginTimer, True

        return beginTimer, False
    elif (check == 0 and flag == True):
        return beginTimer, flag
    else:
        beginTimer = time.time()

        return beginTimer, False
    
def runGuestforTrayicon(beginTimer, flag):
    check = 0
    srcPath = getSrcPath()

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1
            break

    if(check == 0 and flag == False):
        afterTimer = time.time()

        if((int)(afterTimer - beginTimer) >= 2):   # 타이머 설정
            emptyTrayicon = QSystemTrayIcon()
            emptyTrayicon.setVisible(False)
            emptyTrayicon.show()
            
            focusThread = focusOnThread()
            focusThread.start()
            QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "개인정보 삭제 중...", 1, 1000)
            guestFileRemove(srcPath, 0)
            guestFileRemove(srcPath, 1)
            time.sleep(2)
            QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "개인정보를 삭제했습니다.", 1, 1000)
            focusThread.terminate()
            emptyTrayicon.hide()
            return beginTimer, True

        return beginTimer, False
    elif (check == 0 and flag == True):
        return beginTimer, flag
    else:
        beginTimer = time.time()

        return beginTimer, False



def runMem(beginTimer, flag, doubleCheck, nickname):
    check = 0
    srcPath = getSrcPath()
    dstPath = getDstPath(nickname)

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1
            break

    if(check == 1 and flag == 0):
        if doubleCheck == 0:
            os.system('taskkill /f /im chrome.exe')
            time.sleep(3)
            # 파일 옮기기
            memberFileMove(dstPath, srcPath, nickname)
            webbrowser.open("https://google.com")
        beginTimer = time.time()

        return beginTimer, 0, 1

    elif(check == 1 and flag == 1):
        os.system('taskkill /f /im chrome.exe')

        decryptThread = DecryptLoadingClass(dstPath, nickname)
        decryptThread.exec()

        # 파일 옮기기
        memberFileMove(dstPath, srcPath, nickname)

        webbrowser.open("https://google.com")
        beginTimer = time.time()

        return beginTimer, 0, doubleCheck
    elif (check == 0 and flag == 0):
        # 파일 옮기기
        memberFileMove(srcPath, dstPath, nickname)

        afterTimer = time.time()

        if((int)(afterTimer - beginTimer) >= 2):   # 타이머 설정
            encryptThread = EncryptLoadingClass(srcPath, dstPath, nickname)
            encryptThread.exec()

            return beginTimer, 1, 0
        else:
            return beginTimer, 0, 0
    elif (check==0 and flag == 1):
        return beginTimer, 1, doubleCheck


def runMemforTrayicon(beginTimer, flag, doubleCheck, nickname):
    check = 0
    srcPath = getSrcPath()
    dstPath = getDstPath(nickname)

    for proc in psutil.process_iter():    # 실행중인 프로세스를 순차적으로 검색
        ps_name = proc.name()               # 프로세스 이름을 ps_name에 할당

        if ps_name == "chrome.exe":
            check = 1
            break

    if(check == 1 and flag == 0):
        if doubleCheck == 0:
            os.system('taskkill /f /im chrome.exe')
            time.sleep(3)
            # 파일 옮기기
            memberFileMove(dstPath, srcPath, nickname)
            webbrowser.open("https://google.com")
        beginTimer = time.time()

        return beginTimer, 0, 1

    elif(check == 1 and flag == 1):
        os.system('taskkill /f /im chrome.exe')

        emptyTrayicon = QSystemTrayIcon()
        emptyTrayicon.setVisible(False)
        emptyTrayicon.show()
        
        focusThread = focusOnThread()
        focusThread.start()
        QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "복호화 진행 중...", 1, 1000)
        time.sleep(1)
        decrypt_all_files(dstPath,nickname)
        QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "복호화가 완료되었습니다.", 1, 1000)
        time.sleep(1)
        focusThread.terminate()
        emptyTrayicon.hide()
        
        # 파일 옮기기
        memberFileMove(dstPath, srcPath, nickname)

        webbrowser.open("https://google.com")
        beginTimer = time.time()

        return beginTimer, 0, doubleCheck
    elif (check == 0 and flag == 0):
        # 파일 옮기기
        memberFileMove(srcPath, dstPath, nickname)

        afterTimer = time.time()

        if((int)(afterTimer - beginTimer) >= 2):   # 타이머 설정
            emptyTrayicon = QSystemTrayIcon()
            emptyTrayicon.setVisible(False)
            emptyTrayicon.show()
            
            focusThread = focusOnThread()
            focusThread.start()
            QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "암호화 진행 중...", 1, 1000)
            time.sleep(1)
            encrypt_all_files(dstPath,nickname)
            QSystemTrayIcon.showMessage(emptyTrayicon, "알림:", "암호화가 완료되었습니다.", 1, 1000)
            time.sleep(1)
            focusThread.terminate()
            emptyTrayicon.hide()
            return beginTimer, 1, 0
        else:
            return beginTimer, 0, 0
    elif (check==0 and flag == 1):
        return beginTimer, 1, doubleCheck