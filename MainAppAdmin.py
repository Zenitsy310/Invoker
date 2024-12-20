from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidget, QWidget, QGridLayout, QTabWidget, QTableWidgetItem, QPushButton, QComboBox, \
    QLineEdit, QLabel, QFormLayout, QVBoxLayout, QStackedLayout, QCheckBox
import dbMan
import matplotlib.pyplot as plt
from Window import Window
import pandas as pd

class MainAppAdmin(Window):
    def __init__(self, current_admin):
        super().__init__()
        # print(current_admin)
        self.current_admin = current_admin
        self.array_all_users = dbMan.getAllUsers(self)
        self.array_all_tarif = dbMan.getAllTarif(self)
        self.tarifs_name = []
        for i in self.array_all_tarif:
            if i[1] != 'Выберете новый тариф' and i[1] != '':
                self.tarifs_name.append(i[1])

        #self.array_all_tarif.remove('Выберете новый тариф')

        self.array_all_history = dbMan.getAllHistory(self)
        #self.tarifs_name = dbMan.getAllTarifNames(self)
        self.tabs = QTabWidget(self)
        self.tabs.setStyleSheet('background-color: white;')

        self.tableUsers = QTableWidget(self)
        self.tableUsers.setFixedSize(800, 400)
        self.tableUsers.setColumnCount(12)


        self.tableUsers.setHorizontalHeaderLabels(
            ['Passport_data', 'First_name', 'Last_name', 'Patronymic', 'Age', 'Current_tarif',
             'Phone_number', 'Login', 'Password', 'Balans', 'Root', 'Last_op'])
        self.tableUsers.setStyleSheet('color:black;')

        self.WriteTableUsers()

        self.layout.addWidget(self.tabs, 0, 0, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.tableTarif = QTableWidget(self)
        self.tableTarif.setColumnCount(7)
        self.tableTarif.setColumnWidth(6, 200)
        self.tableTarif.setHorizontalHeaderLabels(
            ['Tarif_id', 'Name', 'Ithernet', 'Minets', 'Sms', 'Cost',
             'Additional_services'])
        self.tableTarif.setStyleSheet('color:black;')

        self.writeTableTarif()

        self.tableHistory = QTableWidget(self)
        self.tableHistory.setColumnCount(5)
        self.tableHistory.setColumnWidth(3, 700)
        self.tableHistory.setColumnWidth(4, 550)
        self.tableHistory.setHorizontalHeaderLabels(['id', 'Type', 'Date',
                                                     'AfterAct',
                                                     'AdminLog'])
        self.tableHistory.setStyleSheet('color:black;')
        self.writeTableHistory()

        self.btn_edit = QPushButton('Редактировать', clicked=self.editTables)
        self.layout.addWidget(self.btn_edit, 2, 1)

        self.btn_analytics = QPushButton('Аналитика', clicked=self.analytic)
        self.layout.addWidget(self.btn_analytics, 2, 0)

        self.btn_exit = QPushButton('Выход', clicked=lambda : self.close())
        self.layout.addWidget(self.btn_exit, 2, 3)

        self.search = QLineEdit('Поиск')
        self.layout.addWidget(self.search, 1, 0)

        btn_exel = QPushButton('Экспорт в экслель', clicked = self.exportToExcel)
        self.layout.addWidget(btn_exel,2,4)
        self.btn_search = QPushButton('Поиск',
                                      clicked=lambda: self.sendSearch())  # clicked=lambda: if    elif self.tabs.currentIndex() == 1   elif self.tabs.currentIndex() == 2 )
        self.layout.addWidget(self.btn_search, 1, 1)

        self.tabs.addTab(self.tableUsers, 'Пользователи')
        self.tabs.addTab(self.tableTarif, 'Тарифы')
        self.tabs.addTab(self.tableHistory, 'История операций')



    def exportToExcel(self):
        try:
            if self.tabs.currentIndex() == 0:
                columnHeaders = []
                # create column header list
                for j in range(self.tableUsers.model().columnCount()):
                    columnHeaders.append(self.tableUsers.horizontalHeaderItem(j).text())
                df = pd.DataFrame(columns=columnHeaders)
                for row in range(self.tableUsers.rowCount()):
                    for col in range(self.tableUsers.columnCount()):
                        df.at[row, columnHeaders[col]] = self.tableUsers.item(row, col).text()
                df.to_excel('Documents/Users.xlsx', index=False)
            elif self.tabs.currentIndex() == 1:
                columnHeaders = []
                # create column header list
                for j in range(self.tableTarif.model().columnCount()):
                    columnHeaders.append(self.tableTarif.horizontalHeaderItem(j).text())
                df = pd.DataFrame(columns=columnHeaders)
                for row in range(self.tableTarif.rowCount()):
                    for col in range(self.tableTarif.columnCount()):
                        df.at[row, columnHeaders[col]] = self.tableTarif.item(row, col).text()
                df.to_excel('Documents/Tatif.xlsx', index=False)
            else:
                columnHeaders = []
                # create column header list
                for j in range(self.tableHistory.model().columnCount()):
                    columnHeaders.append(self.tableHistory.horizontalHeaderItem(j).text())
                df = pd.DataFrame(columns=columnHeaders)
                for row in range(self.tableHistory.rowCount()):
                    for col in range(self.tableHistory.columnCount()):
                        df.at[row, columnHeaders[col]] = self.tableHistory.item(row, col).text()
                df.to_excel('Documents/History.xlsx', index=False)
            self.showDilog('Сохранение прошло успешно')
        except:
            self.showDilog('Файл с таким именем уже существует, переименуйте или удалите прошлый файл')

    def sendSearch(self):
        if self.tabs.currentIndex() == 0:
            self.findName('users')
        elif self.tabs.currentIndex() == 1:
            self.findName('tarif')
        elif self.tabs.currentIndex() == 2:
            self.findName('history')

    def editTables(self):
        if self.tabs.currentIndex() == 0:
            self.setUsersTableWidgetEdit()
        elif self.tabs.currentIndex() == 1:
            self.setTarifTableWidgetEdit()
        else:
            self.setTableHistoryWiget()

    def setUsersTableWidgetEdit(self):

        self.current_user_id = self.tableUsers.currentRow()
        self.hide()
        self.edit_window = Window()

        from RegistrationWindow import RegistrationWindow
        self.edit_window.setWindowTitle('Invoker.Редактирование таблицы Users')

        self.edit_window.pixmap = QPixmap('Images/invok_bg.png')
        self.edit_window.labelbg.setPixmap(self.edit_window.pixmap)

        self.edit_window.labels = {}
        self.edit_window.lineEdits = {}

        self.edit_window.labels['PasportData'] = QLabel('Серия и номер паспорта')
        self.edit_window.labels['Name'] = QLabel('Имя')
        self.edit_window.labels['LastName'] = QLabel('Фамилия')
        self.edit_window.labels['Patronymic'] = QLabel('Отчество')
        self.edit_window.labels['Age'] = QLabel('Возраст')
        self.edit_window.labels['Tarif'] = QLabel('Выберете тариф')
        self.edit_window.labels['Login'] = QLabel('Логин')
        self.edit_window.labels['Password'] = QLabel('Пароль')
        self.edit_window.labels['Phone_number'] = QLabel('Номер телефона')
        self.edit_window.labels['Balans'] = QLabel('Баланс')
        self.edit_window.labels['Root'] = QLabel('Права доступа, 1-админ,0-клиент')

        self.edit_window.lineEdits['Name'] = QLineEdit()
        self.edit_window.lineEdits['LastName'] = QLineEdit()
        self.edit_window.lineEdits['Patronymic'] = QLineEdit()
        self.edit_window.lineEdits['Age'] = QLineEdit()
        self.edit_window.lineEdits['PasportData'] = QLineEdit()
        self.edit_window.lineEdits['Tarif'] = QLineEdit()
        self.edit_window.lineEdits['Login'] = QLineEdit()
        self.edit_window.lineEdits['Password'] = QLineEdit()
        self.edit_window.lineEdits['Phone_number'] = QLineEdit()
        self.edit_window.lineEdits['Balans'] = QLineEdit()
        self.edit_window.lineEdits['Root'] = QLineEdit()

        if self.current_user_id != -1:
            try:
                self.edit_window.lineEdits['Name'].setText(self.array_all_users[self.current_user_id][1])
                self.edit_window.lineEdits['LastName'].setText(self.array_all_users[self.current_user_id][2])
                self.edit_window.lineEdits['Patronymic'].setText(self.array_all_users[self.current_user_id][3])
                self.edit_window.lineEdits['Age'].setText(str(self.array_all_users[self.current_user_id][4]))
                self.edit_window.lineEdits['PasportData'].setText(str(self.array_all_users[self.current_user_id][0]))
                self.edit_window.lineEdits['Tarif'].setText(str(self.array_all_users[self.current_user_id][5]))
                self.edit_window.lineEdits['Login'].setText(str(self.array_all_users[self.current_user_id][7]))
                self.edit_window.lineEdits['Password'].setText(str(self.array_all_users[self.current_user_id][8]))
                self.edit_window.lineEdits['Phone_number'].setText(str(self.array_all_users[self.current_user_id][6]))
                self.edit_window.lineEdits['Balans'].setText(str(self.array_all_users[self.current_user_id][9]))
                self.edit_window.lineEdits['Root'].setText(str(self.array_all_users[self.current_user_id][10]))
            except:
                pass

        self.edit_window.layout.addWidget(self.edit_window.labels['Name'], 0, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Name'], 0, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['LastName'], 1, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['LastName'], 1, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Patronymic'], 2, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Patronymic'], 2, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Age'], 3, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Age'], 3, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['PasportData'], 4, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['PasportData'], 4, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Phone_number'], 5, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Phone_number'], 5, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Login'], 9, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Login'], 9, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Password'], 10, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Password'], 10, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Balans'], 6, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Balans'], 6, 1, 1, 3)

        self.edit_window.combobox_usr_root = QComboBox()
        self.edit_window.combobox_usr_root.addItems(['0', '1'])
        self.edit_window.layout.addWidget(self.edit_window.labels['Root'], 7, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.combobox_usr_root, 7, 1, 1, 3)

        self.edit_window.combobox_tarif = QComboBox()
        #self.edit_window.tarifs_name = dbMan.getAllTarifNames(self)

        self.edit_window.tarifs_name = []
        # = 0
        for i in self.array_all_tarif:
            #print(i[1])
            if i[1] != 'Выберете новый тариф' and i[1] != '':
                self.edit_window.tarifs_name.append(i[1])

        #print(str(self.edit_window.tarifs_name) + ' 186')

        self.edit_window.combobox_tarif.addItems(self.edit_window.tarifs_name)

        self.edit_window.layout.addWidget(self.edit_window.labels['Tarif'], 8, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.combobox_tarif, 8, 1, 1, 3)
        #print(str(self.current_user_id) + ' users' )
        if self.current_user_id == -1:
            self.edit_window.btn_add_info_user = QPushButton('Добавить', clicked=lambda: self.addUserText('insert'))
            self.edit_window.layout.addWidget(self.edit_window.btn_add_info_user, 12, 1, 1, 1)

        self.edit_window.btn_upd_info_user = QPushButton('Обновить', clicked=lambda: self.addUserText('update'))
        self.edit_window.layout.addWidget(self.edit_window.btn_upd_info_user, 12, 2, 1, 1)

        self.edit_window.btn_del_user = QPushButton('Удалить', clicked=lambda: self.addUserText('delete'))
        self.edit_window.layout.addWidget(self.edit_window.btn_del_user, 12, 3, 1, 1)

        self.edit_window.btn_set_tarif_widgets = QPushButton('Тарифы', clicked=self.setTarifTableWidgetEdit)
        self.edit_window.layout.addWidget(self.edit_window.btn_set_tarif_widgets, 12, 0, 1, 1)

        self.edit_window.btn_back_main_window = QPushButton('К Главному окну',
                                                            clicked=lambda: [self.show(), self.updateData(),
                                                                             self.edit_window.close()])
        self.edit_window.layout.addWidget(self.edit_window.btn_back_main_window, 13, 0, 1, 1)

        self.edit_window.show()

    def addUserText(self, action):

        # self.before_reg = self.array_all_users[int(self.edit_window.lineEdits['PasportData'].text()) - 1]
        array_reg = [''] * 11
        array_reg[0] = self.edit_window.lineEdits['PasportData'].text()
        array_reg[1] = self.edit_window.lineEdits['Name'].text()
        array_reg[2] = self.edit_window.lineEdits['LastName'].text()
        array_reg[3] = self.edit_window.lineEdits['Patronymic'].text()
        array_reg[4] = self.edit_window.lineEdits['Age'].text()
        array_reg[5] = self.edit_window.combobox_tarif.currentText()
        array_reg[6] = self.edit_window.lineEdits['Phone_number'].text()
        array_reg[7] = self.edit_window.lineEdits['Login'].text()
        array_reg[8] = self.edit_window.lineEdits['Password'].text()
        array_reg[9] = self.edit_window.lineEdits['Balans'].text()
        array_reg[10] = self.edit_window.combobox_usr_root.currentText()

        for i in range(len(array_reg)):
            if (action == 'delete' and array_reg[0] != '') or (action == 'delete' and array_reg[7] != ''):
                if array_reg[0] != '':
                    dbMan.deleteUserFromAdminWindow(self, array_reg[0], 0)

                else:
                    dbMan.deleteUserFromAdminWindow(self, array_reg[7], 1)
                dbMan.addNewInfoHistory(self, 'delete', array_reg, self.current_admin)
            elif array_reg[i] == '':
                self.showDilog("Все ячейки должня быть заполнены")
                break
            elif array_reg[i] != '' and i == len(array_reg) - 1 and action == 'insert':
                dbMan.addNewUserFromAdminWindow(self, array_reg[0], array_reg[1], array_reg[2], array_reg[3],
                                                array_reg[4],
                                                array_reg[5], array_reg[6], array_reg[7], array_reg[8], array_reg[9],
                                                array_reg[10])
                dbMan.addNewInfoHistory(self, 'insert', array_reg, self.current_admin)
            elif array_reg[i] != '' and i == len(array_reg) - 1 and action == 'update':
                dbMan.updateUserFromAdminWindow(self, array_reg[0], array_reg[1], array_reg[2], array_reg[3],
                                                array_reg[4],
                                                array_reg[5], array_reg[6], array_reg[7], array_reg[8], array_reg[9],
                                                array_reg[10])
                dbMan.addNewInfoHistory(self, 'update', array_reg, self.current_admin)

    def setTarifTableWidgetEdit(self):
        self.current_tarif_id = self.tableTarif.currentRow()
        self.hide()
        self.edit_window = Window()
        self.edit_window.setWindowTitle('Invoker.Редактирование таблицы Tarif')

        self.edit_window.labels = {}
        self.edit_window.lineEdits = {}

        self.edit_window.labels['Tarif_id'] = QLabel('id тарифа \n(не нужен при добавлении нового тарифа)')
        self.edit_window.labels['Name'] = QLabel('Название тарифа')
        self.edit_window.labels['Ithernet'] = QLabel('Количество Гб интернета')
        self.edit_window.labels['Minets'] = QLabel('Количество минут')
        self.edit_window.labels['Sms'] = QLabel('Количество смс')
        self.edit_window.labels['Cost'] = QLabel('Стоимость в месяц')
        self.edit_window.labels['Additional_services'] = QLabel('Дополнительные услуги')

        self.edit_window.lineEdits['Tarif_id'] = QLineEdit()
        self.edit_window.lineEdits['Name'] = QLineEdit()
        self.edit_window.lineEdits['Ithernet'] = QLineEdit()
        self.edit_window.lineEdits['Minets'] = QLineEdit()
        self.edit_window.lineEdits['Sms'] = QLineEdit()
        self.edit_window.lineEdits['Cost'] = QLineEdit()
        self.edit_window.lineEdits['Additional_services'] = QLineEdit()

        if self.current_tarif_id != -1:
            print(str(self.array_all_tarif[self.current_tarif_id][0]))
            self.edit_window.lineEdits['Tarif_id'].setText(str(self.array_all_tarif[self.current_tarif_id][0]))
            self.edit_window.lineEdits['Name'].setText(str(self.array_all_tarif[self.current_tarif_id][1]))
            self.edit_window.lineEdits['Ithernet'].setText(str(self.array_all_tarif[self.current_tarif_id][2]))
            self.edit_window.lineEdits['Minets'].setText(str(self.array_all_tarif[self.current_tarif_id][3]))
            self.edit_window.lineEdits['Sms'].setText(str(self.array_all_tarif[self.current_tarif_id][4]))
            self.edit_window.lineEdits['Cost'].setText(str(self.array_all_tarif[self.current_tarif_id][5]))
            self.edit_window.lineEdits['Additional_services'].setText(
                str(self.array_all_tarif[self.current_tarif_id][6]))


        self.edit_window.layout.addWidget(self.edit_window.labels['Tarif_id'], 0, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Tarif_id'], 0, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Name'], 1, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Name'], 1, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Ithernet'], 2, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Ithernet'], 2, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Minets'], 3, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Minets'], 3, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Sms'], 4, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Sms'], 4, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Cost'], 5, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Cost'], 5, 1, 1, 3)

        self.edit_window.layout.addWidget(self.edit_window.labels['Additional_services'], 6, 0, 1, 1)
        self.edit_window.layout.addWidget(self.edit_window.lineEdits['Additional_services'], 6, 1, 1, 3)

        self.edit_window.btn_set_tarif_widgets = QPushButton('Пользователи', clicked=self.setUsersTableWidgetEdit)
        self.edit_window.layout.addWidget(self.edit_window.btn_set_tarif_widgets, 9, 3, 1, 1)

        #print(str (self.current_tarif_id) + 'tarif')
        if self.current_tarif_id == -1:
            self.edit_window.btn_add_info_user = QPushButton('Добавить', clicked=lambda: self.addTarifText('insert'))
            self.edit_window.layout.addWidget(self.edit_window.btn_add_info_user, 10, 1, 1, 1)

        self.edit_window.btn_upd_info_user = QPushButton('Обновить', clicked=lambda: self.addTarifText('update'))
        self.edit_window.layout.addWidget(self.edit_window.btn_upd_info_user, 10, 2, 1, 1)


        self.edit_window.btn_del_user = QPushButton('Удалить', clicked=lambda: self.addTarifText('delete'))
        self.edit_window.layout.addWidget(self.edit_window.btn_del_user, 10, 3, 1, 1)

        self.edit_window.btn_back_main_window = QPushButton('К Главному окну',
                                                            clicked=lambda: [self.show(), self.updateData(),
                                                                             self.edit_window.close()])
        self.edit_window.layout.addWidget(self.edit_window.btn_back_main_window, 13, 0, 1, 1)
        self.edit_window.show()

    def addTarifText(self, action):
        array_reg = [''] * 7

        array_reg[0] = self.edit_window.lineEdits['Tarif_id'].text()
        array_reg[1] = self.edit_window.lineEdits['Name'].text()
        array_reg[2] = self.edit_window.lineEdits['Ithernet'].text()
        array_reg[3] = self.edit_window.lineEdits['Minets'].text()
        array_reg[4] = self.edit_window.lineEdits['Sms'].text()
        array_reg[5] = self.edit_window.lineEdits['Cost'].text()
        array_reg[6] = self.edit_window.lineEdits['Additional_services'].text()

        for i in range(len(array_reg)):
            if action == 'delete' and array_reg[0] != '':
                dbMan.addNewInfoHistory(self, 'delete',str(array_reg), self.current_admin[0])
                dbMan.deleteTarifFromAdminWindow(self, array_reg[0])
                break

            elif i != 0 :
                if array_reg[i] == '':
                    self.showDilog("Все ячейки должня быть заполнены")
                    break
                elif array_reg[i].isdigit() and (i == 1, 6):
                    self.showDilog("Поля Дополнительные услуги и Название тарифа, не должны быть числами")
                    break
                else:
                    self.showDilog("Поля Интернет, Минуты, Смс, Дополнительные услуги должны содержать только числа")
                    break

            elif array_reg[i] != '' and i == len(array_reg) - 1 and action == 'insert':
                dbMan.addNewTarifFromAdminWindow(self, array_reg[1], array_reg[2], array_reg[3],
                                                 array_reg[4],
                                                 array_reg[5], array_reg[6])
                dbMan.addNewInfoHistory(self, 'insert', str(array_reg), self.current_admin[0])
            elif array_reg[i] != '' and i == len(array_reg) - 1 and action == 'update':
                dbMan.updateTarifFromAdminWindow(self, array_reg[0], array_reg[1], array_reg[2], array_reg[3],
                                                 array_reg[4],
                                                 array_reg[5], array_reg[6])
                dbMan.addNewInfoHistory(self, 'update', str(array_reg), self.current_admin[0])

    def setTableHistoryWiget(self):
        self.current_history_id = self.tableUsers.currentRow()
        self.hide()
        self.history_window = Window()
        self.history_window.setWindowTitle('Invoker.Записи из таблицы Tarif')
        self.current_history = self.array_all_history[self.current_history_id]

        self.history_window.labels = {}
        self.history_window.lineEdits = {}

        self.history_window.labels['id'] = QLabel('id записи:' + str(self.current_history[0]))
        self.history_window.layout.addWidget(self.history_window.labels['id'], 0, 0)

        self.history_window.labels['type'] = QLabel('Тип операции:' + str(self.current_history[1]))
        self.history_window.layout.addWidget(self.history_window.labels['type'], 1, 0)

        self.history_window.labels['date'] = QLabel('Дата операции: ' + str(self.current_history[2]))
        self.history_window.layout.addWidget(self.history_window.labels['date'], 2, 0)


        self.history_window.labels['after_act'] = QLabel('Данные операции: ' + str(self.current_history[3]))
        self.history_window.layout.addWidget(self.history_window.labels['after_act'], 3, 0, 1,2)
        self.history_window.labels['after_act'].setStyleSheet('''font-size: 16px;''')

        self.history_window.labels['admin_log'] = QLabel(
            'Данные админ-а , кто совершил операцию: ' + str(self.current_history[4]))
        self.history_window.labels['admin_log'].setStyleSheet('''font-size: 16px;''')
        self.history_window.layout.addWidget(self.history_window.labels['admin_log'], 4, 0, 1, 2)

        self.history_window.search_hr = QLineEdit('Поиск по id')
        self.history_window.layout.addWidget(self.history_window.search_hr, 5, 0)

        self.history_window.btn_search_history = QPushButton('Выполнить', clicked=lambda: self.findHistory(self.history_window.search_hr.text()))
        self.history_window.layout.addWidget(self.history_window.btn_search_history,5,1)

        self.history_window.btn_back_main_window = QPushButton('К Главному окну',
                                                            clicked=lambda: [self.show(), self.updateData(),
                                                                             self.history_window.close()])
        self.history_window.layout.addWidget(self.history_window.btn_back_main_window, 6, 0, 1, 1)
        self.history_window.show()
    def analytic(self):
        self.hide()
        self.analityc_window = Window()
        self.analityc_window.setFixedSize(600, 600)

        self.analityc_window.pixmap = QPixmap('Images/dark_bg.jpg')
        self.analityc_window.labelbg.setPixmap(self.analityc_window.pixmap)

        self.analityc_window.labelbg.setStyleSheet("background-color:black")
        label_stat = QLabel('Aналитика',alignment=Qt.AlignmentFlag.AlignCenter)
        self.analityc_window.layout.addWidget(label_stat, 0, 0, 1, 2)
        label_stat.setStyleSheet('''font-family: 'Times new Rowan', cursive;
            font-weight: 400;
            color: white;
            font-size: 45px;
            text-align: center;
            position: relative;''')

        label_full_stat = QLabel('Полная статистика',alignment=Qt.AlignmentFlag.AlignCenter)
        self.analityc_window.layout.addWidget(label_full_stat, 1, 0)

        label_short_stat = QLabel('Кратая статистика',alignment=Qt.AlignmentFlag.AlignCenter)
        self.analityc_window.layout.addWidget(label_short_stat, 1, 1)

        label_short_info = QLabel('Зарегистрированных \n' 
                                  'пользователей: '
                                  + str(dbMan.getCountUser(self)))

        self.analityc_window.layout.addWidget(label_short_info, 2, 1)

        btn_av_tr = QPushButton('Использование тарифов', clicked=self.averageTarif)
        self.analityc_window.layout.addWidget(btn_av_tr, 2, 0)

        btn_avg_age = QPushButton('Показатель возрастов', clicked = self.averageUsersAge)
        self.analityc_window.layout.addWidget(btn_avg_age, 3, 0)

        btn_avg_atr = QPushButton('Средние показатели тарифов', clicked=self.avgTarAtr)
        self.analityc_window.layout.addWidget(btn_avg_atr, 4, 0)

        btn_back_main_window = QPushButton('К Главному окну',
                                                            clicked=lambda: [self.show(), self.updateData(),
                                                                             self.analityc_window.close()])
        self.analityc_window.layout.addWidget(btn_back_main_window, 4,1)

        self.analityc_window.show()

    def averageTarif(self):
        fig, ax = plt.subplots()
        tarifs = []
        for i in range(len(self.tarifs_name)):
            if self.tarifs_name[i] != 'Выберете новый тариф' and self.tarifs_name[i] != '':
                tarifs.append(self.tarifs_name[i])

        arr_counts_tar = dbMan.getStatsTarif(self, tarifs)
        bar_labels = []
        for i in tarifs:
            bar_labels.append(i)
        bar_colors = ['tab:red', 'tab:blue', 'tab:pink', 'tab:orange']
        ax.bar(tarifs, arr_counts_tar, label=bar_labels, color=bar_colors)
        ax.set_ylabel('Количество пользователей')
        ax.set_title('Гистограмма использования тарифов')
        ax.legend(title='Тарифы')
        plt.show()

        # Средний возраст пользователь
    def averageUsersAge(self):
        fig, ax = plt.subplots()
        ages = ['До 20', 'от 20 до  50', 'от 50']
        av_ages = dbMan.getAvAge(self)

        bar_labels = ages
        bar_colors = ['tab:blue', 'tab:green', 'tab:orange']

        ax.bar(ages, av_ages, label=bar_labels, color=bar_colors)

        ax.set_ylabel('Возраст')
        ax.set_title('Преобладающие группы возрастов')
        ax.legend(title='Группы возрастов')

        plt.show()

     #всего пользователей
    def countUsers(self):
        pass

    # ср показатель атрибутов тарифа
    def avgTarAtr(self):
        #dbMan.getAvgAtr(self)
        fig, ax = plt.subplots()

        atr = ['Интернет в месяц в Гб','Минуты для звонков в мин', "Количество Смс", "Стоимость в месяц"]
        av_atr = dbMan.getAvgAtr(self)

        bar_labels = atr
        bar_colors = ['tab:blue', 'tab:green', 'tab:orange','tab:pink']

        ax.bar(atr, av_atr, label=bar_labels, color=bar_colors)

        ax.set_ylabel('Показатели')
        ax.set_title('Атрибуты')
        ax.legend(title='Средние показатели атрибутов используемых тарифов')

        plt.show()

    def WriteTableUsers(self):
        self.array_all_users = dbMan.getAllUsers(self)
        self.tableUsers.setRowCount(len(self.array_all_users))
        row = 0
        for i in self.array_all_users:
            self.tableUsers.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.tableUsers.setItem(row, 1, QTableWidgetItem(i[1]))
            self.tableUsers.setItem(row, 2, QTableWidgetItem(i[2]))
            self.tableUsers.setItem(row, 3, QTableWidgetItem(i[3]))
            self.tableUsers.setItem(row, 4, QTableWidgetItem(str(i[4])))
            self.tableUsers.setItem(row, 5, QTableWidgetItem(i[5]))
            self.tableUsers.setItem(row, 6, QTableWidgetItem(str(i[6])))
            self.tableUsers.setItem(row, 7, QTableWidgetItem(i[7]))
            self.tableUsers.setItem(row, 8, QTableWidgetItem(i[8]))
            self.tableUsers.setItem(row, 9, QTableWidgetItem(str(i[9])))
            self.tableUsers.setItem(row, 10, QTableWidgetItem(str(i[10])))
            self.tableUsers.setItem(row, 11, QTableWidgetItem(str(i[11])))
            row += 1

    def writeTableTarif(self):
        #self.array_all_tarif.clear()
        self.array_all_tarif = dbMan.getAllTarif(self)
        self.tableTarif.setRowCount(len(self.array_all_tarif))
        row = 0
        for i in self.array_all_tarif:
            self.tableTarif.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.tableTarif.setItem(row, 1, QTableWidgetItem(str(i[1])))
            self.tableTarif.setItem(row, 2, QTableWidgetItem(str(i[2])))
            self.tableTarif.setItem(row, 3, QTableWidgetItem(str(i[3])))
            self.tableTarif.setItem(row, 4, QTableWidgetItem(str(i[4])))
            self.tableTarif.setItem(row, 5, QTableWidgetItem(str(i[5])))
            self.tableTarif.setItem(row, 6, QTableWidgetItem(str(i[6])))
            row += 1

    def writeTableHistory(self):
        self.array_all_history = dbMan.getAllHistory(self)
        self.tableHistory.setRowCount(len(self.array_all_history))
        row = 0
        for i in self.array_all_history:
            self.tableHistory.setItem(row, 0, QTableWidgetItem(str(i[0])))
            self.tableHistory.setItem(row, 1, QTableWidgetItem(str(i[1])))
            self.tableHistory.setItem(row, 2, QTableWidgetItem(str(i[2])))
            self.tableHistory.setItem(row, 3, QTableWidgetItem(str(i[3])))
            self.tableHistory.setItem(row, 4, QTableWidgetItem(str(i[4])))
            row += 1

    def updateData(self):
        self.tableTarif.clear()
        self.tableUsers.clear()
        self.tableHistory.clear()

        self.tableUsers.setHorizontalHeaderLabels(
            ['Passport_data', 'First_name', 'Last_name', 'Patronymic', 'Age', 'Current_tarif',
             'Phone_number', 'Login', 'Password', 'Balans', 'Root'])
        self.tableTarif.setHorizontalHeaderLabels(
            ['Tarif_id', 'Name', 'Ithernet', 'Minets', 'Sms', 'Cost',
             'Additional_services'])
        self.tableHistory.setHorizontalHeaderLabels(['id', 'Type', 'Date',
                                                     'BeforeAct', 'AfterAct',
                                                     'AdminLog'])

        self.writeTableHistory()
        self.writeTableTarif()
        self.WriteTableUsers()

    def findName(self, table_name):
        name = str(self.search.text().lower())
        if table_name == 'users':
            for row in range(self.tableUsers.rowCount()):
                res = 0
                for col in range(self.tableUsers.columnCount()):
                    item = self.tableUsers.item(row, col)
                    if name in item.text().lower():
                        res += 1
                    self.tableUsers.setRowHidden(row, name not in item.text().lower() and res == 0 and col == 11)
        elif table_name == 'tarif':
            for row in range(self.tableTarif.rowCount()):
                res = 0
                for col in range(self.tableTarif.columnCount()):
                    item = self.tableTarif.item(row, col)
                    if name in item.text().lower():
                        res += 1
                    self.tableTarif.setRowHidden(row, name not in item.text().lower() and res == 0 and col == 6)
        elif table_name == 'history':

            for row in range(self.tableHistory.rowCount()):
                res = 0
                for col in range(self.tableHistory.columnCount()):
                    item = self.tableHistory.item(row, col)
                    if name in item.text().lower():
                        res += 1
                    self.tableHistory.setRowHidden(row, name not in item.text().lower() and res == 0 and col == 4)




    def findHistory(self, id):
        if id.isdigit():
            self.history_window.current_history = dbMan.getHistoryFromId(self, id)
            #(self.history_window.current_history)
            self.history_window.labels['id'].setText('id записи:' + str(self.history_window.current_history[0]))
            self.history_window.labels['type'].setText('Тип операции:' + str(self.history_window.current_history[1]))
            self.history_window.labels['date'].setText('Дата операции: ' + str(self.history_window.current_history[2]))
            self.history_window.labels['after_act'].setText('Данные операции: ' + str(self.history_window.current_history[3]))
            self.history_window.labels['admin_log'] .setText(
                'Данные админ-а , кто совершил операцию: ' + str(self.history_window.current_history[4]))

        else:
            self.showDilog('Введите число, id интересующей вас записи')
