import keyboard, pyautogui
import time
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *

from CustomCrypto import encrypt_all_files, decrypt_all_files
from RunData import guestFileRemove, initLocalCheck, memberFileRemove


encryptLoading_form_class = uic.loadUiType("UI/encryptLoadingGUI.ui")[0]
decryptLoading_form_class = uic.loadUiType("UI/decryptLoadingGUI.ui")[0]
preGuest_form_class = uic.loadUiType("UI/preGuestGui.ui")[0]
preMem_form_class = uic.loadUiType("UI/preMemGui.ui")[0]

class focusOnThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.breakPoint = False
        
    def run(self):
        size = pyautogui.size()
        while(not self.breakPoint):
            try:
                pyautogui.moveTo(size[0]/2, size[1]/2) 
                if keyboard.is_pressed('win'):
                    time.sleep(0.3)
                    pyautogui.press('winleft')
                if keyboard.is_pressed('alt'):
                    time.sleep(0.3)
                    pyautogui.press('esc')

            except:
                pass

    def stop(self):
        self.breakPoint = True
        self.terminate()
        self.wait(3000)

class preGuestThread(QThread):
    preGuest_signal = pyqtSignal()

    def __init__(self, srcPath):
        super().__init__()
        self.srcPath = srcPath

    def run(self):
        guestFileRemove(self.srcPath, 0)
        guestFileRemove(self.srcPath, 1)
        self.preGuest_signal.emit()

class preMemThread(QThread):
    preMem_signal = pyqtSignal()

    def __init__(self, nickname):
        super().__init__()
        self.nickname = nickname

    def run(self):
        os.system('taskkill /f /im chrome.exe')
        initLocalCheck(self.nickname)
        time.sleep(1)
        self.preMem_signal.emit()


class encryptThread(QThread):
    encrypt_signal = pyqtSignal()

    def __init__(self, srcPath, dstPath, nickname):
        super().__init__()
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.nickname = nickname
    
    def run(self):
        encrypt_all_files(self.dstPath, self.nickname)
        memberFileRemove(self.srcPath, self.nickname)
        self.encrypt_signal.emit()


class decryptThread(QThread):
    decrypt_signal = pyqtSignal()

    def __init__(self, dstPath, nickname):
        super().__init__()
        self.dstPath = dstPath
        self.nickname = nickname
    
    def run(self):
        decrypt_all_files(self.dstPath, self.nickname)
        self.decrypt_signal.emit()


class EncryptLoadingClass(QDialog, encryptLoading_form_class):

    def __init__(self, srcPath, dstPath, nickname):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Image/windowIcon.png"))
        self.encryptLoadingGIF:QLabel

        self.srcPath = srcPath
        self.dstPath = dstPath
        self.nickname = nickname
        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # ?????? ????????? ??????
        self.loadingmovie = QMovie('Image/loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel??? ?????? ????????? ??????
        self.encryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.encryptTh = encryptThread(self.srcPath, self.dstPath, self.nickname)
        self.focusOnTh = focusOnThread()

        self.encryptTh.encrypt_signal.connect(self.doneLoading)

        self.encryptTh.start()
        self.focusOnTh.start()


    def doneLoading(self):
        self.encryptTh.terminate()
        self.focusOnTh.terminate()
        self.close()


class DecryptLoadingClass(QDialog, decryptLoading_form_class):
    def __init__(self, dstPath, nickname):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Image/windowIcon.png"))
        
        self.decryptLoadingGIF:QLabel

        self.dstPath = dstPath
        self.nickname = nickname

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # ?????? ????????? ??????
        self.loadingmovie = QMovie('Image/loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel??? ?????? ????????? ??????
        self.decryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.decryptTh = decryptThread(self.dstPath, self.nickname)
        self.focusOnTh = focusOnThread()

        self.decryptTh.decrypt_signal.connect(self.doneLoading)

        self.decryptTh.start()
        self.focusOnTh.start()

    def doneLoading(self):
        self.decryptTh.terminate()
        self.focusOnTh.terminate()
        self.close()

class preGuestClass(QDialog, preGuest_form_class):
    def __init__(self, srcPath):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Image/windowIcon.png"))
        self.preGuestGIF:QLabel
        self.srcPath = srcPath

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # ?????? ????????? ??????
        self.loadingmovie = QMovie('Image/loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel??? ?????? ????????? ??????
        self.preGuestGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.preGuestTh = preGuestThread(self.srcPath)
        self.focusOnTh = focusOnThread()

        self.preGuestTh.preGuest_signal.connect(self.doneProc)

        self.preGuestTh.start()
        self.focusOnTh.start()

    def doneProc(self):
        self.preGuestTh.terminate()
        self.focusOnTh.terminate()
        self.close()

class preMemClass(QDialog, preMem_form_class):
    def __init__(self, nickname):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("Image/windowIcon.png"))
        self.preMemGIF:QLabel
        self.nickname = nickname

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # ?????? ????????? ??????
        self.loadingmovie = QMovie('Image/loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel??? ?????? ????????? ??????
        self.preMemGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.preMemTh = preMemThread(self.nickname)
        self.focusOnTh = focusOnThread()

        self.preMemTh.preMem_signal.connect(self.doneProc)

        self.preMemTh.start()
        self.focusOnTh.start()

    def doneProc(self):
        self.preMemTh.terminate()
        self.focusOnTh.terminate()
        self.close()