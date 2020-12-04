from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import json

from aqt import mw
from aqt.qt import *
from aqt.utils import showWarning, showInfo

from .config_manager import write_config

def load_league(self, colors):

	### GET DATA ###

	config = mw.addonManager.getConfig(__name__)
	url = 'https://ankileaderboard.pythonanywhere.com/league/'
	try:
		data = requests.get(url, timeout=20).json()
	except:
		data = []
		showWarning("Timeout error [load_league] - No internet connection, or server response took too long.", title="Leaderboard error")

	user_league_name = "Alpha"
	for i in data:
		if config["username"] in i:
			user_league_name = i[5]
			self.dialog.league_label.setText(f"{user_league_name}: {self.current_season}")

	### BUILD TABLE ###

	medal_users = []
	counter = 0
	for i in data:
		username = i[0]
		xp = i[1]
		reviews = i[2]
		time_spend = i[3]
		retention = i[4]
		league_name = i[5]
		if i[7]:
			days_learned = i[7]
		else:
			days_learned = "n/a"

		if i[6]:
			history = json.loads(i[6])
			if history["gold"] != 0 or history["silver"] != 0 or history["bronze"] != 0:
				medal_users.append([username, history["gold"], history["silver"], history["bronze"]])
				username = f"{username} |"
			if config["show_medals"] == True:
				if history["gold"] > 0:
					username = f"{username} {history['gold'] if history['gold'] != 1 else ''}🥇"
				if history["silver"] > 0:
					username = f"{username} {history['silver'] if history['silver'] != 1 else ''}🥈"
				if history["bronze"] > 0:
					username = f"{username} {history['bronze'] if history['bronze'] != 1 else ''}🥉"

		if league_name == user_league_name and xp != 0:
			counter += 1

			rowPosition = self.dialog.League.rowCount()
			self.dialog.League.setColumnCount(6)
			self.dialog.League.insertRow(rowPosition)

			self.dialog.League.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(username)))
			self.dialog.League.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(xp)))
			self.dialog.League.item(rowPosition, 1).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
			self.dialog.League.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(reviews)))
			self.dialog.League.item(rowPosition, 2).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
			self.dialog.League.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(time_spend)))
			self.dialog.League.item(rowPosition, 3).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
			self.dialog.League.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(retention)))
			self.dialog.League.item(rowPosition, 4).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
			self.dialog.League.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(str(days_learned)))
			self.dialog.League.item(rowPosition, 5).setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

			if username.split(" |")[0] in config['friends']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))
			if username.split(" |")[0] == config['username']:
				for j in range(self.dialog.League.columnCount()):
					self.dialog.League.item(counter-1, j).setBackground(QtGui.QColor(colors['USER_COLOR']))
	
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
			item = self.dialog.League.item(i, 0).text().split(" |")[0]
			if item == config['username'] or item == config['friends'] or user_league_name == "Alpha":
				continue
			else:
				self.dialog.League.item(i, j).setBackground(QtGui.QColor(colors['LEAGUE_TOP']))

	if self.dialog.League.rowCount() >= 3:
		for j in range(self.dialog.League.columnCount()):
			self.dialog.League.item(0, j).setBackground(QtGui.QColor(colors['GOLD_COLOR']))
			self.dialog.League.item(1, j).setBackground(QtGui.QColor(colors['SILVER_COLOR']))
			self.dialog.League.item(2, j).setBackground(QtGui.QColor(colors['BRONZE_COLOR']))

		for i in range((users - threshold), users):
			for j in range(self.dialog.League.columnCount()):
				item = self.dialog.League.item(i, 0).text().split(" |")[0]
				if item == config['username'] and user_league_name != "Delta":
					self.dialog.League.item(i, j).setBackground(QtGui.QColor(colors['LEAGUE_BOTTOM_USER']))
				if user_league_name == "Delta" or item == config['friends']:
					continue
				else:
					self.dialog.League.item(i, j).setBackground(QtGui.QColor(colors['LEAGUE_BOTTOM']))
	
	write_config("medal_users", medal_users)