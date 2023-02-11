import keyboard
import pyautogui
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
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


class EncryptLoadingClass(QDialog, encryptLoading_form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        QTimer.singleShot((int)(5000) , self.doneLoading)
        self.setWindowIcon(QIcon("windowIcon.png"))

        self.encryptLoadingGIF:QLabel


        # 동적 이미지 추가
        self.loadingmovie = QMovie('loading.gif', QByteArray(), self)
        #print(self.movie.size())
        self.loadingmovie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.encryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()
        self.show()
        self.focusThread = focusThread()
        self.focusThread.start()

    def doneLoading(self):
        self.focusThread.stop()
        self.close()


class DecryptLoadingClass(QDialog, decryptLoading_form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        QTimer.singleShot((int)(5000) , self.doneLoading)
        self.setWindowIcon(QIcon("windowIcon.png"))

        self.decryptLoadingGIF:QLabel


        # 동적 이미지 추가
        self.loadingmovie = QMovie('loading.gif', QByteArray(), self)
        #print(self.movie.size())
        self.loadingmovie.setCacheMode(QMovie.CacheAll)
        # QLabel에 동적 이미지 삽입
        self.decryptLoadingGIF.setMovie(self.loadingmovie)
        self.loadingmovie.start()
        self.show()
        self.focusThread = focusThread()
        self.focusThread.start()

    def doneLoading(self):
        self.focusThread.stop()
        self.close()



