import keyboard
import pyautogui
import time
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *

from CustomCrypto import encrypt_all_files
from RunData import guestFileRemove, initLocalCheck, memberFileRemove

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

encryptLoading_form_class = uic.loadUiType(BASE_DIR + r'\UI\encryptLoadingGUI.ui')[0]
preGuest_form_class = uic.loadUiType(BASE_DIR + r'\UI\preGuestGui.ui')[0]
preMem_form_class = uic.loadUiType(BASE_DIR + r'\UI\preMemGui.ui')[0]

class focusOnThread(QThread):

    def __init__(self):
        super().__init__()
        self.breakPoint = False

    def run(self):
        size = pyautogui.size()
        for i in range(150):
            keyboard.block_key(i)
        while(not self.breakPoint):
            try:
                pyautogui.moveTo(size[0]/2, size[1]/2)
            except:
                pass


class preGuestThread(QThread):
    preGuest_signal = pyqtSignal()

    def __init__(self, srcPath):
        super().__init__()
        self.srcPath = srcPath

    def run(self):
        guestFileRemove(self.srcPath, 0)
        guestFileRemove(self.srcPath, 1)
        time.sleep(3)
        self.preGuest_signal.emit()



class preMemThread(QThread):
    preMem_signal = pyqtSignal()

    def __init__(self, nickname, member_setting):
        super().__init__()
        self.nickname = nickname
        self.member_setting = member_setting

    def run(self):
        os.system('taskkill /f /im chrome.exe')
        initLocalCheck(self.nickname, self.member_setting)
        time.sleep(1)
        self.preMem_signal.emit()
    

class encryptThread(QThread):
    encrypt_signal = pyqtSignal()

    def __init__(self, srcPath, dstPath, nickname, member_setting):
        super().__init__()
        self.srcPath = srcPath
        self.dstPath = dstPath
        self.nickname = nickname
        self.member_setting = member_setting

    def run(self):
        encrypt_all_files(self.dstPath, self.nickname)
        memberFileRemove(self.srcPath, self.nickname, self.member_setting)
        time.sleep(1)
        self.encrypt_signal.emit()

class EncryptLoadingClass(QDialog, encryptLoading_form_class):

    def __init__(self, srcPath, dstPath, nickname, member_setting):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(BASE_DIR + r"\Image\windowIcon.png"))
        self.encryptLoadingGIF: QLabel

        self.srcPath = srcPath
        self.dstPath = dstPath
        self.nickname = nickname
        self.member_setting = member_setting

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint)

        # 동적 이미지 추가
        self.loadingmovie = QMovie(
            BASE_DIR + r'\Image\loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel에 동적 이미지 삽입
        self.encryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.encryptTh = encryptThread(self.srcPath, self.dstPath, self.nickname, self.member_setting)
        self.focusOnTh = focusOnThread()

        self.encryptTh.encrypt_signal.connect(self.doneLoading)

        self.encryptTh.start()
        self.focusOnTh.start()

    def doneLoading(self):
        self.encryptTh.terminate()
        self.focusOnTh.terminate()
        keyboard.unhook_all()
        self.close()

class preGuestClass(QDialog, preGuest_form_class):
    def __init__(self, srcPath):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(BASE_DIR + r"\Image\windowIcon.png"))
        self.preGuestGIF: QLabel
        self.srcPath = srcPath

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint)

        # 동적 이미지 추가
        self.loadingmovie = QMovie(
            BASE_DIR + r'\Image\loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel에 동적 이미지 삽입
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
        keyboard.unhook_all()
        self.close()


class preMemClass(QDialog, preMem_form_class):
    def __init__(self, nickname, member_setting):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(BASE_DIR + r"\Image\windowIcon.png"))
        self.preMemGIF: QLabel
        self.nickname = nickname
        self.member_setting = member_setting

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint |
                            Qt.FramelessWindowHint)

        # 동적 이미지 추가
        self.loadingmovie = QMovie(
            BASE_DIR + r'\Image\loadingImg.gif', QByteArray(), self)
        self.loadingmovie.setCacheMode(QMovie.CacheAll)

        # QLabel에 동적 이미지 삽입
        self.preMemGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()

        self.preMemTh = preMemThread(self.nickname, self.member_setting)
        self.focusOnTh = focusOnThread()

        self.preMemTh.preMem_signal.connect(self.doneProc)

        self.preMemTh.start()
        self.focusOnTh.start()

    def doneProc(self):
        self.preMemTh.terminate()
        self.focusOnTh.terminate()
        keyboard.unhook_all()
        self.close()
        