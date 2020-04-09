import datetime
import traceback
from datetime import date, time, timedelta
from os.path import dirname, join, realpath
from time import sleep

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
		header = self.dialog.Global_Leaderboard.horizontalHeader()
		header.sortIndicatorChanged.connect(self.change_colors)

		config = mw.addonManager.getConfig(__name__)

		tab_widget = self.dialog.Parent
		country_tab = tab_widget.indexOf(self.dialog.tab_3)
		subject_tab = tab_widget.indexOf(self.dialog.tab_4)
		tab_widget.setTabText(country_tab, config["country"])
		tab_widget.setTabText(subject_tab, config["subject"])

		self.sync()

	def sync(self):
		#SYNC#
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/sync/'
		config1 = config['username']
		config5 = config['subject']
		config6 = config['country']
		streak, cards, time, cards_past_30_days = Stats()
		data = {'Username': config1 , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.datetime.now(), "Month": cards_past_30_days, "Subject": config5, "Country": config6}
		try:
			x = requests.post(url, data = data)
		except:
			showWarning("Make sure that you're connected to the internet.")

		#get data#

		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		url = 'https://ankileaderboard.pythonanywhere.com/getreviews/'
		x = requests.post(url)
		counter = 0
		friend_counter = 0
		country_counter = 0
		custom_counter = 0
		data = x.text
		data = data.split("<br>")
		for i in data:
			if not i:
				continue
			data_list = i.split(",")
			username = data_list[0]
			streak = data_list[1]
			cards = data_list[2]
			time = data_list[3]
			sync_date = data_list[4]
			if len(sync_date) == 10:
				sync_date = sync_date + "12:00:00"
			sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))
			month = data_list[5]
			if month.isdigit():
				month = int(month)
			subject = data_list[6]
			country = data_list[7]
			if sync_date > start_day:
				counter = counter + 1

				rowPosition = self.dialog.Global_Leaderboard.rowCount()
				self.dialog.Global_Leaderboard.setColumnCount(5)
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
			
				self.dialog.Global_Leaderboard.resizeColumnsToContents()

				if country == config6 and country != "":
					country_counter = country_counter + 1

					rowPosition = self.dialog.Country_Leaderboard.rowCount()
					self.dialog.Country_Leaderboard.setColumnCount(5)
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
					item.setData(QtCore.Qt.DisplayRole, int(month))
					self.dialog.Country_Leaderboard.setItem(rowPosition, 4, item)

					self.dialog.Country_Leaderboard.resizeColumnsToContents()

					if username in config['friends']:
						for j in range(self.dialog.Country_Leaderboard.columnCount()):
							self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor("#2176ff"))

				if subject == config5 and subject != "Custom":
					custom_counter = custom_counter + 1

					rowPosition = self.dialog.Custom_Leaderboard.rowCount()
					self.dialog.Custom_Leaderboard.setColumnCount(5)
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
					item.setData(QtCore.Qt.DisplayRole, int(month))
					self.dialog.Custom_Leaderboard.setItem(rowPosition, 4, item)

					self.dialog.Custom_Leaderboard.resizeColumnsToContents()

					if username in config['friends']:
						for j in range(self.dialog.Custom_Leaderboard.columnCount()):
							self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor("#2176ff"))

				if username in config['friends']:
					friend_counter = friend_counter + 1

					rowPosition = self.dialog.Friends_Leaderboard.rowCount()
					self.dialog.Friends_Leaderboard.setColumnCount(5)
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
					item.setData(QtCore.Qt.DisplayRole, int(month))
					self.dialog.Friends_Leaderboard.setItem(rowPosition, 4, item)
				
					self.dialog.Friends_Leaderboard.resizeColumnsToContents()
				
					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#2176ff"))
				
				if username == config['username']:
					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#51f564"))
					for j in range(self.dialog.Friends_Leaderboard.columnCount()):
						self.dialog.Friends_Leaderboard.item(friend_counter-1, j).setBackground(QtGui.QColor("#51f564"))
					for j in range(self.dialog.Country_Leaderboard.columnCount()):
						self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor("#51f564"))
					for j in range(self.dialog.Custom_Leaderboard.columnCount()):
						self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor("#51f564"))
		# try:
		# 	for j in range(self.dialog.Global_Leaderboard.columnCount()):
		# 		self.dialog.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
		# 		self.dialog.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
		# 		self.dialog.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))
		# except:
		# 	pass

	def change_colors(self):
		pass
		# try:
		# 	for j in range(self.dialog.Global_Leaderboard.columnCount()):
		# 		self.dialog.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
		# 		self.dialog.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
		# 		self.dialog.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))
		# except:
		# 	pass
		# for row in range(self.dialog.Global_Leaderboard.rowCount ()):
		#    for column in range(self.dialog.Global_Leaderboard.columnCount ()):
		#        item = self.dialog.Global_Leaderboard.item(row, column )
		#        if item and item.data(Qt.DisplayRole) == "Thore":
		#            showInfo(str(self.dialog.Global_Leaderboard.indexFromItem(item)))
