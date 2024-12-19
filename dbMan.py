import random
import sqlite3
from datetime import date

import LoginWindow
import RegistrationWindow

global db

arr_all_tars = []
def startAppInvoker():
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Tarif  (
                              'Tarif_id' INTEGER,
                              'Name' text(50) NOT NULL PRIMARY KEY,
                              'Ithernet' text(50) NOT NULL,
                              'Minets' text(50) NOT NULL,
                              'Sms' VARCHAR(12) NOT NULL,
                              'Cost' varchar(30) NOT NULL,
                              'Additional_services' varchar(50) NOT NULL
                            )""")

        #cursor.execute('''INSERT INTO Tarif ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('1', 'Выгодный', '30', '200', '100', '350', '-');''')

        cursor.execute(""" CREATE TABLE IF NOT EXISTS "Users" (
              "Passport_data" int(10) NOT NULL PRIMARY KEY,
              "First_name" text(50) NOT NULL,
              "Last_name" text (50)NOT NULL,
              "Patronymic" text(50) NOT NULL,
              "Age" int(11) NOT NULL,
              "Current_tarif" TEXT(50),
              "Phone_number" VARCHAR(12),
              "Login" varchar(30) UNIQUE NOT NULL,
              "Password" varchar(30) NOT NULL,
              "Balans" int(11),
              "Root" TINYINT,
              "Last_op" Text(100),
    		  FOREIGN KEY ("Current_tarif") REFERENCES"Tarif"("Name")
            ) 
            """)
        cursor.execute('''CREATE TABLE IF NOT EXISTS "History" (
                "id"	INTEGER,
                "Type"	TEXT,
                "Date"	TEXT,
                "AfterAct"	TEXT,
                "AdminLog"	VARCHAR(30),
                PRIMARY KEY("id" AUTOINCREMENT),
				FOREIGN KEY ("AdminLog") REFERENCES"Users"("Login")
            );''')

        db.commit()


'''
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('2324654545', 'Oleg', 'Markelov', 'Andreevich', '19', 'Выгодный', '79619341653', 'kokushibo', 'oleg75270', '822', '0');
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('2006180119', 'ILia', 'Kulagin', 'Alekseevich', '19', 'Выгодный', '88880002314', 'r891', 'r891', '500', '0');
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('1234567890', 'admin', 'adminov', 'adminovich', '18', 'Выберете новый тариф', '89998881122', 'admin', 'admin', '100', '1');
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('1234509812', 'влад', 'кругов', 'андреевич', '24', 'Всегда на связи', '89990002314', 'gamerVlad', 'vald1234', '100', '0');
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('1987789012', 'Abobus', 'Abobusov', 'Abobusovich', '41', 'Всегда на связи', '88880002314', 'Wr1ter', 'writer2000', '2341', '0');
INSERT INTO "Users" ("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login", "Password", "Balans", "Root") VALUES ('6002310837', 'Pavel', 'Korchagin', 'userovich', '37', 'Безлимитище', '88880002314', 'KorAndChaga', 'qwe123zxc', '338', '0');

INSERT INTO "Tarif" ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('1', 'Выгодный', '30', '200', '100', '350', '-');
INSERT INTO "Tarif" ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('2', 'ГиГи', '45', '100', '100', '400', '-');
INSERT INTO "Tarif" ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('3', 'Всегда на связи', '20', '300', '300', '400', '-');
INSERT INTO "Tarif" ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('4', 'Безлимитище', '100', '100', '100', '1000', '-');
INSERT INTO "Tarif" ("Tarif_id", "Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") VALUES ('5', 'Выберете новый тариф, прошлый был удален мобильным оператором', '0', '0', '0', '0', '-');
 '''


def auth(self, login, password):
    with sqlite3.connect('Invoker.db') as db:

        cursor = db.cursor()
        try:
            res = cursor.execute('''SELECT * FROM Users WHERE login =  (?) AND password = (?)''',
                                 (login, password)).fetchone()

            if res != None and login == res[7] and password == res[8]:
                if res[10] == 1:
                    LoginWindow.LoginWindow.showDilog(self, 'Вы зашли от имени администратора')
                    LoginWindow.LoginWindow.openAdminWindow(self, res)
                else:
                    LoginWindow.LoginWindow.showDilog(self, 'Вы зашли в личный кабинет')
                    LoginWindow.LoginWindow.openMainWindow(self, res)
            else:
                LoginWindow.LoginWindow.showDilog(self, 'Неверный логин или пароль')
        finally:
            db.commit()


def addInfoUser(self, Name, LastName, Patronymic, Age, PasportData, Tarif, Login, Password):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute(''' INSERT INTO "Users"('Passport_data', 'First_name', 'Last_name', 'Patronymic', 'Age', 'Current_tarif','Phone_number','Login', 'Password', 'Balans', 'Root')  
            VALUES (?,?,?,?,?,?,?,?,?,0,0) ''',
                           (PasportData, Name, LastName, Patronymic, Age, Tarif,
                            str(random.randint(80000000000, 89999999999)), Login,
                            Password))
            res = cursor.execute('''SELECT * FROM Users WHERE login =  (?) AND password = (?)''',
                                 (Login, Password)).fetchone()

            LoginWindow.LoginWindow.showDilog(self, 'Вы завершили регистрацию, добро пожаловать в личный кабинет!')
            LoginWindow.LoginWindow.openMainWindow(self, res)
        except:
            LoginWindow.LoginWindow.showDilog(self, "Ошибка.Проверьте правильность заполнения данных --")
        finally:
            db.commit()


def addNewUserFromAdminWindow(self, passport_data, First_name, Last_name, Patronymic, Age, Current_tarif, Phone_number,
                              Login,
                              Password, Balans, Root):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute('''INSERT INTO"Users"("Passport_data", "First_name", "Last_name", "Patronymic", "Age", "Current_tarif", "Phone_number", "Login",
            "Password", "Balans", "Root" ,"Last_op") VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,-)''', (
                passport_data, First_name, Last_name, Patronymic, str(Age), str(Current_tarif), str(Phone_number),
                str(Login), str(Password), str(Balans), str(Root)))
            RegistrationWindow.RegistrationWindow.showDilog(self, 'Вы завершили регистрацию пользователя')
        except:
            LoginWindow.LoginWindow.showDilog(self, "Ошибка.Проверьте правильность заполнения данных")
        finally:
            db.commit()

def updateUserFromAdminWindow(self, passport_data, First_name, Last_name, Patronymic, Age, Current_tarif, Phone_number,
                              Login,
                              Password, Balans, Root):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            executeU = '''UPDATE "Users" SET "Passport_data" = '{}', "First_name" = '{}', "Last_name" = '{}', "Patronymic" = '{}' ,
             "Age" = '{}', "Current_tarif" = '{}' , "Phone_number" = '{}',  "Login" = '{}',
               "Password" = '{}', "Balans" = '{}', "Root" = '{}' WHERE "Passport_data" = '{}' '''.format(passport_data,
                                                                                                         First_name,
                                                                                                         Last_name,
                                                                                                         Patronymic,
                                                                                                         str(Age),
                                                                                                         str(Current_tarif),
                                                                                                         str(Phone_number),
                                                                                                         str(Password),
                                                                                                         str(Login),
                                                                                                         str(Balans),
                                                                                                         str(Root),
                                                                                                         passport_data)
            cursor.execute(executeU)

            RegistrationWindow.RegistrationWindow.showDilog(self, 'Вы завершили обновление данных пользователя')
        except sqlite3.Error as er:
            LoginWindow.LoginWindow.showDilog(self, "Ошибка.Проверьте правильность заполнения данных")
        finally:
            # cursor.close()
            db.commit()


def addNewInfoHistory(self, Type,AfterAct, AdminLog):
    Date = date.today()
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute('''INSERT INTO "History" (Type,Date,AfterAct,AdminLog) VALUES (?,?,?,?)''',
                           (Type, str(Date), str(AfterAct), str(AdminLog[7])))
        except:
            pass
        finally:
            db.commit()
def addNewTarifFromAdminWindow(self, Name, Ithernet, Minets, Sms, Cost, Additional_services):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        self.id_tarif = int(getLastRowidTarif()) + 1
        try:
            cursor.execute('''INSERT INTO"Tarif"( "Tarif_id","Name", "Ithernet", "Minets", "Sms", "Cost", "Additional_services") 
            VALUES(?,?, ?, ?, ?, ?, ?)''', (
                str(self.id_tarif), str(Name), str(Ithernet), str(Minets), str(Sms), str(Cost),
                str(Additional_services)))
            RegistrationWindow.RegistrationWindow.showDilog(self, 'Вы завершили добавление нового тарифа')

        except:
            LoginWindow.LoginWindow.showDilog(self, "Ошибка.Проверьте правильность заполнения данных")
        finally:
            db.commit()


def updateTarifFromAdminWindow(self, Tarif_id, Name, Ithernet, Minets, Sms, Cost, Additional_services):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()

        try:
            executeU = '''UPDATE "Tarif" SET "Tarif_id" = '{}', "Name" = '{}', "Ithernet" = '{}', "Minets" = '{}' ,
                         "Sms" = '{}', "Cost" = '{}' , "Additional_services" = '{}' WHERE "Tarif_id" = '{}' '''.format(
                str(Tarif_id), str(Name), str(Ithernet), str(Minets),
                str(Sms), str(Cost), str(Additional_services))

            cursor.execute(executeU)

            RegistrationWindow.RegistrationWindow.showDilog(self, 'Вы завершили обновление данных тарифа ' + str(Name))
        except:
            LoginWindow.LoginWindow.showDilog(self, "Ошибка.Проверьте правильность заполнения данных")
        finally:
            db.commit()


def getUserInfo(PasportData):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            return cursor.execute(
                '''SELECT * FROM Users WHERE Passport_data = (''' + str(PasportData) + ''')''').fetchone()
        except:
            pass
        finally:
            cursor.close()


def updateUsersTarif(self, passport_data, new_tarif):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute('''UPDATE "Users" SET "Current_tarif" = (?) WHERE "Passport_data" = (?)''',
                           (new_tarif, passport_data,))
            LoginWindow.LoginWindow.showDilog(self, 'Операция прошла успешно')
        except:
            pass
        finally:
            #cursor.close()
            db.commit()

def getLastRowidTarif():
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            return cursor.execute('''SELECT * FROM Tarif ORDER BY Tarif_id DESC LIMIT 1''').fetchone()[0]

        except:
            # LoginWindow.LoginWindow.showDilog(self, "Ошибка в запросе SQl")
            pass

def getAllTarifNames(self):
    global arr_all_tars
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            #array_all_users_name = [''] * getLastRowidTarif()
            for i in range(getLastRowidTarif()):

                if i == 0:
                    arr_all_tars.append(cursor.execute('''SELECT Name FROM Tarif WHERE Tarif_id = 1 ''').fetchone()[0])
                else:
                    arr_all_tars.append(cursor.execute('''SELECT Name FROM Tarif WHERE Tarif_id = (?) ''', (i + 1,)).fetchone()[0])

            return arr_all_tars
        except:

            pass



def getAllHistory(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        return cursor.execute('''SELECT * FROM "History"''').fetchall()


def getAllUsers(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            return cursor.execute('''SELECT * FROM Users''').fetchall()
        except:
            pass
        finally:

            db.commit()
def getAllTarif(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()

        try:
            return cursor.execute('''SELECT * FROM Tarif''').fetchall()

        except:
            pass
        finally:
            db.commit()


def getRawsUsers(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            return cursor.execute('SELECT COUNT(*) FROM "users" ').fetchone()[0]
        except:
            pass
        finally:
            db.commit()


def getInfoTarif(self, id):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()

        try:
            if str(id).isdigit():
                res = cursor.execute('''SELECT * FROM "Tarif" WHERE "Tarif_id" =  "''' + str(id) + '''"''').fetchone()
            else:
                res = cursor.execute('''SELECT * FROM "Tarif" WHERE "Name" =  "''' + str(id) + '''"''').fetchone()

            return res

        except:
            # LoginWindow.LoginWindow.showDilog(self, "Ошибка в запросе SQl")
            pass
        finally:
            db.commit()


# последняя страка в таблице tarif


def addBalans(self, summ, paasport_data):
    from MainApp import MainApp

    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:

            cursor.execute('''UPDATE "Users" SET "Balans" = "Balans"+(?) WHERE "Passport_data" = (?)''',
                           (int(summ), paasport_data,))
            res = cursor.execute('''SELECT * FROM Users WHERE Passport_data =  (?)''',
                                 (int(paasport_data),)).fetchone()

            MainApp.WidgetUpdate(self, res)
        except:
            pass
        finally:
            db.commit()


def deleteUserFromAdminWindow(self, data, choose_atr):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            if choose_atr == 0:
                cursor.execute('''DELETE FROM "Users" WHERE "Passport_data" = (''' + str(data) + ''')''')
            else:
                cursor.execute('''DELETE FROM "Users" WHERE "Login" = (''' + str(data) + ''')''')
            LoginWindow.LoginWindow.showDilog('Операция удаления прошла успешно')
        except:
            LoginWindow.LoginWindow.showDilog('Проверьте точность данных, возможно, \n'
                                              'данная запись была уже удалена,\n'
                                              'проверьте в журнале событий.')


def deleteTarifFromAdminWindow(self, tarif_id):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            name_tarif = cursor.execute('''SELECT "Name" FROM "Tarif" WHERE "Tarif_id" = "''' + str(tarif_id) + '''" ''').fetchone()[0]

            cursor.execute('''UPDATE "Users" SET "Current_tarif" = "Выберете новый тариф" WHERE "Current_tarif" = "''' + str(name_tarif) + '''"''')

            cursor.execute('''DELETE FROM "Tarif" WHERE "Tarif_id" = (''' + str(tarif_id) + ''')''')

            LoginWindow.LoginWindow.showDilog(self, 'Тарифа был успешно удален')
        except:
            LoginWindow.LoginWindow.showDilog(self, 'Тарифа с таким id не было найдено, проверьте данные')
        finally:
            db.commit()

def getHistoryFromId(self, id):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            res = cursor.execute('''SELECT * FROM History WHERE id="'''+str(id)+'''"''').fetchone()
            return res
        except:
            LoginWindow.LoginWindow.showDilog(self,'Заипси с таким id не было найдено, проверьте данные')

def getStatsTarif(self,names):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            counts = []
            for i in names:
                counts.append(int(cursor.execute('''SELECT COUNT(*) FROM Users WHERE Current_tarif = "''' + str(i) + '''" ''').fetchone()[0]))

            return counts
        except:
            LoginWindow.LoginWindow.showDilog(self, 'Заипси с таким id не было найдено, проверьте данные')

def getAvAge(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            #ages = [20, 35, 60]
            am_people = [] ;
            #for i in ages:
            am_people.append(int(cursor.execute('''SELECT COUNT(*) FROM Users WHERE Age < 25 ''').fetchone()[0]))
            am_people.append(int(cursor.execute('''SELECT COUNT(*) FROM Users WHERE Age > 25 ''').fetchone()[0]))
            am_people.append(int(cursor.execute('''SELECT COUNT(*) FROM Users WHERE Age > 50 ''').fetchone()[0])- am_people[1])
            if am_people[2] < 0: am_people[2] *= -1

            return am_people
        except:
            pass


def getAvgAtr(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        avg_atr = []
        try: #"Ithernet", "Minets", "Sms", "Cost",
            avg_atr.append(cursor.execute('''SELECT AVG(Ithernet) FROM Tarif;''').fetchone()[0])
            avg_atr.append(cursor.execute('''SELECT AVG(Minets) FROM Tarif;''').fetchone()[0])
            avg_atr.append(cursor.execute('''SELECT AVG(Sms) FROM Tarif;''').fetchone()[0])
            avg_atr.append(cursor.execute('''SELECT AVG(Cost) FROM Tarif;''').fetchone()[0])

            return  avg_atr
        except:
            pass
def getCountUser(self):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            res = cursor.execute('''SELECT COUNT(*) FROM Users''').fetchone()[0]

            return res
        except:
            pass
def addLastOp(self, last_op, passport):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            cursor.execute('''UPDATE "Users" SET "Last_op" = "'''+last_op+'''" WHERE Passport_data ="'''+ str(passport)+'''";''')
        except:
            pass
        finally:
            db.commit()

def getLastOp(self,passport):
    with sqlite3.connect('Invoker.db') as db:
        cursor = db.cursor()
        try:
            res = cursor.execute('''Select "Last_op" FROM "Users" WHERE Passport_data ="''' + str(passport) + '''";''').fetchone()[0]
            #print(res)
            return res
        except:
            pass