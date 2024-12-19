import sys
from PyQt6.QtWidgets import QApplication
import os
import dbMan
from LoginWindow import LoginWindow

if __name__ == "__main__":
    dir_cur = os.getcwd() + "/Documents/"
    print(dir_cur)
    os.makedirs(dir_cur, exist_ok=True)
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.show()
    dbMan.startAppInvoker()
    app.exec()
