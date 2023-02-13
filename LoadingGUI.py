import keyboard
import pyautogui
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic,QtCore
from PyQt5.QtCore import *

encryptLoading_form_class = uic.loadUiType("encryptLoadingGUI.ui")[0]
decryptLoading_form_class = uic.loadUiType("decryptLoadingGUI.ui")[0]

class focusThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.breakPoint = False
    
    def run(self):
        size = pyautogui.size()
        while(not self.breakPoint):
            try:
                pyautogui.moveTo(size[0]/2, size[1]/2)
                if keyboard.is_pressed('win'):
                    print("win")
                    time.sleep(0.3)
                    pyautogui.press('winleft')

            except:
                pass
    def stop(self):
        self.breakPoint = True
        self.quit()
        self.wait(3000)


class encryptLoadingThread(QThread):
    def __init__(self):
        super().__init__()
        

    def run(self):
        print("encryptLoadingThread")
        self.encryptLoad = EncryptLoadingClass()
        
        self.encryptLoad.exec()

    def stop(self):
        self.encryptLoad.doneLoading()
        self.quit()
        self.wait(3000)


class decryptLoadingThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        print("decryptLoadingThread")
        self.decryptLoad = DecryptLoadingClass()
        self.decryptLoad.exec()

    def stop(self):
        self.decryptLoad.doneLoading()
        self.quit()
        self.wait(3000)


        
class EncryptLoadingClass(QDialog, encryptLoading_form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("windowIcon.png"))

        self.encryptLoadingGIF:QLabel

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        size = pyautogui.size()
        self.move(size[0]/2, 0)
        # 동적 이미지 추가
        self.loadingmovie = QMovie('loading.gif', QByteArray(), self)
        #print(self.movie.size())
        self.loadingmovie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.encryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()
        #self.focusThread = focusThread()
        #self.focusThread.start()

    def doneLoading(self):
        #self.focusThread.stop()
        self.close()


class DecryptLoadingClass(QDialog, decryptLoading_form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("windowIcon.png"))

        self.decryptLoadingGIF:QLabel

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        size = pyautogui.size()
        self.move(size[0]/2, 0)
        # 동적 이미지 추가
        self.loadingmovie = QMovie('loading.gif', QByteArray(), self)
        #print(self.movie.size())
        self.loadingmovie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.decryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()
        #self.focusThread = focusThread()
        #self.focusThread.start()

    def doneLoading(self):
        #self.focusThread.stop()
        self.close()



