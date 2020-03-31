from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from os.path import dirname, join, realpath
from aqt.utils import tooltip
from datetime import date
from .Stats import Stats

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 159)
        Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        Dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'person.png')))
        #<div>Icons erstellt von <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 261, 141))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.setup_info = QtWidgets.QLabel(self.widget)
        self.setup_info.setObjectName("setup_info")
        self.gridLayout.addWidget(self.setup_info, 0, 0, 1, 2)
        self.Username = QtWidgets.QLineEdit(self.widget)
        self.Username.setObjectName("Username")
        self.gridLayout.addWidget(self.Username, 1, 0, 1, 1)
        self.Setup_Button = QtWidgets.QPushButton(self.widget)
        self.Setup_Button.setObjectName("Setup_Button")
        self.Setup_Button.clicked.connect(self.create_account)
        self.gridLayout.addWidget(self.Setup_Button, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Setup"))
        self.setup_info.setText(_translate("Dialog", "<html><head/><body><p>Enter a username to create an account. <br/>Creating an account will allow other users <br/>of the add-on to see your username, <br/>your streak, how many cards you studied<br/>today and for how long.</p></body></html>"))
        self.Setup_Button.setText(_translate("Dialog", "Create account"))

    def create_account(self):
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
            tooltip("Successfully created account")


class start_setup(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
