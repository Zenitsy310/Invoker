from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import*


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Invoker')
        self.setWindowIcon(QIcon('Images/invoker _icon.jpg'))
        self.window_width, self.window_height = 1200, 700
        self.setFixedSize(self.window_width, self.window_height)
        self.pixmap = QPixmap('Images/Invoker_bg_admin.png')
        self.labelbg = QLabel(self)
        self.labelbg.setPixmap(self.pixmap)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.labelbg.resize(self.window_width, self.window_height)
        self.setStyleSheet(open("style.qss", "r").read())

    def showDilog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Invoker")
        dlg.setText(message)
        dlg.setStyleSheet('''
            color: black
        ''')
        dlg.exec()
