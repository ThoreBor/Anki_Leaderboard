from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
from .Stats import Stats
import datetime
import requests
config = mw.addonManager.getConfig(__name__)

class Ui_dialog(object):
	def setupUi(self, dialog):
		dialog.setObjectName("dialog")
		dialog.resize(310, 578)
		self.widget = QtWidgets.QWidget(dialog)
		self.widget.setGeometry(QtCore.QRect(10, 10, 291, 561))
		self.widget.setObjectName("widget")
		self.gridLayout = QtWidgets.QGridLayout(self.widget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.Tab = QtWidgets.QTabWidget(self.widget)
		self.Tab.setObjectName("Tab")
		self.tab1 = QtWidgets.QWidget()
		self.tab1.setObjectName("tab1")
		self.Streak_Leaderboard = QtWidgets.QListWidget(self.tab1)
		self.Streak_Leaderboard.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Streak_Leaderboard.setFont(font)
		self.Streak_Leaderboard.setStyleSheet("QListWidget {border: none}")
		self.Streak_Leaderboard.setObjectName("Streak_Leaderboard")
		self.Tab.addTab(self.tab1, "")
		self.tab_3 = QtWidgets.QWidget()
		self.tab_3.setObjectName("tab_3")
		self.Reviews_Leaderboard = QtWidgets.QListWidget(self.tab_3)
		self.Reviews_Leaderboard.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Reviews_Leaderboard.setFont(font)
		self.Reviews_Leaderboard.setStyleSheet("QListWidget {border: none}")
		self.Reviews_Leaderboard.setObjectName("Reviews_Leaderboard")
		self.Tab.addTab(self.tab_3, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.Time_Leaderboard = QtWidgets.QListWidget(self.tab_2)
		self.Time_Leaderboard.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Time_Leaderboard.setFont(font)
		self.Time_Leaderboard.setStyleSheet("QListWidget {border: none}")
		self.Time_Leaderboard.setObjectName("Time_Leaderboard")
		self.Tab.addTab(self.tab_2, "")
		self.gridLayout.addWidget(self.Tab, 0, 0, 1, 1)

		self.retranslateUi(dialog)
		self.Tab.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(dialog)

		#SYNC#
		url = 'https://ankileaderboard.pythonanywhere.com/sync/'
		username = config['username']
		streak, cards, time = Stats()
		data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.datetime.now()}
		x = requests.post(url, data = data)

		url = 'https://ankileaderboard.pythonanywhere.com/getdata/'
		x = requests.post(url)
		data = x.text
		data = data.split("<br>")
		for i in data:
			data_list = i.split(",")
			if len(data_list) > 1:
				username = data_list[0]
				streak = data_list[1]
				cards = data_list[2]
				time = data_list[3]

				self.Streak_Leaderboard.addItem(str(username + "\t" + streak + " days"))
				self.Reviews_Leaderboard.addItem(str(username + "\t" + cards + " cards"))
				self.Time_Leaderboard.addItem(str(username + "\t" + time + " minutes"))
		



	def retranslateUi(self, dialog):
		_translate = QtCore.QCoreApplication.translate
		dialog.setWindowTitle(_translate("dialog", "Leaderboard"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab1), _translate("dialog", "Streak"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_3), _translate("dialog", "Reviews today"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("dialog", "Time"))


class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_dialog()
		self.dialog.setupUi(self)
