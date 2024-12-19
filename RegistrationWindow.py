from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import MainApp
import MainAppAdmin
import dbMan
from Window import Window


class RegistrationWindow(Window):
    def __init__(self):
        super().__init__()

        self.labels = {}
        self.lineEdits = {}

        self.labels['Name'] = QLabel('Имя')
        self.labels['LastName'] = QLabel('Фамилия')
        self.labels['Patronymic'] = QLabel('Отчество')
        self.labels['Age'] = QLabel('Возраст')
        self.labels['PasportData'] = QLabel('Серия и номер паспорта')
        self.labels['Tarif'] = QLabel('Выбирете тариф')
        self.labels['Login'] = QLabel('Логин')
        self.labels['Password'] = QLabel('Пароль')

        self.lineEdits['Name'] = QLineEdit()
        self.lineEdits['LastName'] = QLineEdit()
        self.lineEdits['Patronymic'] = QLineEdit()
        self.lineEdits['Age'] = QLineEdit()
        self.lineEdits['PasportData'] = QLineEdit()
        self.lineEdits['Tarif'] = QLineEdit()
        self.lineEdits['Login'] = QLineEdit()
        self.lineEdits['Password'] = QLineEdit()
        self.lineEdits['Password'].setEchoMode(QLineEdit.EchoMode.Password)

        self.layout.addWidget(self.labels['Name'], 0, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Name'], 0, 1, 1, 3)

        self.layout.addWidget(self.labels['LastName'], 1, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['LastName'], 1, 1, 1, 3)

        self.layout.addWidget(self.labels['Patronymic'], 2, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Patronymic'], 2, 1, 1, 3)

        self.layout.addWidget(self.labels['Age'], 3, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Age'], 3, 1, 1, 3)

        self.layout.addWidget(self.labels['PasportData'], 4, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['PasportData'], 4, 1, 1, 3)

        self.combobox_tarif = QComboBox()
        self.all_tarif = dbMan.getAllTarif(self)
        #print(str(self.tarifs_name)+" redW")
        self.tarifs_name = []
        # = 0
        for i in self.all_tarif:

            if i[1] != 'Выбирете новый тариф':
                print(i[1])
                self.tarifs_name.append(i[1])
        self.combobox_tarif.addItems(self.tarifs_name)

        self.layout.addWidget(self.labels['Tarif'], 5, 0, 1, 1)
        self.layout.addWidget(self.combobox_tarif, 5, 1, 1, 2)

        self.button_info_tarif = QPushButton('Подробнее о тарифах', clicked=self.tarifInfo)
        self.layout.addWidget(self.button_info_tarif, 5, 3, 1, 1)

        self.layout.addWidget(self.labels['Login'], 6, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Login'], 6, 1, 1, 3)

        self.layout.addWidget(self.labels['Password'], 7, 0, 1, 1)
        self.layout.addWidget(self.lineEdits['Password'], 7, 1, 1, 3)

        button_login = QPushButton('Зарегистрироваться', clicked=self.registration)
        self.layout.addWidget(button_login, 8, 3, 1, 1)
        button_registration = QPushButton('Авторизация', clicked=self.openAuthWindow)
        self.layout.addWidget(button_registration, 9, 3, 1, 1)

    def openAuthWindow(self):
        import LoginWindow
        self.AuthWindow = LoginWindow.LoginWindow()
        self.AuthWindow.show()
        self.close()

    def registration(self):
        import dbMan
        import LoginWindow
        array_reg = [''] * 8
        array_reg[0] = self.lineEdits['Name'].text()
        array_reg[1] = self.lineEdits['LastName'].text()
        array_reg[2] = self.lineEdits['Patronymic'].text()
        array_reg[3] = self.lineEdits['Age'].text()
        array_reg[4] = self.lineEdits['PasportData'].text()
        array_reg[5] = self.combobox_tarif.currentText()
        array_reg[6] = self.lineEdits['Login'].text()
        array_reg[7] = self.lineEdits['Password'].text()

        if len(array_reg[4]) != 10:
            self.showDilog("В поле серия и номер паспорта должно быть 10 цифр")
        for i in range(len(array_reg)):
            if array_reg[i] == '':
                self.showDilog("Все ячейки должня быть заполнены")
                break
            elif array_reg[i].isdigit() and (i == 1 or i == 0 or i == 2):
                RegistrationWindow.showDilog(self, "Поля с ФИО не могут быть числом")
                break
            #print(array_reg[i].isalpha())
            if isinstance(array_reg[i], str) and (i == 3 or i == 4):
                RegistrationWindow.showDilog(self, "Поля Возраст, Серия и номер паспорта не могут быть текстом")
                break
            if array_reg[i] != '' and i == len(array_reg) - 1:
                dbMan.addInfoUser(self, array_reg[0], array_reg[1], array_reg[2], array_reg[3], array_reg[4],
                                  array_reg[5], array_reg[6], array_reg[7])

    def tarifInfo(self):
        self.dlg = self.tarifWindow()
        self.dlg.show()

    def showDilog(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Invoker")
        dlg.setText(message)
        dlg.setStyleSheet('''
            color: black
        ''')
        dlg.exec()

    class tarifWindow(Window):
        def __init__(self):

            super().__init__()

            self.window_width, self.window_height = 700, 250
            self.setFixedSize(self.window_width, self.window_height)

            self.tarifId = 1
            self.lastTarifId = dbMan.getLastRowidTarif()
            self.array_info = dbMan.getInfoTarif(self, int(self.tarifId))


            self.label_info = QLabel('Тариф: ' + self.array_info[1] + ' \n'
                                                                      'Интернет: ' + self.array_info[2] + ' Гб\n'
                                                                                                          'Минуты: ' +
                                     self.array_info[3] + ' \n'
                                                          'Смс: ' + self.array_info[4] + '\n'
                                                                                         'Стоимость: ' +
                                     self.array_info[5] + ' рублей в месяц')
            self.label_info.setStyleSheet('font: 20pt;border: 1px solid white;')
            self.layout.addWidget(self.label_info, 0, 0, 1, 1)
            self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.btn_next = QPushButton('Следующий', clicked=self.nextTarif)
            self.layout.addWidget(self.btn_next, 1, 0, 1, 1)

        def nextTarif(self):
            self.tarifId += 1
            if self.tarifId <= self.lastTarifId:
                self.array_info = dbMan.getInfoTarif(self, self.tarifId)
                if self.array_info[1] != 'Выбирете новый тариф':
                    self.label_info.setText('Тариф: ' + self.array_info[1] + ' \n'
                                                                             'Интернет: ' + self.array_info[2] + ' Гб\n'
                                                                                                                 'Минуты: ' +
                                            self.array_info[3] + ' \n'
                                                                 'Смс: ' + self.array_info[4] + '\n'
                                                                                                'Стоимость: ' +
                                            self.array_info[5] + ' рублей в месяц')
                elif self.tarifId < self.lastTarifId:
                    self.tarifId += 1
                    self.array_info = dbMan.getInfoTarif(self, self.tarifId)
                    self.label_info.setText('Тариф: ' + self.array_info[1] + ' \n'
                                                                             'Интернет: ' + self.array_info[
                                                2] + ' Гб\n'
                                                     'Минуты: ' +
                                            self.array_info[3] + ' \n'
                                                                 'Смс: ' + self.array_info[4] + '\n'
                                                                                                'Стоимость: ' +
                                            self.array_info[5] + ' рублей в месяц')
                else:
                    self.tarifId = 1
                    self.array_info = dbMan.getInfoTarif(self, self.tarifId)
                    self.label_info.setText('Тариф: ' + self.array_info[1] + ' \n'
                                                                             'Интернет: ' + self.array_info[2] + ' Гб\n'
                                                                                                                 'Минуты: ' +
                                            self.array_info[3] + ' \n'
                                                                 'Смс: ' + self.array_info[4] + '\n'
                                                                                                'Стоимость: ' +
                                            self.array_info[5] + ' рублей в месяц')

            elif self:
                self.tarifId = 1
                self.array_info = dbMan.getInfoTarif(self, self.tarifId)
                self.label_info.setText('Тариф: ' + self.array_info[1] + ' \n'
                                                                         'Интернет: ' + self.array_info[2] + ' Гб\n'
                                                                                                             'Минуты: ' +
                                        self.array_info[3] + ' \n'
                                                             'Смс: ' + self.array_info[4] + '\n'
                                                                                            'Стоимость: ' +
                                        self.array_info[5] + ' рублей в месяц')
