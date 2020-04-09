from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys
from ftplib import FTP
import ftplib
import requests
import time
from datetime import datetime, timezone
import os
import os.path
import zipfile
import pymysql
import urllib
from pymysql.cursors import DictCursor
global path
global file

class SetInit(): # Инициализация настроек
    def __init__(self):
        super().__init__()
        self.pathinit()
        self.download_res()
        self.unzip_res()

    def pathinit(self): # Переход в папку с ресурсами
        global path
        path = os.getenv('APPDATA') + '\\EtMemory'
        try:
            os.mkdir(path)
            print('LOG (OK): Folder with resources has been created')
        except FileExistsError:
            print('LOG (OK): Folder with resources exists')

    def download_res(self): # Скачивание ресурсов программы
        global path
        try:
            os.chdir(path)
            urllib.request.urlretrieve('http://www.etmemory.ru.com/resources.zip', 'resources.zip')
            print('LOG (OK): Resources has been downloaded')
        except:
            print("LOG (ERROR): Resources hasn't been downloaded")
            app = QtWidgets.QApplication([])
            win = Warn2('no err')
            win.ErrorMessage("Error: Internet error.")
            sys.exit(app.exec_())

    def unzip_res(self): # Распаковка ресурсов программы
        global path
        try:
            with zipfile.ZipFile("resources.zip", "r") as zip_ref:
                zip_ref.extractall(path)
            os.remove('resources.zip')
            print("LOG (OK): Resources has been unpacked and installed")
        except:
            print("LOG (ERROR): Resources hasn't been unpacked")

class MySQL(): # Функции для подключения и работы с БД

    def connect(host, username, password, dbname): # Создания подключения к БД
        global connection
        connection = pymysql.connect(host, username, password, dbname, cursorclass=DictCursor, port=3306)

    def check_login(login): # Проверка существования логина в системе
        global connection
        queue = """SELECT * FROM `users` WHERE login = '""" + login + """'""" # SQL запрос
        cursor = connection.cursor()
        cursor.execute(queue) # Выполнение SQL запроса
        ans = cursor.fetchone() # Присваивание ответа от выполнения SQL запроса в переменную ans
        try:
            if login == ans['login']: # Попытка проверить существования логина
                return 0 # Возврат "0", как сигнала, что ошибок нет
        except TypeError:
            return 144 # Возврат "145", как сигнала об ошибке "Логина не существует"

    def check_password(login, password): # Проверка пароля к логину
        global connection
        queue = """SELECT * FROM users WHERE login = '""" + login + """'""" # SQL запрос
        cursor = connection.cursor()
        cursor.execute(queue) # Выполнение SQL запроса
        ans = cursor.fetchone() # Присваивание ответа от выполнения SQL запроса в переменную ans
        try:
            if password == ans['password']: # Проверка пароля к аккаунту
                return 0 # Возврат "0", как сигнала, что ошибок нет
            else:
                return 143 # Возврат "143", как сигнала, что пароль неправильный
        except TypeError:
            return 144 # Возврат "145", как сигнала о непредвиденной ошибке

class Auth(QMainWindow): # Окно авторизации

    def center(self): # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event): # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event): # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self): # Инициализация класса
        super().__init__()
        self.initUI()

    def initUI(self): # Инициализация интерфейса
        def closebtn():
            sys.exit()
        global path
        path = path.replace("\\","/") # Нормализация пути
        uic.loadUi(path + "/etmemory_auth.ui", self) # Загрузка интерфейса из .ui файла
        self.pwd.setEchoMode(QLineEdit.Password) # Замена знаков в поле "Пароль"
        self.setAttribute(Qt.WA_TranslucentBackground, True) # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint) # Удаление рамок окна от ОС
        self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("background-image:url(" + path + "/bg_auth.png);")  # Фон
        self.signin.setStyleSheet("""
                                           QPushButton:!hover { background-image:url(""" + path + """/sign_in.png) }
                                           QPushButton:hover { background-image:url(""" + path + """/sign_in_hover.png) };
                                       """) # Дизайн кнопки "Войти"
        self.reg.setStyleSheet("""
                                           QPushButton:!hover { background-image:url(""" + path + """/register.png) }
                                           QPushButton:hover { background-image:url(""" + path + """/register_hover.png) };
                                       """) # Дизайн кнопки "Регистрация"
        self.closed.setStyleSheet("""
                                                                   QPushButton { border:none; background-image:url(""" + path + """/close.png) }
                                                               """)  # Дизайн кнопки "Закрыть"
        self.login.setStyleSheet("""QLineEdit {
                        border: 1px solid #f26e00;
                        border-radius: 5px;
                        padding: 0 5px;
                        background-image:url(""" + path + """/texture2.png);
                        selection-background-color: darkgray;
                        color: #f3f3f3
                        }
                    """) # Дизайн поля "Логин"

        self.pwd.setStyleSheet("""QLineEdit {
                        border: 1px solid #f26e00;
                        border-radius: 5px;
                        padding: 0 5px;
                        background-image:url(""" + path + """/texture2.png);
                        selection-background-color: darkgray;
                        color: #f3f3f3
                        }
                    """) # Дизайн поля "Пароль"

        self.signin.clicked.connect(self.sign_in) # Передача кнопке "Войти" функции sign_in
        self.reg.clicked.connect(self.register) # Передача кнопке "Регистрация" функции register
        self.closed.clicked.connect(closebtn) # Передача кнопке "Закрыть" задачи закрытия окна

        self.move(QApplication.instance().desktop().screen().rect().center()
                  - self.rect().center()) # Для свободного перемещения окна

    def sign_in(self):
        global connection
        MySQL.connect('37.140.192.116', 'u1001983_mhack', 'T3g3V2s5', 'u1001983_mhack')
        login = self.login.text()
        pwd = self.pwd.text()
        check1 = MySQL.check_login(login)
        if check1 == 0:
            check2 = MySQL.check_password(login, pwd)
            if check2 == 0:
                print('LOG (OK): Successful enter')
                queue = """SELECT * FROM users WHERE login = '""" + login + """'"""
                cursor = connection.cursor()
                cursor.execute(queue)
                ans = cursor.fetchone()
                if ans['role'] == 'noactive':
                    self.win = Warn('Ваш аккаунт ожидает подтверждения: с Вами свяжется модератор через почту, указанную в ходе регистрации.')
                    self.win.show()
                if ans['role'] == 'moderator':
                    self.win = Moderate(login)
                    self.win.show()
                    self.close()

            elif check2 == 143:
                print('LOG (ERROR): Incorrect password')
                self.win = Warn(
                    'Вы ввели неверный пароль. Попробуйте ещё раз!')
                self.win.show()
            elif check2 == 144:
                print('LOG (ERROR): Unexpected error')
                self.win = Warn(
                    'Произошла непредвиденная ошибка!')
                self.win.show()
        else:
            print("LOG (ERROR): User don't exists")
            self.win = Warn(
                'Пользователя не существует!')
            self.win.show()

    def register(self):
        login = self.login.text()
        pwd = self.pwd.text()
        self.win = Register(login, pwd)
        self.win.show()

class Register(QMainWindow): # Окно регистрации

    def center(self):  # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event):  # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self, login, pwd):  # Инициализация класса
        super().__init__()
        self.initUI(login, pwd)

    def initUI(self, login, pwd):
        # Инициализация интерфейса
        def closebtn():
            self.close()

        global path
        path = path.replace("\\", "/")  # Нормализация пути
        uic.loadUi(path + "/etmemory_reg.ui", self)  # Загрузка интерфейса из .ui файла
        self.pwd.setEchoMode(QLineEdit.Password)  # Замена знаков в поле "Пароль"
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint)  # Удаление рамок окна от ОС
        self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("background-image:url(" + path + "/bg_reg.png);")  # Фон
        self.login.setText(login)
        self.pwd.setText(pwd)
        self.confirm.setStyleSheet("""
                                                  QPushButton:!hover { background-image:url(""" + path + """/confirm.png) }
                                                  QPushButton:hover { background-image:url(""" + path + """/confirm_hover.png) };
                                              """)  # Дизайн кнопки "Войти"
        self.cancel.setStyleSheet("""
                                                  QPushButton:!hover { background-image:url(""" + path + """/cancel.png) }
                                                  QPushButton:hover { background-image:url(""" + path + """/cancel_hover.png) };
                                              """)  # Дизайн кнопки "Регистрация"
        self.closed.setStyleSheet("""
                                                           QPushButton { border:none; background-image:url(""" + path + """/close.png) }
                                                       """)  # Дизайн кнопки "Закрыть"
        self.login.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Логин"

        self.pwd.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Пароль"
        self.email.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Эл. почта"

        self.lastname.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Фамилия"
        self.firstname.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Имя"

        self.middlename.setStyleSheet("""QLineEdit {
                                border: 1px solid #2f2f2f;
                                border-radius: 5px;
                                padding: 0 5px;
                                background-image:url(""" + path + """/texture3.png);
                                selection-background-color: darkgray;
                                color: #2f2f2f
                                }
                            """)  # Дизайн поля "Отчество"
        self.confirm.clicked.connect(self.confirmed)
        self.cancel.clicked.connect(self.canceled)
        self.closed.clicked.connect(closebtn)

    def confirmed(self):
        global connection
        MySQL.connect('37.140.192.116', 'u1001983_mhack', 'T3g3V2s5', 'u1001983_mhack')
        flag = 0
        login = self.login.text()
        pwd = self.pwd.text()
        email = self.email.text()
        lastname = self.lastname.text()
        firstname = self.firstname.text()
        middlename = self.middlename.text()
        if (login == '') or (pwd == '') or (email == '') or (lastname == '') or (firstname == '') or (middlename == ''):
            self.win = Warn('Для регистрации необходимо заполнить все поля!')
            self.win.show()
            flag = 1
        if flag == 0:
            check1 = MySQL.check_login(login)
            if check1 == 0:
                self.win = Warn('Пользователь с таким логином уже существует. Попробуйте выбрать другой')
                self.win.show()
                flag = 1
        if flag == 0:
            cursor = connection.cursor()
            queue = """INSERT INTO users (login, password, email, lastname, firstname, middlename, role, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(queue, (login, pwd, email, lastname, firstname, middlename, 'noactive', 'register from app'))
            connection.commit()
            self.win = Warn('Заявка успешно создана. Менеджер с Вами свяжется по указанной электронной почте.')
            self.win.show()
            self.close()
    def canceled(self):
        self.win = Warn('Регистрация отменена по просьбе пользователя.')
        self.win.show()
        self.close()

class Warn(QMainWindow): # Окно с сообщением

    def center(self):  # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event):  # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self, text):  # Инициализация класса
        super().__init__()
        self.initUI(text)

    def initUI(self, text):
        # Инициализация интерфейса
        def closebtn():
            self.close()

        global path
        path = path.replace("\\", "/")  # Нормализация пути
        uic.loadUi(path + "/etmemory_message.ui", self)  # Загрузка интерфейса из .ui файла
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint)  # Удаление рамок окна от ОС
        self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("background-image:url(" + path + "/bg_message.png);") # Установка фона
        self.message.setText(text)
        self.message.setStyleSheet("background-image:url(" + path + "/texture.png);")
        self.ok.setStyleSheet("""
                                                          QPushButton:!hover { background-image:url(""" + path + """/ok.png) }
                                                          QPushButton:hover { background-image:url(""" + path + """/ok_hover.png) };
                                                      """)  # Дизайн кнопки "Ок"
        self.ok.clicked.connect(self.okay)

    def ErrorMessage(self, text):
        QMessageBox.critical(self, "Error", text)

    def okay(self):
        self.close()

class Moderate(QMainWindow): # Окно модерации

    def center(self):  # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event):  # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self, moderator):  # Инициализация класса
        super().__init__()
        self.initUI(moderator)

    def initUI(self, moderator):
        # Инициализация интерфейса
        def closebtn():
            self.close()
        def approved():
            self.approved(moderator)
        global path
        path = path.replace("\\", "/")  # Нормализация пути
        uic.loadUi(path + "/etmemory_moderate.ui", self)  # Загрузка интерфейса из .ui файла
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Удаление рамок окна от ОС
        self.setWindowFlags(Qt.FramelessWindowHint)  # Удаление рамок окна от ОС
        self.setWindowIcon(QIcon(path + '/logo.png'))
        self.setStyleSheet("background-image:url(" + path + "/bg_moderate.png);")  # Установка фона
        self.description.setStyleSheet("background-image:url(" + path + "/texture.png); color: #f3f3f3")
        self.approve.setStyleSheet("""
                                                                 QPushButton:!hover { background-image:url(""" + path + """/approve.png) }
                                                                 QPushButton:hover { background-image:url(""" + path + """/approve_hover.png) };
                                                             """)  # Дизайн кнопки "Одобрить"
        self.reject.setStyleSheet("""
                                                                         QPushButton:!hover { background-image:url(""" + path + """/reject.png) }
                                                                         QPushButton:hover { background-image:url(""" + path + """/reject_hover.png) };
                                                                     """)  # Дизайн кнопки "Отклонить"
        self.closed.setStyleSheet("""
                                                                   QPushButton { border:none; background-image:url(""" + path + """/close.png) }
                                                               """)  # Дизайн кнопки "Закрыть"
        self.closed.clicked.connect(closebtn)
        self.approve.clicked.connect(approved)
        self.reject.clicked.connect(self.rejected)
        self.upload()

    def upload(self):
        global connection
        global path
        global file
        try:
            os.mkdir(path + '/TEMP')
            print('LOG (OK): Folder TEMP has been created')
        except FileExistsError:
            print('LOG (OK): Folder TEMP exists')
        MySQL.connect('37.140.192.116', 'u1001983_mhack', 'T3g3V2s5', 'u1001983_mhack')
        cursor = connection.cursor()
        queue = """SELECT * FROM `unchecked_photos` LIMIT 1"""
        cursor.execute(queue)
        ans = cursor.fetchone()
        file = ans['path']
        host = "37.140.192.116"
        ftp_user = "u1001983_uncheck"
        ftp_password = "KSoftPass9493"
        con = ftplib.FTP(host, ftp_user, ftp_password)
        f = open(path + '/TEMP/temp.jpg', "wb")
        send = con.retrbinary('RETR ' + file, f.write)
        con.close()
        f.close()
        self.IMAGE.setScaledContents(True)
        image = QImage(path + "/TEMP/temp.jpg")
        self.IMAGE.setPixmap(QPixmap.fromImage(image))
        os.remove(path + "/TEMP/temp.jpg")

    def approved(self, moderator):
        global connection
        global path
        global file
        MySQL.connect('37.140.192.116', 'u1001983_mhack', 'T3g3V2s5', 'u1001983_mhack')
        cursor = connection.cursor()
        queue = """SELECT * FROM `unchecked_photos` WHERE path = '""" + file + """'"""
        cursor.execute(queue)
        ans = cursor.fetchone()
        id = ans['id']
        queue = """DELETE FROM unchecked_photos WHERE id = """ + str(id)
        cursor.execute(queue)
        queue = """INSERT INTO checked_photos (path, moderator, lastname, firstname, middlename, dob, place_birthday, place_military, date_military, history) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(queue, (file, moderator, 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'))
        connection.commit()
        self.upload()

    def rejected(self):
        global connection
        global path
        global file
        MySQL.connect('37.140.192.116', 'u1001983_mhack', 'T3g3V2s5', 'u1001983_mhack')
        cursor = connection.cursor()
        queue = """SELECT * FROM `unchecked_photos` WHERE path = '""" + file + """'"""
        cursor.execute(queue)
        ans = cursor.fetchone()
        id = ans['id']
        queue = """DELETE FROM unchecked_photos WHERE id = """ + str(id)
        cursor.execute(queue)
        connection.commit()
        host = "37.140.192.116"
        ftp_user = "u1001983_uncheck"
        ftp_password = "KSoftPass9493"
        con = ftplib.FTP(host, ftp_user, ftp_password)
        send = con.sendcmd('DELE ' + file)
        con.close()
        self.upload()

class Warn2(QMainWindow): # Окно с сообщением

    def center(self):  # Для свободного перемещения окна (Централизация окна)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = event.pos()

    def mouseReleaseEvent(self, event):  # Для свободного перемещения окна
        if event.button() == Qt.LeftButton:
            self.__press_pos = None

    def mouseMoveEvent(self, event):  # Для свободного перемещения окна
        if self.__press_pos:
            self.move(self.pos() + (event.pos() - self.__press_pos))

    def __init__(self, text):  # Инициализация класса
        super().__init__()
        self.initUI(text)

    def initUI(self, text):
        # Инициализация интерфейса
        print('no interface')
        
    def ErrorMessage(self, text):
        buttonReply = QMessageBox.critical(self, "Error", text)
        if int(buttonReply) == 1024:
            sys.exit()

    def okay(self):
        self.close()

if __name__ == '__main__':
    try:
        SetInit()
        app = QtWidgets.QApplication([])
        startwin = Auth()
        startwin.show()
        sys.exit(app.exec_())
    except Exception as er:
        app = QtWidgets.QApplication([])
        win = Warn2('no err')
        win.ErrorMessage("Error: " + str(er))
        sys.exit(app.exec_())