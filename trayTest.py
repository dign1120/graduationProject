import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)

trayIcon = QSystemTrayIcon(QIcon("windowIcon.png"), parent = app)
trayIcon.setToolTip("PIM Agent")
trayIcon.show()

menu = QMenu()
exitAction = menu.addAction('Exit')
exitAction.triggered.connect(app.quit)

trayIcon.setContextMenu(menu)

sys.exit(app.exec_())