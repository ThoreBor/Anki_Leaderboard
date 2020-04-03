from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
from .Stats import Stats
from aqt.utils import tooltip, showInfo, showWarning
from os.path import dirname, join, realpath
from datetime import date, timedelta, time, datetime
import datetime
import requests

class Ui_dialog(object):
	def setupUi(self, dialog):
		config = mw.addonManager.getConfig(__name__)
		dialog.setObjectName("dialog")
		dialog.resize(330, 619)
		dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'krone.png')))
		dialog.setFixedSize(dialog.size())
		self.Parent = QtWidgets.QTabWidget(dialog)
		self.Parent.setGeometry(QtCore.QRect(10, 10, 311, 601))
		self.Parent.setObjectName("Parent")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.Tab = QtWidgets.QTabWidget(self.tab)
		self.Tab.setGeometry(QtCore.QRect(10, 10, 289, 559))
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
		self.Parent.addTab(self.tab, "")
		self.tab_4 = QtWidgets.QWidget()
		self.tab_4.setObjectName("tab_4")
		self.Tab_2 = QtWidgets.QTabWidget(self.tab_4)
		self.Tab_2.setGeometry(QtCore.QRect(10, 10, 289, 559))
		self.Tab_2.setObjectName("Tab_2")
		self.tab1_2 = QtWidgets.QWidget()
		self.tab1_2.setObjectName("tab1_2")
		self.Streak_Leaderboard_Friends = QtWidgets.QListWidget(self.tab1_2)
		self.Streak_Leaderboard_Friends.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Streak_Leaderboard_Friends.setFont(font)
		self.Streak_Leaderboard_Friends.setStyleSheet("QListWidget {border: none}")
		self.Streak_Leaderboard_Friends.setObjectName("Streak_Leaderboard_Friends")
		self.Tab_2.addTab(self.tab1_2, "")
		self.tab_5 = QtWidgets.QWidget()
		self.tab_5.setObjectName("tab_5")
		self.Reviews_Leaderboard_Friends = QtWidgets.QListWidget(self.tab_5)
		self.Reviews_Leaderboard_Friends.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Reviews_Leaderboard_Friends.setFont(font)
		self.Reviews_Leaderboard_Friends.setStyleSheet("QListWidget {border: none}")
		self.Reviews_Leaderboard_Friends.setObjectName("Reviews_Leaderboard_Friends")
		self.Tab_2.addTab(self.tab_5, "")
		self.tab_6 = QtWidgets.QWidget()
		self.tab_6.setObjectName("tab_6")
		self.Time_Leaderboard_Friends = QtWidgets.QListWidget(self.tab_6)
		self.Time_Leaderboard_Friends.setGeometry(QtCore.QRect(10, 10, 271, 511))
		font = QtGui.QFont()
		font.setFamily("Arial")
		font.setPointSize(12)
		self.Time_Leaderboard_Friends.setFont(font)
		self.Time_Leaderboard_Friends.setStyleSheet("QListWidget {border: none}")
		self.Time_Leaderboard_Friends.setObjectName("Time_Leaderboard_Friends")
		self.Tab_2.addTab(self.tab_6, "")
		self.Parent.addTab(self.tab_4, "")

		self.retranslateUi(dialog)
		self.Parent.setCurrentIndex(0)
		self.Tab.setCurrentIndex(0)
		self.Tab_2.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(dialog)

		#SYNC#

		url = 'https://ankileaderboard.pythonanywhere.com/sync/'
		username = config['username']
		streak, cards, time = Stats()
		data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.datetime.now()}
		try:
			x = requests.post(url, data = data)
		except:
			showWarning("Make sure that you're connected to the internet.")

		#get data#
		url = 'https://ankileaderboard.pythonanywhere.com/getstreaks/'
		x = requests.post(url)
		counter = 0
		friend_counter = 0
		data = x.text
		data = data.split("<br>")

		config = mw.addonManager.getConfig(__name__)
		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		for i in data:
			try:
				data_list = i.split(",")			
				username = data_list[0]
				o_user = username
				if len(username) > 10:
					username = username[:10]
				if len(username) < 10:
					username += "‎  "*(10 - len(username))
				streak = data_list[1]
				
				sync_date = data_list[4]
				sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

				if sync_date > start_day:
					counter = counter + 1
					self.Streak_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(streak) + " days")

					if o_user in config['friends']:
						friend_counter = friend_counter + 1
						self.Streak_Leaderboard_Friends.addItem(str(friend_counter)+ ". "+ str(username) + "\t" + str(streak) + " days")
						self.Streak_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#2176ff"))

					if o_user == config['username']:
						self.Streak_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
						self.Streak_Leaderboard_Friends.item(friend_counter-1).setBackground(QtGui.QColor("#51f564"))
			except:
				pass

		try:
			self.Streak_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Streak_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Streak_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			self.Streak_Leaderboard_Friends.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Streak_Leaderboard_Friends.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Streak_Leaderboard_Friends.item(2).setBackground(QtGui.QColor("#bf8970"))
		except:
			pass

		url = 'https://ankileaderboard.pythonanywhere.com/getreviews/'
		x = requests.post(url)
		counter = 0
		friend_counter = 0
		data = x.text
		data = data.split("<br>")
		for i in data:
			data_list = i.split(",")
			try:
				username = data_list[0]
				o_user = username
				if len(username) > 10:
					username = username[:10]
				if len(username) < 10:
					username += "‎  "*(10 - len(username))
				cards = data_list[2]
				
				sync_date = data_list[4]
				sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

				if sync_date > start_day:
					counter = counter + 1
					self.Reviews_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(cards) + " cards")

					if o_user in config['friends']:
						friend_counter = friend_counter + 1
						self.Reviews_Leaderboard_Friends.addItem(str(friend_counter)+ ". "+ str(username) + "\t" + str(cards) + " cards")
						self.Reviews_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#2176ff"))
					if o_user == config['username']:
						 self.Reviews_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
						 self.Reviews_Leaderboard_Friends.item(friend_counter-1).setBackground(QtGui.QColor("#51f564"))
			except:
				pass
		try:
			self.Reviews_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Reviews_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Reviews_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			self.Reviews_Leaderboard_Friends.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Reviews_Leaderboard_Friends.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Reviews_Leaderboard_Friends.item(2).setBackground(QtGui.QColor("#bf8970"))
		except:
			pass

		url = 'https://ankileaderboard.pythonanywhere.com/gettime/'
		x = requests.post(url)
		counter = 0
		friend_counter = 0
		data = x.text
		data = data.split("<br>")
		for i in data:
			data_list = i.split(",")
			try:
				username = data_list[0]
				o_user = username
				if len(username) > 10:
					username = username[:10]
				if len(username) < 10:
					username += "‎  "*(10 - len(username))
				time = data_list[3]

				sync_date = data_list[4]
				sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

				if sync_date > start_day:
					counter = counter + 1
					self.Time_Leaderboard.addItem(str(counter)+ ". "+ str(username) + "\t" + str(time) + " min")

					if o_user in config['friends']:
						friend_counter = friend_counter + 1
						self.Time_Leaderboard_Friends.addItem(str(friend_counter)+ ". "+ str(username) + "\t" + str(time) + " min")
						self.Time_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#2176ff"))
					if o_user == config['username']:
						 self.Time_Leaderboard.item(counter-1).setBackground(QtGui.QColor("#51f564"))
						 self.Time_Leaderboard_Friends.item(friend_counter-1).setBackground(QtGui.QColor("#51f564"))
			except:
				pass
		try:
			self.Time_Leaderboard.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Time_Leaderboard.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Time_Leaderboard.item(2).setBackground(QtGui.QColor("#bf8970"))
			self.Time_Leaderboard_Friends.item(0).setBackground(QtGui.QColor("#ffd700"))
			self.Time_Leaderboard_Friends.item(1).setBackground(QtGui.QColor("#c0c0c0"))
			self.Time_Leaderboard_Friends.item(2).setBackground(QtGui.QColor("#bf8970"))
		except:
			pass


	def retranslateUi(self, dialog):
		_translate = QtCore.QCoreApplication.translate
		dialog.setWindowTitle(_translate("dialog", "Leaderboard"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab1), _translate("dialog", "Streak"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_3), _translate("dialog", "Reviews today"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("dialog", "Time"))
		self.Parent.setTabText(self.Parent.indexOf(self.tab), _translate("dialog", "Global"))
		self.Tab_2.setTabText(self.Tab_2.indexOf(self.tab1_2), _translate("dialog", "Streak"))
		self.Tab_2.setTabText(self.Tab_2.indexOf(self.tab_5), _translate("dialog", "Reviews today"))
		self.Tab_2.setTabText(self.Tab_2.indexOf(self.tab_6), _translate("dialog", "Time"))
		self.Parent.setTabText(self.Parent.indexOf(self.tab_4), _translate("dialog", "Friends"))

class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_dialog()
		self.dialog.setupUi(self)
