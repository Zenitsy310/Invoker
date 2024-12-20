from PyQt6.QtWidgets import *
import MainApp
import MainAppAdmin
from Window import Window

class LoginWindow(Window):
    def __init__(self):
        super().__init__()

        labels = {}
        self.lineEdits = {}

        labels['Username'] = QLabel('Имя Пользователя')
        labels['Password'] = QLabel('Пароль')

        labels['Username'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        labels['Password'].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.lineEdits['Username'] = QLineEdit('admin')
        self.lineEdits['Password'] = QLineEdit('admin')
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)
        # layout.addWidget(labelBg)
        self.layout.addWidget(labels['Username'], 0, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Username'], 0, 1, 1, 3)

        self.layout.addWidget(labels['Password'], 1, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Password'], 1, 1, 1, 3)

        button_login = QPushButton('Войти', clicked=self.checkCredential)
        self.layout.addWidget(button_login, 2, 3, 1, 1)

        button_registration = QPushButton('Регистрация', clicked=self.openRegWindow)
        self.layout.addWidget(button_registration, 3, 3, 1, 1)

    def checkCredential(self):
        import dbMan
        array_aut = [''] * 2
        array_aut[0] = self.lineEdits['Username'].text()
        array_aut[1] = self.lineEdits['Password'].text()
        for i in range(len(array_aut)):
            if array_aut[i] == '':
                self.showDilog("Все ячейки должня быть заполнены")
                break
            elif array_aut[i] != '' and i == len(array_aut)-1:
                dbMan.auth(self, array_aut[0], array_aut[1])

    def showDilog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Invoker")
        dlg.setText(message)
        dlg.setStyleSheet('''
            color: black
        ''')
        dlg.exec()

    def openMainWindow(self, user_info):
        self.mainWindow = MainApp.MainApp(user_info)
        self.mainWindow.show()
        self.close()

    def openAdminWindow(self,current_admin):
        self.mainWindow = MainAppAdmin.MainAppAdmin(current_admin)
        self.mainWindow.show()
        self.close()

    def openRegWindow(self):
        from RegistrationWindow import RegistrationWindow
        self.regWindow = RegistrationWindow()
        self.regWindow.show()
        self.close()

# dbMan.addInfoUser(self,username,password)

