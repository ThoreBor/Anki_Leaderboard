import datetime
from datetime import date, time, timedelta
from os.path import dirname, join, realpath
import threading

import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, showWarning, tooltip

from .forms import Leaderboard
from .Stats import Stats


class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Leaderboard.Ui_dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		config = mw.addonManager.getConfig(__name__)
		if config["refresh"] == "True":
			self.dialog.Global_Leaderboard.setSortingEnabled(False)
			self.dialog.Friends_Leaderboard.setSortingEnabled(False)
			self.dialog.Country_Leaderboard.setSortingEnabled(False)
			self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		else:
			header1 = self.dialog.Global_Leaderboard.horizontalHeader()
			header1.sortIndicatorChanged.connect(self.change_colors_global)
			header2 = self.dialog.Friends_Leaderboard.horizontalHeader()
			header2.sortIndicatorChanged.connect(self.change_colors_friends)
			header3 = self.dialog.Country_Leaderboard.horizontalHeader()
			header3.sortIndicatorChanged.connect(self.change_colors_country)
			header4 = self.dialog.Custom_Leaderboard.horizontalHeader()
			header4.sortIndicatorChanged.connect(self.change_colors_custom)

		config = mw.addonManager.getConfig(__name__)
		tab_widget = self.dialog.Parent
		country_tab = tab_widget.indexOf(self.dialog.tab_3)
		subject_tab = tab_widget.indexOf(self.dialog.tab_4)
		tab_widget.setTabText(country_tab, config["country"])
		tab_widget.setTabText(subject_tab, config["subject"])

		self.load_leaderboard()

	def load_leaderboard(self):

		### SYNC ###

		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/sync/'
		config1 = config['username']
		config5 = config['subject'].replace(" ", "")
		config6 = config['country'].replace(" ", "")
		streak, cards, time, cards_past_30_days, retention = Stats()
		data = {'Username': config1 , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.datetime.now(), 
		"Month": cards_past_30_days, "Subject": config5, "Country": config6, "Retention": retention}
		try:
			x = requests.post(url, data = data)
		except:
			showWarning("Make sure you're connected to the internet.")

		### CLEAR TABLE ###

		self.dialog.Global_Leaderboard.setRowCount(0)
		self.dialog.Friends_Leaderboard.setRowCount(0)
		self.dialog.Country_Leaderboard.setRowCount(0)
		self.dialog.Custom_Leaderboard.setRowCount(0)

		### GET DATA ###

		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		url = 'https://ankileaderboard.pythonanywhere.com/getdata/'
		try:
			data = requests.get(url).json()
		except:
			showWarning("Make sure you're connected to the internet.")
		counter = 0
		friend_counter = 0
		country_counter = 0
		custom_counter = 0
		for i in data:
			username = i[0]
			streak = i[1]
			cards = i[2]
			time = i[3]
			sync_date = i[4]
			sync_date = sync_date.replace(" ", "")
			if len(sync_date) == 10:
				sync_date = sync_date + "12:00:00"
			sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))
			try:
				month = int(i[5])
			except:
				month = ""
			subject = i[6]
			country = i[7]
			retention = i[8]
			try:
				retention = float(retention)
			except:
				retention = ""
			if sync_date > start_day:
				counter = counter + 1

				rowPosition = self.dialog.Global_Leaderboard.rowCount()
				self.dialog.Global_Leaderboard.setColumnCount(6)
				self.dialog.Global_Leaderboard.insertRow(rowPosition)

				self.dialog.Global_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, int(cards))
				self.dialog.Global_Leaderboard.setItem(rowPosition, 1, item)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, float(time))
				self.dialog.Global_Leaderboard.setItem(rowPosition, 2, item)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, int(streak))
				self.dialog.Global_Leaderboard.setItem(rowPosition, 3, item)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, month)
				self.dialog.Global_Leaderboard.setItem(rowPosition, 4, item)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, retention)
				self.dialog.Global_Leaderboard.setItem(rowPosition, 5, item)
			
				self.dialog.Global_Leaderboard.resizeColumnsToContents()

				if country == config6 and country != "Country":
					country_counter = country_counter + 1

					rowPosition = self.dialog.Country_Leaderboard.rowCount()
					self.dialog.Country_Leaderboard.setColumnCount(6)
					self.dialog.Country_Leaderboard.insertRow(rowPosition)

					self.dialog.Country_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
			
					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(cards))
					self.dialog.Country_Leaderboard.setItem(rowPosition, 1, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, float(time))
					self.dialog.Country_Leaderboard.setItem(rowPosition, 2, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(streak))
					self.dialog.Country_Leaderboard.setItem(rowPosition, 3, item)
				

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, month)
					self.dialog.Country_Leaderboard.setItem(rowPosition, 4, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, retention)
					self.dialog.Country_Leaderboard.setItem(rowPosition, 5, item)

					self.dialog.Country_Leaderboard.resizeColumnsToContents()

					if username in config['friends']:
						for j in range(self.dialog.Country_Leaderboard.columnCount()):
							self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor("#2176ff"))

				if subject == config5 and subject != "Custom":
					custom_counter = custom_counter + 1

					rowPosition = self.dialog.Custom_Leaderboard.rowCount()
					self.dialog.Custom_Leaderboard.setColumnCount(6)
					self.dialog.Custom_Leaderboard.insertRow(rowPosition)

					self.dialog.Custom_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
			
					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(cards))
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 1, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, float(time))
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 2, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(streak))
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 3, item)
				

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, month)
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 4, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, retention)
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 5, item)

					self.dialog.Custom_Leaderboard.resizeColumnsToContents()

					if username in config['friends']:
						for j in range(self.dialog.Custom_Leaderboard.columnCount()):
							self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor("#2176ff"))

				if username in config['friends']:
					friend_counter = friend_counter + 1

					rowPosition = self.dialog.Friends_Leaderboard.rowCount()
					self.dialog.Friends_Leaderboard.setColumnCount(6)
					self.dialog.Friends_Leaderboard.insertRow(rowPosition)

					self.dialog.Friends_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
			
					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(cards))
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 1, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, float(time))
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 2, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, int(streak))
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 3, item)
				

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, month)
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 4, item)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, retention)
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 5, item)
				
					self.dialog.Friends_Leaderboard.resizeColumnsToContents()
				
					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#2176ff"))
				

				if username == config['username']:
					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#51f564"))
					if config['friends'] != []:
						for j in range(self.dialog.Friends_Leaderboard.columnCount()):
							self.dialog.Friends_Leaderboard.item(friend_counter-1, j).setBackground(QtGui.QColor("#51f564"))
					if config['country'] != "Country":
						for j in range(self.dialog.Country_Leaderboard.columnCount()):
							self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor("#51f564"))
					if config["subject"] != "Custom":
						for j in range(self.dialog.Custom_Leaderboard.columnCount()):
							self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor("#51f564"))
							
		### Highlight first three places###
		
		if self.dialog.Global_Leaderboard.rowCount() >= 3:
			global first_three_global
			first_three_global = []
			for i in range(3):
				item = self.dialog.Global_Leaderboard.item(i, 0).text()
				first_three_global.append(item)

			for j in range(self.dialog.Global_Leaderboard.columnCount()):
				self.dialog.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

		if self.dialog.Friends_Leaderboard.rowCount() >= 3:
			global first_three_friends
			first_three_friends = []
			for i in range(3):
				item = self.dialog.Friends_Leaderboard.item(i, 0).text()
				first_three_friends.append(item)

			for j in range(self.dialog.Friends_Leaderboard.columnCount()):
				self.dialog.Friends_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Friends_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Friends_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

		if self.dialog.Country_Leaderboard.rowCount() >= 3:
			global first_three_country
			first_three_country = []
			for i in range(3):
				item = self.dialog.Country_Leaderboard.item(i, 0).text()
				first_three_country.append(item)

			for j in range(self.dialog.Country_Leaderboard.columnCount()):
				self.dialog.Country_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Country_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Country_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

		if self.dialog.Custom_Leaderboard.rowCount() >= 3:
			global first_three_custom
			first_three_custom = []
			for i in range(3):
				item = self.dialog.Custom_Leaderboard.item(i, 0).text()
				first_three_custom.append(item)

			for j in range(self.dialog.Custom_Leaderboard.columnCount()):
				self.dialog.Custom_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Custom_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Custom_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))
		
		### SCROLL ###

		current_ranking_list = []
		if config["scroll"] == "True":
			for i in range(self.dialog.Global_Leaderboard.rowCount()):
				item = self.dialog.Global_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username']:
					userposition = self.dialog.Global_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Global_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
					self.dialog.Global_Leaderboard.selectRow(current_ranking_list.index(item))
					self.dialog.Global_Leaderboard.clearSelection()

		current_ranking_list = []
		if config["scroll"] == "True":
			for i in range(self.dialog.Friends_Leaderboard.rowCount()):
				item = self.dialog.Friends_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username']:
					userposition = self.dialog.Friends_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Friends_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
					self.dialog.Friends_Leaderboard.selectRow(current_ranking_list.index(item))
					self.dialog.Friends_Leaderboard.clearSelection()

		current_ranking_list = []
		if config["scroll"] == "True":
			for i in range(self.dialog.Country_Leaderboard.rowCount()):
				item = self.dialog.Country_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username']:
					userposition = self.dialog.Country_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Country_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
					self.dialog.Country_Leaderboard.selectRow(current_ranking_list.index(item))
					self.dialog.Country_Leaderboard.clearSelection()

		current_ranking_list = []
		if config["scroll"] == "True":
			for i in range(self.dialog.Custom_Leaderboard.rowCount()):
				item = self.dialog.Custom_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username']:
					userposition = self.dialog.Custom_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Custom_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
					self.dialog.Custom_Leaderboard.selectRow(current_ranking_list.index(item))
					self.dialog.Custom_Leaderboard.clearSelection()

		if config["refresh"] == "True":
			global t
			t = threading.Timer(120.0, self.load_leaderboard)
			t.daemon = True
			t.start()
		else:
			pass

	def change_colors_global(self):
		if self.dialog.Global_Leaderboard.rowCount() >= 3:
			config = mw.addonManager.getConfig(__name__)
			global first_three_global
			current_ranking_list = []

			for i in range(self.dialog.Global_Leaderboard.rowCount()):
				item = self.dialog.Global_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username'] and config["scroll"] == "True":
					userposition = self.dialog.Global_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Global_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)

			for i in first_three_global:
				for j in range(self.dialog.Global_Leaderboard.columnCount()):
					if mw.pm.night_mode() == False:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#ffffff"))
						else:
							self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#f5f5f5"))
					else:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#3A3A3A"))
						else:
							self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2F2F31"))

					if i in config['friends']:
						self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2176ff"))
					if i == config['username']:
						self.dialog.Global_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#51f564"))

			for j in range(self.dialog.Global_Leaderboard.columnCount()):
				self.dialog.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

			first_three_global = []
			for i in range(3):
				item = self.dialog.Global_Leaderboard.item(i, 0).text()
				first_three_global.append(item)

	def change_colors_friends(self):
		if self.dialog.Friends_Leaderboard.rowCount() >= 3:
			config = mw.addonManager.getConfig(__name__)
			global first_three_friends
			current_ranking_list = []

			for i in range(self.dialog.Friends_Leaderboard.rowCount()):
				item = self.dialog.Friends_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username'] and config["scroll"] == "True":
					userposition = self.dialog.Friends_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Friends_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)

			for i in first_three_friends:
				for j in range(self.dialog.Friends_Leaderboard.columnCount()):
					if mw.pm.night_mode() == False:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Friends_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#ffffff"))
						else:
							self.dialog.Friends_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#f5f5f5"))
					else:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Friends_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#3A3A3A"))
						else:
							self.dialog.Friends_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2F2F31"))

					if i == config['username']:
						self.dialog.Friends_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#51f564"))

			for j in range(self.dialog.Friends_Leaderboard.columnCount()):
				self.dialog.Friends_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Friends_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Friends_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

			first_three_friends = []
			for i in range(3):
				item = self.dialog.Friends_Leaderboard.item(i, 0).text()
				first_three_friends.append(item)

	def change_colors_country(self):
		if self.dialog.Country_Leaderboard.rowCount() >= 3:
			config = mw.addonManager.getConfig(__name__)
			global first_three_country
			current_ranking_list = []

			for i in range(self.dialog.Country_Leaderboard.rowCount()):
				item = self.dialog.Country_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username'] and config["scroll"] == "True":
					userposition = self.dialog.Country_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Country_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)

			for i in first_three_country:
				for j in range(self.dialog.Country_Leaderboard.columnCount()):
					if mw.pm.night_mode() == False:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#ffffff"))
						else:
							self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#f5f5f5"))
					else:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#3A3A3A"))
						else:
							self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2F2F31"))

					if i in config['friends']:
						self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2176ff"))
					if i == config['username']:
						self.dialog.Country_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#51f564"))

			for j in range(self.dialog.Country_Leaderboard.columnCount()):
				self.dialog.Country_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Country_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Country_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

			first_three_country = []
			for i in range(3):
				item = self.dialog.Country_Leaderboard.item(i, 0).text()
				first_three_country.append(item)

	def change_colors_custom(self):
		if self.dialog.Custom_Leaderboard.rowCount() >= 3:
			config = mw.addonManager.getConfig(__name__)
			global first_three_custom
			current_ranking_list = []

			for i in range(self.dialog.Custom_Leaderboard.rowCount()):
				item = self.dialog.Custom_Leaderboard.item(i, 0).text()
				current_ranking_list.append(item)
				if item == config['username'] and config["scroll"] == "True":
					userposition = self.dialog.Custom_Leaderboard.item(current_ranking_list.index(item), 0)
					self.dialog.Custom_Leaderboard.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)

			for i in first_three_custom:
				for j in range(self.dialog.Custom_Leaderboard.columnCount()):
					if mw.pm.night_mode() == False:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#ffffff"))
						else:
							self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#f5f5f5"))
					else:
						if current_ranking_list.index(i) % 2 == 0:
							self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#3A3A3A"))
						else:
							self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2F2F31"))

					if i in config['friends']:
						self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#2176ff"))
					if i == config['username']:
						self.dialog.Custom_Leaderboard.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor("#51f564"))

			for j in range(self.dialog.Custom_Leaderboard.columnCount()):
				self.dialog.Custom_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
				self.dialog.Custom_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
				self.dialog.Custom_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))

			first_three_custom = []
			for i in range(3):
				item = self.dialog.Custom_Leaderboard.item(i, 0).text()
				first_three_custom.append(item)

	def closeEvent(self, event):
		config = mw.addonManager.getConfig(__name__)
		if config["refresh"] == "True":
			global t
			t.cancel()
			event.accept()
		else:
			event.accept()