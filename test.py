from ctypes import Structure, windll, c_uint, sizeof, byref
import time

print(windll.kernel32.GetTickCount())

class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]
lastInputInfo = LASTINPUTINFO()
lastInputInfo.cbSize = sizeof(lastInputInfo)

i=0
while(i<10):
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    print(lastInputInfo.dwTime)
    time.sleep(1)
    i+=1
windll.kernel32.GetTickCount() - lastInputInfo.dwTime
