import json
from aqt import mw
from aqt.qt import Qt, qtmajor, QAbstractItemView
import datetime

if qtmajor > 5:
	from PyQt6 import QtCore, QtGui, QtWidgets
else:
	from PyQt5 import QtCore, QtGui, QtWidgets
from .config_manager import write_config

def load_league(self):
	for i in self.response[1]:
		if self.config["username"] in i:
			user_league_name = i[5]
			self.dialog.league_label.setText(f"{user_league_name}: {self.current_season}")

	time_remaining = self.season_end - datetime.datetime.now()
	tr_days = time_remaining.days

	if tr_days < 0:
		self.dialog.time_left.setText(f"The next season is going to start soon.")
	else:
		self.dialog.time_left.setText(f"{tr_days} days remaining")
	self.dialog.time_left.setToolTip(f"Season start: {self.season_start} \nSeason end: {self.season_end} (local time)")

	### BUILD TABLE ###

	medal_users = []
	counter = 0
	for i in self.response[1]:
		username = i[0]
		xp = i[1]
		reviews = i[2]
		time_spend = i[3]
		retention = i[4]
		league_name = i[5]
		days_learned = i[7]

		if i[6]:
			if self.config["show_medals"] == True:
				history = json.loads(i[6])
				if history["gold"] != 0 or history["silver"] != 0 or history["bronze"] != 0:
					medal_users.append([username, history["gold"], history["silver"], history["bronze"]])
					username = f"{username} |"
				if history["gold"] > 0:
					username = f"{username} {history['gold'] if history['gold'] != 1 else ''}🥇"
				if history["silver"] > 0:
					username = f"{username} {history['silver'] if history['silver'] != 1 else ''}🥈"
				if history["bronze"] > 0:
					username = f"{username} {history['bronze'] if history['bronze'] != 1 else ''}🥉"

		if league_name == user_league_name and xp != 0:
			counter += 1

			rowPosition = self.dialog.League.rowCount()
			self.dialog.League.setColumnCount(7)
			self.dialog.League.insertRow(rowPosition)

			self.dialog.League.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(rowPosition + 1)))
			self.dialog.League.item(rowPosition, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

			self.dialog.League.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(username)))
			
			self.dialog.League.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(xp)))
			self.dialog.League.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
			
			self.dialog.League.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(reviews)))
			self.dialog.League.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
			
			self.dialog.League.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(time_spend)))
			self.dialog.League.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
			
			self.dialog.League.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(str(retention)))
			self.dialog.League.item(rowPosition, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)
			
			self.dialog.League.setItem(rowPosition, 6, QtWidgets.QTableWidgetItem(str(days_learned)))
			self.dialog.League.item(rowPosition, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

			if username.split(" |")[0] in self.config['friends']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor(self.colors['FRIEND_COLOR']))
			if username.split(" |")[0] == self.config['username']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor(self.colors['USER_COLOR']))
	
	### HIGHLIGHT ###

	users = self.dialog.League.rowCount()

	if user_league_name == "Delta":
		threshold = int((users / 100) * 20)
	if user_league_name == "Gamma":
		threshold = int((users / 100) * 20)
	if user_league_name == "Beta":
		threshold = int((users / 100) * 20)
	if user_league_name == "Alpha":
		threshold = int((users / 100) * 20)

	for i in range(threshold):
		for j in range(self.dialog.League.columnCount()):
			item = self.dialog.League.item(i, 1).text().split(" |")[0]
			if item == self.config['username'] or item == self.config['friends'] or user_league_name == "Alpha":
				continue
			else:
				self.dialog.League.item(i, j).setBackground(QtGui.QColor(self.colors['LEAGUE_TOP']))

	if self.dialog.League.rowCount() >= 3:
		for j in range(self.dialog.League.columnCount()):
			self.dialog.League.item(0, j).setBackground(QtGui.QColor(self.colors['GOLD_COLOR']))
			self.dialog.League.item(1, j).setBackground(QtGui.QColor(self.colors['SILVER_COLOR']))
			self.dialog.League.item(2, j).setBackground(QtGui.QColor(self.colors['BRONZE_COLOR']))

		for i in range((users - threshold), users):
			for j in range(self.dialog.League.columnCount()):
				item = self.dialog.League.item(i, 1).text().split(" |")[0]
				if item == self.config['username'] and user_league_name != "Delta":
					self.dialog.League.item(i, j).setBackground(QtGui.QColor(self.colors['LEAGUE_BOTTOM_USER']))
				if user_league_name == "Delta" or item == self.config['friends']:
					continue
				else:
					self.dialog.League.item(i, j).setBackground(QtGui.QColor(self.colors['LEAGUE_BOTTOM']))
	
	### SCROLL ###

	for i in range(self.dialog.League.rowCount()):
		item = self.dialog.League.item(i, 1).text().split(" |")[0]
		if item == self.config['username']:
			userposition = self.dialog.League.item(i, 1)
			self.dialog.League.selectRow(i)
			self.dialog.League.scrollToItem(userposition, QAbstractItemView.ScrollHint.PositionAtCenter)
			self.dialog.League.clearSelection()

	### HEADER ###
	
	for i in range(0, 6):
		headerItem = self.dialog.League.horizontalHeaderItem(i)
		headerItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)

	
	write_config("medal_users", medal_users)
