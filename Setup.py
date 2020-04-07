from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from os.path import dirname, join, realpath
from aqt.utils import tooltip
from datetime import date, datetime
from .Stats import Stats
from .Leaderboard import start_main

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(569, 240)
		Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		Dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'person.png')))
		Dialog.setFixedSize(Dialog.size())
		self.Accout = QtWidgets.QGroupBox(Dialog)
		self.Accout.setGeometry(QtCore.QRect(10, 0, 261, 231))
		self.Accout.setObjectName("Accout")
		self.layoutWidget = QtWidgets.QWidget(self.Accout)
		self.layoutWidget.setGeometry(QtCore.QRect(11, 21, 241, 201))
		self.layoutWidget.setObjectName("layoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.create_info = QtWidgets.QLabel(self.layoutWidget)
		self.create_info.setObjectName("create_info")
		self.gridLayout.addWidget(self.create_info, 0, 0, 1, 1)
		self.create_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.create_username.setText("")
		self.create_username.setMaxLength(15)
		self.create_username.setObjectName("create_username")
		self.gridLayout.addWidget(self.create_username, 1, 0, 1, 1)
		self.create_button = QtWidgets.QPushButton(self.layoutWidget)
		self.create_button.setObjectName("create_button")
		self.gridLayout.addWidget(self.create_button, 1, 1, 1, 1)
		self.login_info = QtWidgets.QLabel(self.layoutWidget)
		self.login_info.setObjectName("login_info")
		self.gridLayout.addWidget(self.login_info, 2, 0, 1, 1)
		self.login_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.login_username.setText("")
		self.login_username.setObjectName("login_username")
		self.gridLayout.addWidget(self.login_username, 3, 0, 1, 1)
		self.login_button = QtWidgets.QPushButton(self.layoutWidget)
		self.login_button.setObjectName("login_button")
		self.gridLayout.addWidget(self.login_button, 3, 1, 1, 1)
		self.delete_info = QtWidgets.QLabel(self.layoutWidget)
		self.delete_info.setObjectName("delete_info")
		self.gridLayout.addWidget(self.delete_info, 4, 0, 1, 1)
		self.delete_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.delete_username.setText("")
		self.delete_username.setObjectName("delete_username")
		self.gridLayout.addWidget(self.delete_username, 5, 0, 1, 1)
		self.delete_button = QtWidgets.QPushButton(self.layoutWidget)
		self.delete_button.setObjectName("delete_button")
		self.gridLayout.addWidget(self.delete_button, 5, 1, 1, 1)
		self.Friends = QtWidgets.QGroupBox(Dialog)
		self.Friends.setGeometry(QtCore.QRect(280, 0, 279, 141))
		self.Friends.setObjectName("Friends")
		self.layoutWidget1 = QtWidgets.QWidget(self.Friends)
		self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 261, 111))
		self.layoutWidget1.setObjectName("layoutWidget1")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.add_friends_info = QtWidgets.QLabel(self.layoutWidget1)
		self.add_friends_info.setObjectName("add_friends_info")
		self.gridLayout_2.addWidget(self.add_friends_info, 0, 0, 1, 1)
		self.friend_username = QtWidgets.QLineEdit(self.layoutWidget1)
		self.friend_username.setText("")
		self.friend_username.setObjectName("friend_username")
		self.gridLayout_2.addWidget(self.friend_username, 1, 0, 1, 1)
		self.add_friends_button = QtWidgets.QPushButton(self.layoutWidget1)
		self.add_friends_button.setObjectName("add_friends_button")
		self.gridLayout_2.addWidget(self.add_friends_button, 1, 1, 1, 1)
		self.remove_friend_info = QtWidgets.QLabel(self.layoutWidget1)
		self.remove_friend_info.setObjectName("remove_friend_info")
		self.gridLayout_2.addWidget(self.remove_friend_info, 2, 0, 1, 1)
		self.remove_friend_username = QtWidgets.QLineEdit(self.layoutWidget1)
		self.remove_friend_username.setText("")
		self.remove_friend_username.setObjectName("remove_friend_username")
		self.gridLayout_2.addWidget(self.remove_friend_username, 3, 0, 1, 1)
		self.remove_friend_button = QtWidgets.QPushButton(self.layoutWidget1)
		self.remove_friend_button.setObjectName("remove_friend_button")
		self.gridLayout_2.addWidget(self.remove_friend_button, 3, 1, 1, 1)
		self.widget = QtWidgets.QWidget(Dialog)
		self.widget.setGeometry(QtCore.QRect(280, 150, 281, 86))
		self.widget.setObjectName("widget")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.widget)
		self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.subject = QtWidgets.QComboBox(self.widget)
		self.subject.setObjectName("subject")
		self.subject.addItem("")
		self.subject.addItem("")
		self.subject.addItem("")
		self.subject.addItem("")
		self.gridLayout_4.addWidget(self.subject, 0, 0, 1, 3)
		self.country = QtWidgets.QLineEdit(self.widget)
		self.country.setObjectName("country")
		self.gridLayout_4.addWidget(self.country, 1, 0, 1, 3)
		self.next_day_info1 = QtWidgets.QLabel(self.widget)
		self.next_day_info1.setObjectName("next_day_info1")
		self.gridLayout_4.addWidget(self.next_day_info1, 2, 0, 1, 1)
		self.newday = QtWidgets.QSpinBox(self.widget)
		self.newday.setMaximum(23)
		self.newday.setObjectName("newday")
		self.gridLayout_4.addWidget(self.newday, 2, 1, 1, 1)
		self.next_day_info2 = QtWidgets.QLabel(self.widget)
		self.next_day_info2.setObjectName("next_day_info2")
		self.gridLayout_4.addWidget(self.next_day_info2, 2, 2, 1, 1)

		self.create_button.clicked.connect(self.create_account)
		self.login_button.clicked.connect(self.login)
		self.delete_button.clicked.connect(self.delete)
		self.add_friends_button.clicked.connect(self.add_friend)
		self.remove_friend_button.clicked.connect(self.remove_friend)
		self.newday.valueChanged.connect(self.set_time)
		self.subject.currentTextChanged.connect(self.set_subject)
		self.country.textEdited.connect(self.set_country)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate

		config = mw.addonManager.getConfig(__name__)
		config4 = int(config['newday'])
		config5 = config["subject"]
		config6 = config["country"]
		self.newday.setValue(config4)
		self.country.setText(config6)

		Dialog.setWindowTitle(_translate("Dialog", "Config"))
		self.Accout.setTitle(_translate("Dialog", "Account"))
		self.create_info.setText(_translate("Dialog", "Create Account:"))
		self.create_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.create_button.setText(_translate("Dialog", "Create Account"))
		self.login_info.setText(_translate("Dialog", "Login:"))
		self.login_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.login_button.setText(_translate("Dialog", "Login"))
		self.delete_info.setText(_translate("Dialog", "Delete Account:"))
		self.delete_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.delete_button.setText(_translate("Dialog", "Delete Account"))
		self.Friends.setTitle(_translate("Dialog", "Friends"))
		self.add_friends_info.setText(_translate("Dialog", "Add Friend:"))
		self.friend_username.setPlaceholderText(_translate("Dialog", "Friend"))
		self.add_friends_button.setText(_translate("Dialog", "Add Friend"))
		self.remove_friend_info.setText(_translate("Dialog", "Remove Friend:"))
		self.remove_friend_username.setPlaceholderText(_translate("Dialog", "Friend"))
		self.remove_friend_button.setText(_translate("Dialog", "Remove Friend"))
		
		self.subject.setItemText(0, _translate("Dialog", "What are you studying?"))
		self.subject.setItemText(1, _translate("Dialog", "Languages"))
		self.subject.setItemText(2, _translate("Dialog", "Medicine"))
		self.subject.setItemText(3, _translate("Dialog", "Law"))
		self.subject.setCurrentText(config5)
		
		self.country.setPlaceholderText(_translate("Dialog", "What country are you from (in English)"))
		self.next_day_info1.setText(_translate("Dialog", "Next day starts"))
		self.next_day_info2.setText(_translate("Dialog", "hours past midnight"))
		

	def create_account(self):
		try:
			username = self.create_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/users/'
			x = requests.post(url)
			if username in eval(x.text):
				tooltip("Username already taken")
			else:
				url = 'https://ankileaderboard.pythonanywhere.com/sync/'
				streak, cards, time, cards_past_30_days = Stats()
				data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.now(), "Month": cards_past_30_days, "Subject": config5, "Country": config6}
				x = requests.post(url, data = data)
				config = {"new_user": "False","username": username, "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully created account.")
				self.create_username.setText("")
		except:
			pass

	def login(self):
		try:
			username = self.login_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/users/'
			x = requests.post(url)
			if username in eval(x.text):
				config = {"new_user": "False","username": username, "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully logged in.")
				self.login_username.setText("")
			else:
				tooltip("Account doesn't exist.")
		except:
			pass

	def delete(self):
		try:
			username = self.delete_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/delete/'
			data = {'Username': username}
			x = requests.post(url, data = data)
			if x.text == "Deleted":
				config = {"new_user": "True","username": "", "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully deleted account.")
				self.delete_username.setText("")
			else:
				tooltip("Error")
		except:
			pass

	def add_friend(self):
		username = self.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config6 = config['country']
		url = 'https://ankileaderboard.pythonanywhere.com/users/'
		x = requests.post(url)
		if config2 not in config3:
			config3.append(config2)
		if username in eval(x.text):
			config3.append(username)
			config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "country": config6, "subject": config5}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(username + " is now your friend.")
			self.friend_username.setText("")
		else:
			tooltip("Couldn't find friend")

	def remove_friend(self):
		username = self.remove_friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config6 = config['country']
		url = 'https://ankileaderboard.pythonanywhere.com/users/'
		x = requests.post(url)
		if username in config3:
			config3.remove(username)
			config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "country": config6, "subject": config5}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(username + " was removed from your friendlist")
			self.remove_friend_username.setText("")
		else:
			tooltip("Couldn't find friend")

	def set_time(self):
		beginning_of_new_day = self.newday.value()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config5 = config['subject']
		config6 = config['country']
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": str(beginning_of_new_day), "country": config6, "subject": config5}
		mw.addonManager.writeConfig(__name__, config)

	def set_subject(self):
		subject = self.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config6 = config['country']
		if subject == "What are you studying?":
			subject = "Custom"
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "subject": subject, "country": config6}
		mw.addonManager.writeConfig(__name__, config)

	def set_country(self):
		country = self.country.text()
		country = country.capitalize()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "subject": config5 , "country": country}
		mw.addonManager.writeConfig(__name__, config)


class start_setup(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_Dialog()
		self.dialog.setupUi(self)
