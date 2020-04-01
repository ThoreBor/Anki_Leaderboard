from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from os.path import dirname, join, realpath
from aqt.utils import tooltip
from datetime import date
from .Stats import Stats
from .Leaderboard import start_main

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(276, 203)
        Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        Dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'person.png')))
        Dialog.setFixedSize(Dialog.size())
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 184))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.setup_info = QtWidgets.QLabel(self.layoutWidget)
        self.setup_info.setObjectName("setup_info")
        self.gridLayout.addWidget(self.setup_info, 0, 0, 1, 2)
        self.Setup_Button = QtWidgets.QPushButton(self.layoutWidget)
        self.Setup_Button.setObjectName("Setup_Button")
        self.gridLayout.addWidget(self.Setup_Button, 1, 1, 1, 1)
        self.Username = QtWidgets.QLineEdit(self.layoutWidget)
        self.Username.setMaxLength(10)
        self.Username.setObjectName("Username")
        self.gridLayout.addWidget(self.Username, 1, 0, 1, 1)
        self.Login = QtWidgets.QPushButton(self.layoutWidget)
        self.Login.setObjectName("Login")
        self.gridLayout.addWidget(self.Login, 2, 1, 1, 1)
        self.Username__Login = QtWidgets.QLineEdit(self.layoutWidget)
        self.Username__Login.setObjectName("Username__Login")
        self.gridLayout.addWidget(self.Username__Login, 2, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.Setup_Button.clicked.connect(self.create_account)
        self.Login.clicked.connect(self.login)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Setup"))
        self.setup_info.setText(_translate("Dialog", "<html><head/><body><p>Enter a username to create an account. <br/>Creating an account will allow other users <br/>of the add-on to see your username, <br/>your streak, how many cards you studied<br/>today and for how long.<br/>If you already have an account, enter<br/>your username to login.</p></body></html>"))
        self.Setup_Button.setText(_translate("Dialog", "Create account"))
        self.Login.setText(_translate("Dialog", "Login"))

    def create_account(self):
        try:
            username = self.Username.text()
            url = 'https://ankileaderboard.pythonanywhere.com/users/'
            x = requests.post(url)
            if username in eval(x.text):
                tooltip("Username already taken")
            else:
                url = 'https://ankileaderboard.pythonanywhere.com/sync/'
                streak, cards, time = Stats()
                data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": date.today()}
                x = requests.post(url, data = data)
                config = {"new_user": "False","username": username}
                mw.addonManager.writeConfig(__name__, config)
                tooltip("Successfully created account. Close setup and restart the add-on.")
        except:
            pass

    def login(self):
        try:
            username = self.Username__Login.text()
            url = 'https://ankileaderboard.pythonanywhere.com/users/'
            x = requests.post(url)
            if username in eval(x.text):
                config = {"new_user": "False","username": username}
                mw.addonManager.writeConfig(__name__, config)
                tooltip("Successfully logged in. Close setup and restart the add-on.")
            else:
                tooltip("Account doesn't exist.")
        except:
            pass



class start_setup(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
