from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
from .Stats import Stats
from aqt.utils import tooltip, showInfo, showWarning
from os.path import dirname, join, realpath
from datetime import date, timedelta, time, datetime
import datetime
import requests
from time import sleep
import traceback

class Ui_dialog(object):
	def setupUi(self, dialog):
		dialog.setObjectName("dialog")
		dialog.resize(525, 529)
		dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'krone.png')))
		dialog.setFixedSize(dialog.size())
		self.Parent = QtWidgets.QTabWidget(dialog)
		self.Parent.setGeometry(QtCore.QRect(10, 10, 520, 511))
		self.Parent.setObjectName("Parent")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.Global_Leaderboard = QtWidgets.QTableWidget(self.tab)
		self.Global_Leaderboard.setGeometry(QtCore.QRect(0, 10, 651, 471))
		self.Global_Leaderboard.setAutoFillBackground(False)
		self.Global_Leaderboard.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
		self.Global_Leaderboard.setShowGrid(False)
		self.Global_Leaderboard.setObjectName("Global_Leaderboard")
		self.Global_Leaderboard.setColumnCount(5)
		self.Global_Leaderboard.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.Global_Leaderboard.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.Global_Leaderboard.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.Global_Leaderboard.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.Global_Leaderboard.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.Global_Leaderboard.setHorizontalHeaderItem(4, item)
		self.Global_Leaderboard.verticalHeader().setSortIndicatorShown(False)
		self.Parent.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.Friends_Leaderboard = QtWidgets.QTableWidget(self.tab_2)
		self.Friends_Leaderboard.setGeometry(QtCore.QRect(0, 10, 651, 471))
		self.Friends_Leaderboard.setShowGrid(False)
		self.Friends_Leaderboard.setObjectName("Friends_Leaderboard")
		self.Friends_Leaderboard.setColumnCount(5)
		self.Friends_Leaderboard.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.Friends_Leaderboard.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.Friends_Leaderboard.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.Friends_Leaderboard.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.Friends_Leaderboard.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.Friends_Leaderboard.setHorizontalHeaderItem(4, item)
		self.Parent.addTab(self.tab_2, "")
		self.tab_3 = QtWidgets.QWidget()
		self.tab_3.setObjectName("tab_3")
		self.Country_Leaderboard = QtWidgets.QTableWidget(self.tab_3)
		self.Country_Leaderboard.setGeometry(QtCore.QRect(0, 10, 651, 471))
		self.Country_Leaderboard.setShowGrid(False)
		self.Country_Leaderboard.setObjectName("Country_Leaderboard")
		self.Country_Leaderboard.setColumnCount(5)
		self.Country_Leaderboard.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.Country_Leaderboard.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.Country_Leaderboard.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.Country_Leaderboard.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.Country_Leaderboard.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.Country_Leaderboard.setHorizontalHeaderItem(4, item)
		self.Parent.addTab(self.tab_3, "")
		self.tab_4 = QtWidgets.QWidget()
		self.tab_4.setObjectName("tab_4")
		self.Custom_Leaderboard = QtWidgets.QTableWidget(self.tab_4)
		self.Custom_Leaderboard.setGeometry(QtCore.QRect(0, 10, 651, 471))
		self.Custom_Leaderboard.setShowGrid(False)
		self.Custom_Leaderboard.setObjectName("Custom_Leaderboard")
		self.Custom_Leaderboard.setColumnCount(5)
		self.Custom_Leaderboard.setRowCount(0)
		item = QtWidgets.QTableWidgetItem()
		self.Custom_Leaderboard.setHorizontalHeaderItem(0, item)
		item = QtWidgets.QTableWidgetItem()
		self.Custom_Leaderboard.setHorizontalHeaderItem(1, item)
		item = QtWidgets.QTableWidgetItem()
		self.Custom_Leaderboard.setHorizontalHeaderItem(2, item)
		item = QtWidgets.QTableWidgetItem()
		self.Custom_Leaderboard.setHorizontalHeaderItem(3, item)
		item = QtWidgets.QTableWidgetItem()
		self.Custom_Leaderboard.setHorizontalHeaderItem(4, item)
		self.Parent.addTab(self.tab_4, "")

		self.retranslateUi(dialog)
		self.Parent.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(dialog)

		header = self.Global_Leaderboard.horizontalHeader()
		header.sortIndicatorChanged.connect(self.change_colors)
		
		self.sync()


		self.Global_Leaderboard.setMaximumWidth(510)
		self.Friends_Leaderboard.setMaximumWidth(510)
		self.Country_Leaderboard.setMaximumWidth(510)
		self.Custom_Leaderboard.setMaximumWidth(510)

	def retranslateUi(self, dialog):
		_translate = QtCore.QCoreApplication.translate
		config = mw.addonManager.getConfig(__name__)
		config5 = config["subject"]
		config6 = config["country"]
		dialog.setWindowTitle(_translate("dialog", "Leaderboard"))
		self.Global_Leaderboard.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Friends_Leaderboard.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Country_Leaderboard.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Custom_Leaderboard.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.Global_Leaderboard.setAlternatingRowColors(True)
		self.Friends_Leaderboard.setAlternatingRowColors(True)
		self.Country_Leaderboard.setAlternatingRowColors(True)
		self.Custom_Leaderboard.setAlternatingRowColors(True)

		self.Global_Leaderboard.setSortingEnabled(True)
		item = self.Global_Leaderboard.horizontalHeaderItem(0)
		item.setText(_translate("dialog", "Username"))
		item = self.Global_Leaderboard.horizontalHeaderItem(1)
		item.setText(_translate("dialog", "Reviews today"))
		item = self.Global_Leaderboard.horizontalHeaderItem(2)
		item.setText(_translate("dialog", "Minutes today"))
		item = self.Global_Leaderboard.horizontalHeaderItem(3)
		item.setText(_translate("dialog", "Streak"))
		item = self.Global_Leaderboard.horizontalHeaderItem(4)
		item.setText(_translate("dialog", "Reviews past 30 days"))
		self.Parent.setTabText(self.Parent.indexOf(self.tab), _translate("dialog", "Global"))
		self.Friends_Leaderboard.setSortingEnabled(True)
		item = self.Friends_Leaderboard.horizontalHeaderItem(0)
		item.setText(_translate("dialog", "Username"))
		item = self.Friends_Leaderboard.horizontalHeaderItem(1)
		item.setText(_translate("dialog", "Reviews today"))
		item = self.Friends_Leaderboard.horizontalHeaderItem(2)
		item.setText(_translate("dialog", "Minutes today"))
		item = self.Friends_Leaderboard.horizontalHeaderItem(3)
		item.setText(_translate("dialog", "Streak"))
		item = self.Friends_Leaderboard.horizontalHeaderItem(4)
		item.setText(_translate("dialog", "Reviews past 30 days"))
		self.Parent.setTabText(self.Parent.indexOf(self.tab_2), _translate("dialog", "Friends"))
		self.Country_Leaderboard.setSortingEnabled(True)
		item = self.Country_Leaderboard.horizontalHeaderItem(0)
		item.setText(_translate("dialog", "Username"))
		item = self.Country_Leaderboard.horizontalHeaderItem(1)
		item.setText(_translate("dialog", "Reviews today"))
		item = self.Country_Leaderboard.horizontalHeaderItem(2)
		item.setText(_translate("dialog", "Minutes today"))
		item = self.Country_Leaderboard.horizontalHeaderItem(3)
		item.setText(_translate("dialog", "Streak"))
		item = self.Country_Leaderboard.horizontalHeaderItem(4)
		item.setText(_translate("dialog", "Reviews past 30 days"))
		if config6 == "":
			self.Parent.setTabText(self.Parent.indexOf(self.tab_3), _translate("dialog", "Country"))
		else:
			self.Parent.setTabText(self.Parent.indexOf(self.tab_3), _translate("dialog", config6))
		self.Custom_Leaderboard.setSortingEnabled(True)
		item = self.Custom_Leaderboard.horizontalHeaderItem(0)
		item.setText(_translate("dialog", "Username"))
		item = self.Custom_Leaderboard.horizontalHeaderItem(1)
		item.setText(_translate("dialog", "Reviews today"))
		item = self.Custom_Leaderboard.horizontalHeaderItem(2)
		item.setText(_translate("dialog", "Minutes today"))
		item = self.Custom_Leaderboard.horizontalHeaderItem(3)
		item.setText(_translate("dialog", "Streak"))
		item = self.Custom_Leaderboard.horizontalHeaderItem(4)
		item.setText(_translate("dialog", "Reviews past 30 days"))
		self.Parent.setTabText(self.Parent.indexOf(self.tab_4), _translate("dialog", config5))		

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
		data = x.text
		data = data.split("<br>")
		for i in data:
			data_list = i.split(",")
			try:
				username = data_list[0]
				streak = data_list[1]
				cards = data_list[2]
				time = data_list[3]
				sync_date = data_list[4]
				sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))
				month = data_list[5]
				subject = data_list[6]
				country = data_list[7]
				if sync_date > start_day:
					counter = counter + 1

					try:
						rowPosition = self.Global_Leaderboard.rowCount()
						self.Global_Leaderboard.setColumnCount(5)
						self.Global_Leaderboard.insertRow(rowPosition)

						self.Global_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
			
						item = QtWidgets.QTableWidgetItem()
						item.setData(QtCore.Qt.DisplayRole, int(cards))
						self.Global_Leaderboard.setItem(rowPosition, 1, item)

						item = QtWidgets.QTableWidgetItem()
						item.setData(QtCore.Qt.DisplayRole, float(time))
						self.Global_Leaderboard.setItem(rowPosition, 2, item)

						item = QtWidgets.QTableWidgetItem()
						item.setData(QtCore.Qt.DisplayRole, int(streak))
						self.Global_Leaderboard.setItem(rowPosition, 3, item)

						item = QtWidgets.QTableWidgetItem()
						item.setData(QtCore.Qt.DisplayRole, int(month))
						self.Global_Leaderboard.setItem(rowPosition, 4, item)
						
						self.Global_Leaderboard.resizeColumnsToContents()
					except:
						pass

					if username in config['friends']:
						friend_counter = friend_counter + 1

						try:
							rowPosition = self.Friends_Leaderboard.rowCount()
							self.Friends_Leaderboard.setColumnCount(5)
							self.Friends_Leaderboard.insertRow(rowPosition)

							self.Friends_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
						
							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(cards))
							self.Friends_Leaderboard.setItem(rowPosition, 1, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, float(time))
							self.Friends_Leaderboard.setItem(rowPosition, 2, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(streak))
							self.Friends_Leaderboard.setItem(rowPosition, 3, item)
							

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(month))
							self.Friends_Leaderboard.setItem(rowPosition, 4, item)
							
							self.Friends_Leaderboard.resizeColumnsToContents()
						except:
							pass
						
						for j in range(self.Global_Leaderboard.columnCount()):
							self.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#2176ff"))

					if username == config['username']:
						for j in range(self.Global_Leaderboard.columnCount()):
							self.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor("#51f564"))
					
					if country == config6 and country != "":
						try:
							rowPosition = self.Country_Leaderboard.rowCount()
							self.Country_Leaderboard.setColumnCount(5)
							self.Country_Leaderboard.insertRow(rowPosition)

							self.Country_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
						
							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(cards))
							self.Country_Leaderboard.setItem(rowPosition, 1, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, float(time))
							self.Country_Leaderboard.setItem(rowPosition, 2, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(streak))
							self.Country_Leaderboard.setItem(rowPosition, 3, item)
							

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(month))
							self.Country_Leaderboard.setItem(rowPosition, 4, item)

							self.Country_Leaderboard.resizeColumnsToContents()
						except:
							pass
					
					if subject == config5 and subject != "Custom":
						try:
							rowPosition = self.Custom_Leaderboard.rowCount()
							self.Custom_Leaderboard.setColumnCount(5)
							self.Custom_Leaderboard.insertRow(rowPosition)

							self.Custom_Leaderboard.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))
						
							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(cards))
							self.Custom_Leaderboard.setItem(rowPosition, 1, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, float(time))
							self.Custom_Leaderboard.setItem(rowPosition, 2, item)

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(streak))
							self.Custom_Leaderboard.setItem(rowPosition, 3, item)
							

							item = QtWidgets.QTableWidgetItem()
							item.setData(QtCore.Qt.DisplayRole, int(month))
							self.Custom_Leaderboard.setItem(rowPosition, 4, item)

							self.Custom_Leaderboard.resizeColumnsToContents()
						except:
							pass
						 
			except:
				#showInfo(str(traceback.print_exc()))
				pass

		# try:
		# 	for j in range(self.Global_Leaderboard.columnCount()):
		# 		self.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
		# 		self.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
		# 		self.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))
		# except:
		# 	pass

	def change_colors(self):
		pass
		# try:
		# 	for j in range(self.Global_Leaderboard.columnCount()):
		# 		self.Global_Leaderboard.item(0, j).setBackground(QtGui.QColor("#ffd700"))
		# 		self.Global_Leaderboard.item(1, j).setBackground(QtGui.QColor("#c0c0c0"))
		# 		self.Global_Leaderboard.item(2, j).setBackground(QtGui.QColor("#bf8970"))
		# except:
		# 	pass
		# for row in range(self.Global_Leaderboard.rowCount ()):
		#    for column in range(self.Global_Leaderboard.columnCount ()):
		#        item = self.Global_Leaderboard.item(row, column )
		#        if item and item.data(Qt.DisplayRole) == "Thore":
		#            showInfo(str(self.Global_Leaderboard.indexFromItem(item)))
class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_dialog()
		self.dialog.setupUi(self)
