from PyQt5 import QtCore, QtGui, QtWidgets
from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
from os.path import dirname, join, realpath
import requests
from aqt.utils import tooltip

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(281, 71)
        Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        Dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'person.png')))
        Dialog.setFixedSize(Dialog.size())
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 261, 51))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Delete_Info = QtWidgets.QLabel(self.widget)
        self.Delete_Info.setObjectName("Delete_Info")
        self.gridLayout.addWidget(self.Delete_Info, 0, 0, 1, 2)
        self.username_delete = QtWidgets.QLineEdit(self.widget)
        self.username_delete.setObjectName("username_delete")
        self.gridLayout.addWidget(self.username_delete, 1, 0, 1, 1)
        self.delete_2 = QtWidgets.QPushButton(self.widget)
        self.delete_2.setObjectName("delete_2")
        self.delete_2.clicked.connect(self.delete)
        self.gridLayout.addWidget(self.delete_2, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Delete Account"))
        self.Delete_Info.setText(_translate("Dialog", "Enter your username to delete your account."))
        self.delete_2.setText(_translate("Dialog", "Delete Account"))

    def delete(self):
        try:
            username = self.username_delete.text()
            url = 'https://ankileaderboard.pythonanywhere.com/delete/'
            data = {'Username': username}
            x = requests.post(url, data = data)
            if x.text == "Deleted":
                config = {"new_user": "True","username": ""}
                mw.addonManager.writeConfig(__name__, config)
                tooltip("Successfully deleted account.")
            else:
                tooltip("Error")
        except:
            pass

class start_delete(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)
