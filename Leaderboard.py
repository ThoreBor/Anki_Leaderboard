from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
from .Stats import Stats
from aqt.utils import tooltip, showInfo
from os.path import dirname, join, realpath
import datetime
import requests
config = mw.addonManager.getConfig(__name__)

class Ui_dialog(object):
	def setupUi(self, dialog):
		dialog.setObjectName("dialog")
		dialog.resize(315, 579)
		dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'krone.png')))
		dialog.setFixedSize(dialog.size())
		self.layoutWidget = QtWidgets.QWidget(dialog)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 291, 561))
		self.layoutWidget.setObjectName("layoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.Tab = QtWidgets.QTabWidget(self.layoutWidget)
		self.Tab.setObjectName("Tab")
		self.tab1 = QtWidgets.QWidget()
		self.tab1.setObjectName("tab1")
		self.Streak_Leaderboard = QtWidgets.QListWidget(self.tab1)
		self.Streak_Leaderboard.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(11)
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
		font.setPointSize(11)
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
		font.setPointSize(11)
		self.Time_Leaderboard.setFont(font)
		self.Time_Leaderboard.setStyleSheet("QListWidget {border: none}")
		self.Time_Leaderboard.setObjectName("Time_Leaderboard")
		self.Tab.addTab(self.tab_2, "")
		self.gridLayout.addWidget(self.Tab, 0, 0, 1, 1)

		self.retranslateUi(dialog)
		self.Tab.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(dialog)

		#SYNC#
		try:
			url = 'https://ankileaderboard.pythonanywhere.com/sync/'
			username = config['username']
			streak, cards, time = Stats()
			data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.datetime.now()}
			x = requests.post(url, data = data)

			#get data#
			url = 'https://ankileaderboard.pythonanywhere.com/getstreaks/'
			x = requests.post(url)
			counter = 0
			data = x.text
			data = data.split("<br>")
			for i in data:
				data_list = i.split(",")
				try:
					counter = counter + 1
					username = data_list[0]
					o_user = username
					if len(username) > 10:
						username = username[:10]
					if len(username) < 10:
						username += "‎  "*(10 - len(username))
					streak = data_list[1]

					self.Streak_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(streak) + " days")
					self.Streak_Leaderboard.item(counter-1).setWhatsThis("Test")

					if o_user == config['username']:
						 self.Streak_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
				except:
					pass
			try:
				self.Streak_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
				self.Streak_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
				self.Streak_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			except:
				pass

			url = 'https://ankileaderboard.pythonanywhere.com/getreviews/'
			x = requests.post(url)
			counter = 0
			data = x.text
			data = data.split("<br>")
			for i in data:
				data_list = i.split(",")
				try:
					counter = counter + 1
					username = data_list[0]
					o_user = username
					if len(username) > 10:
						username = username[:10]
					if len(username) < 10:
						username += "‎  "*(10 - len(username))
					cards = data_list[2]
				
					self.Reviews_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(cards) + " cards")

					if o_user == config['username']:
						 self.Reviews_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
				except:
					pass
			try:
				self.Reviews_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
				self.Reviews_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
				self.Reviews_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			except:
				pass

			url = 'https://ankileaderboard.pythonanywhere.com/gettime/'
			x = requests.post(url)
			counter = 0
			data = x.text
			data = data.split("<br>")
			for i in data:
				data_list = i.split(",")
				try:
					counter = counter + 1
					username = data_list[0]
					o_user = username
					if len(username) > 10:
						username = username[:10]
					if len(username) < 10:
						username += "‎  "*(10 - len(username))
					time = data_list[3]

					self.Time_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(time) + " min")
					if o_user == config['username']:
						 self.Time_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
				except:
					pass
			try:
				self.Time_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
				self.Time_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
				self.Time_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			except:
				pass
		except:
			pass

	def retranslateUi(self, dialog):
		_translate = QtCore.QCoreApplication.translate
		dialog.setWindowTitle(_translate("dialog", "Leaderboard"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab1), _translate("dialog", "Streak"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_3), _translate("dialog", "Reviews today"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("dialog", "Time")
)	

class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_dialog()
		self.dialog.setupUi(self)
