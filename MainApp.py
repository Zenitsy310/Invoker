import random
from datetime import date

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import *
import threading
import time
import LoginWindow
import dbMan

from Window import Window


# 7 - Login
# 8 - password
class MainApp(Window):

    def __init__(self, user_info):
        super().__init__()

        self.labels = {}
        self.lineEdits = {}
        self.setFixedSize(900,600)

        self.array_user_data = user_info

        self.array_tarif_info = dbMan.getInfoTarif(self, self.array_user_data[5])
        self.tarifs_name_all = dbMan.getAllTarifNames(self)
        self.tarifs_name = []

        for i in self.tarifs_name_all:
            if i != 'Выбирете новый тариф':
                self.tarifs_name.append(i)

        self.labels['PhoneNumber'] = QLabel('')#,alignment=Qt.AlignmentFlag.AlignCenter
        #self.labels['PhoneNumber'].setStyleSheet("")
        self.labels['Balans'] = QLabel('')#,alignment=Qt.AlignmentFlag.AlignCenter
        self.WidgetUpdate(self.array_user_data[0])
        self.layout.addWidget(self.labels['PhoneNumber'], 0, 0, alignment=Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.labels['Balans'], 1, 0)

        self.button_add_balans = QPushButton('Пополнить баланс',
                                             clicked=lambda: [self.showBalansWindow(self.array_user_data[0])])
        self.layout.addWidget(self.button_add_balans, 2, 1)

        button_change_tarif = QPushButton('Сменить тариф', clicked=self.changeTarif)
        self.layout.addWidget(button_change_tarif, 2, 0)
        # passport_data, new_tarif
        new_tar = str(self.getrndTarif(str(self.array_user_data[5])))
        btn_adw = QPushButton('Попробуйте тариф "' + new_tar + '".\n'
                                                               'На выгодных условиях!\n'
                                                               'Со скидкой на плату в месяц',
                              clicked=lambda: [self.changeTarif(),btn_adw.hide()])

        self.layout.addWidget(btn_adw, 0, 1)
        self.btn_exit = QPushButton('Выход', clicked=lambda: self.close())
        self.layout.addWidget(self.btn_exit, 3, 0)
        #btn_adw.setGeometry(50, 50, 200, 250)
        btn_adw.setStyleSheet( '''background-color: grey;
        font-family: times;
        font-size: 22px;
        border: 2px solid white;
        border-radius: 5px;
        padding: 10px 20px;
        color: black;''')

    def getrndTarif(self, name):

        adw_tar = []

        for i in self.tarifs_name:

            if i.lower() != name.lower() and i != 'Выбирете новый тариф':
                adw_tar.append(i)

        rndName = random.randint(0, len(adw_tar)-1)
        nw_rf = dbMan.getInfoTarif(self, adw_tar[rndName])
        return str(nw_rf[1])

    def WidgetUpdate(self, pas):
        self.array_user_data = dbMan.getUserInfo(pas)
        self.array_tarif_info = dbMan.getInfoTarif(self, self.array_user_data[5])

        self.labels['PhoneNumber'].setText('Ваш номер телефона: ' + str(self.array_user_data[6]) + '\n Сегодня: '
                                            + str(date.today()) + ".")
        # self.labels['PhoneNumber'].setStyleSheet("")
        self.labels['Balans'].setText('Баланс: ' + str(self.array_user_data[9]) + 'р\n'
                                                                                   'Тариф: ' + str(
            self.array_user_data[5]) + '\n'
                                       'Интернет: ' + str(self.array_tarif_info[2]) + 'Гб\n'
                                                                                      'Минуты: ' + str(
            self.array_tarif_info[3]) + '\n'
                                        'Cмс: ' + str(self.array_tarif_info[4]) + '\n'
                                                                                  'Стоимость в месяц:' + str(self.array_tarif_info[5]) +'р\n'
                                        'Ваша последняя операция:\n' + str(dbMan.getLastOp(self, self.array_user_data[0])))

    def showBalansWindow(self, passport_data):
        self.balansWindow = Window()
        self.balansWindow.setFixedSize(400, 150)
        self.balansWindow.labelAddBalans = QLabel('Полнить баланс')
        self.balansWindow.layout.addWidget(self.balansWindow.labelAddBalans, 0, 0, 0, 1)
        self.balansWindow.qleAddBalans = QLineEdit()
        self.balansWindow.layout.addWidget(self.balansWindow.qleAddBalans, 1, 0)
        self.balansWindow.btnAdd = QPushButton('Выполнить', clicked=lambda: self.addBalans(passport_data))
        self.balansWindow.layout.addWidget(self.balansWindow.btnAdd, 1, 1)
        self.balansWindow.show()

    def addBalans(self, passport_data):
        dbMan.addBalans(self, self.balansWindow.qleAddBalans.text(), passport_data)
        dbMan.addLastOp(self, 'Пополнение баланса на: '+ str(self.balansWindow.qleAddBalans.text()) +"p.", passport_data)
        LoginWindow.LoginWindow.showDilog(self, "Ваш баланс был успешно пополнен")
        self.WidgetUpdate(passport_data)
        self.balansWindow.close()

    def changeTarif(self):
        from RegistrationWindow import RegistrationWindow
        self.tarifWindow = Window()
        self.tarifWindow.setFixedSize(450, 150)
        self.tarifWindow.labelCnageTarif = QLabel('Выбирете новый желаемый тариф')
        self.tarifWindow.layout.addWidget(self.tarifWindow.labelCnageTarif, 0, 0, 1, 0)
        self.tarifWindow.tarifs_name = self.tarifs_name

        self.tarifWindow.combobox_tarif = QComboBox()

        self.tarifWindow.combobox_tarif.addItems(self.tarifWindow.tarifs_name)

        self.tarifWindow.layout.addWidget(self.tarifWindow.combobox_tarif, 1, 0)

        self.tarifWindow.btn_change_tarif = QPushButton('Подтвердить', clicked=lambda: [dbMan.addLastOp(self,'Смена тарифа c ' + str(self.array_user_data[5]),self.array_user_data[0]),
            dbMan.updateUsersTarif(self, self.array_user_data[0], self.tarifWindow.combobox_tarif.currentText()),
            self.WidgetUpdate(self.array_user_data[0]), self.tarifWindow.close()])

        self.tarifWindow.layout.addWidget(self.tarifWindow.btn_change_tarif, 1, 1)
        self.tarifWindow.btn_tarif_info = QPushButton('Подробнее о тарифах', clicked=self.tarifInfo)
        self.tarifWindow.layout.addWidget(self.tarifWindow.btn_tarif_info, 2, 1)
        self.tarifWindow.show()

    def tarifInfo(self):
        self.dlg = self.tarifMoreWindow()
        self.dlg.show()

    class tarifMoreWindow(Window):
        def __init__(self):

            super().__init__()

            self.window_width, self.window_height = 700, 250
            self.setFixedSize(self.window_width, self.window_height)

            self.tarifId = 1
            self.lastTarifId = dbMan.getLastRowidTarif()
            self.array_info = dbMan.getInfoTarif(self, self.tarifId)

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
                                                                         'Интернет: ' + self.array_info[2] + ' Гб\n'
                                                                                                             'Минуты: ' +
                                        self.array_info[3] + ' \n'
                                                             'Смс: ' + self.array_info[4] + '\n'
                                                                                            'Стоимость: ' +
                                        self.array_info[5] + ' рублей в месяц')