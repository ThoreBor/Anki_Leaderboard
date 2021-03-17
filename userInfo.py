from aqt.qt import *
from aqt.utils import showWarning, tooltip
from aqt import mw

import requests
import json
from PyQt5 import QtCore, QtGui, QtWidgets

from .forms import user_info
from .reportUser import start_report
from .config_manager import write_config
from .api_connect import connectToAPI

class start_user_info(QDialog):
	def __init__(self, user_clicked, enabled, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked.split(" |")[0]
		self.enabled = enabled
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = user_info.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.username_label.setText(self.user_clicked)
		if self.enabled == True:
			self.dialog.banUser.setEnabled(True)

		data = {"username": self.user_clicked}
		data = connectToAPI("getStatus/", True, data, False, "getStatus")

		if data[0]:
			self.dialog.status_message.setMarkdown(data[0])
		else:
			pass

		data = {"user": self.user_clicked}
		data = connectToAPI("getUserinfo/", True, data, False, "getUserinfo")

		header = self.dialog.history.horizontalHeader()   
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

		if data[0] == "Country":
			data[0] = None
		if data[1] == "Custom":
			data[1] = None
		if data[3]:
			medals = ""
			history = json.loads(data[3])
			results = history["results"]
			if history["gold"] > 0:
				medals = f"{medals} {history['gold'] if history['gold'] != 1 else ''}🥇"
			if history["silver"] > 0:
				medals = f"{medals} {history['silver'] if history['silver'] != 1 else ''}🥈"
			if history["bronze"] > 0:
				medals = f"{medals} {history['bronze'] if history['bronze'] != 1 else ''}🥉"
			self.dialog.medals_label.setText(f"Medals: {medals}")
			index = 0
			for i in results["leagues"]:
				rowPosition = self.dialog.history.rowCount()
				self.dialog.history.insertRow(rowPosition)
				
				self.dialog.history.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(str(i)))

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, int(results["seasons"][index]))
				self.dialog.history.setItem(rowPosition, 0, item)
				item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, int(results["xp"][index]))
				self.dialog.history.setItem(rowPosition, 2, item)
				item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

				item = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, int(results["rank"][index]))
				self.dialog.history.setItem(rowPosition, 1, item)
				item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

				index += 1

		self.dialog.country_label.setText(f"Country: {data[0]}")
		self.dialog.group_label.setText(f"Group: {data[1]}")
		self.dialog.league_label.setText(f"League: {data[2]}")
		self.dialog.hideUser.clicked.connect(self.hideUser)
		self.dialog.addFriend.clicked.connect(self.addFriend)
		self.dialog.banUser.clicked.connect(self.banUser)
		self.dialog.reportUser.clicked.connect(self.reportUser)

	def hideUser(self):
		config = mw.addonManager.getConfig(__name__)
		hidden = config["hidden_users"]
		hidden.append(self.user_clicked)
		write_config("hidden_users", hidden)
		tooltip(f"{self.user_clicked} will be hidden next time you open the leaderboard.")

	def addFriend(self):
		config = mw.addonManager.getConfig(__name__)
		friends = config['friends']
		if self.user_clicked in friends:
			tooltip(f"{self.user_clicked} already is your friend.")
		else:
			friends.append(self.user_clicked)
			write_config("friends", friends)
			tooltip(f"{self.user_clicked} is now your friend.")

	def banUser(self):
		config = mw.addonManager.getConfig(__name__)
		toBan = self.user_clicked
		group = config["current_group"]
		pwd = config["group_pwds"][config["groups"].index(config["current_group"])]
		token = config["token"]
		user = config["username"]
		data = {"toBan": toBan, "group": group, "pwd": pwd, "token": token, "user": user}
		x = connectToAPI("banUser/", False, data, "Done!", "banUser")
		if x.text == "Done!":
			tooltip(f"{toBan} is now banned from {group}")
			

	def reportUser(self):
		s = start_report(self.user_clicked)
		if s.exec():
			pass