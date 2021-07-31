import datetime
from datetime import date, timedelta
import threading
import json
from os.path import dirname, join, realpath
from PyQt5 import QtCore, QtGui, QtWidgets

from aqt import mw
from aqt.qt import *

from .forms import Leaderboard
from .Stats import Stats
from .Achievement import start_achievement
from .config_manager import write_config
from .League import load_league
from .userInfo import start_user_info
from .version import version
from .api_connect import connectToAPI

try:
	nightmode = mw.pm.night_mode()
except:
	nightmode = False

with open(join(dirname(realpath(__file__)), "colors.json"), "r") as colors_file:
	data = colors_file.read()
colors_themes = json.loads(data)
colors = colors_themes["dark"] if nightmode else colors_themes["light"]


class start_main(QDialog):
	def __init__(self, season_start, season_end, current_season, parent=None):
		self.parent = parent
		self.season_start = season_start
		self.season_end = season_end
		self.current_season = current_season
		self.groups_lb = []
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Leaderboard.Ui_dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		config = mw.addonManager.getConfig(__name__)
		_translate = QtCore.QCoreApplication.translate
		if config["refresh"] == True:
			self.dialog.Global_Leaderboard.setSortingEnabled(False)
			self.dialog.Friends_Leaderboard.setSortingEnabled(False)
			self.dialog.Country_Leaderboard.setSortingEnabled(False)
			self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		else:
			header1 = self.dialog.Global_Leaderboard.horizontalHeader()
			header1.sortIndicatorChanged.connect(lambda: self.highlight(self.dialog.Global_Leaderboard))
			header2 = self.dialog.Friends_Leaderboard.horizontalHeader()
			header2.sortIndicatorChanged.connect(lambda: self.highlight(self.dialog.Friends_Leaderboard))
			header3 = self.dialog.Country_Leaderboard.horizontalHeader()
			header3.sortIndicatorChanged.connect(lambda: self.highlight(self.dialog.Country_Leaderboard))
			header4 = self.dialog.Custom_Leaderboard.horizontalHeader()
			header4.sortIndicatorChanged.connect(lambda: self.highlight(self.dialog.Custom_Leaderboard))

		tab_widget = self.dialog.Parent
		country_tab = tab_widget.indexOf(self.dialog.tab_3)
		subject_tab = tab_widget.indexOf(self.dialog.tab_4)
		tab_widget.setTabText(country_tab, config["country"])
		for i in range(0, len(config["groups"])):
			self.dialog.groups.addItem("")
			self.dialog.groups.setItemText(i, _translate("Dialog", config["groups"][i]))
		self.dialog.groups.setCurrentText(config["current_group"])
		self.dialog.groups.currentTextChanged.connect(lambda: self.highlight(self.dialog.Custom_Leaderboard))
		self.dialog.Parent.setCurrentIndex(config['tab'])

		self.dialog.Global_Leaderboard.doubleClicked.connect(lambda: self.user_info(self.dialog.Global_Leaderboard))
		self.dialog.Global_Leaderboard.setToolTip("Double click on user for more info.")
		self.dialog.Friends_Leaderboard.doubleClicked.connect(lambda: self.user_info(self.dialog.Friends_Leaderboard))
		self.dialog.Friends_Leaderboard.setToolTip("Double click on user for more info.")
		self.dialog.Country_Leaderboard.doubleClicked.connect(lambda: self.user_info(self.dialog.Country_Leaderboard))
		self.dialog.Country_Leaderboard.setToolTip("Double click on user for more info.")
		self.dialog.Custom_Leaderboard.doubleClicked.connect(lambda: self.user_info(self.dialog.Custom_Leaderboard))
		self.dialog.Custom_Leaderboard.setToolTip("Double click on user for more info.")
		self.dialog.League.doubleClicked.connect(lambda: self.user_info(self.dialog.League))
		self.dialog.League.setToolTip("Double click on user for more info.")
		self.dialog.league_label.setToolTip("Leagues (from lowest to highest): Delta, Gamma, Beta, Alpha")

		### RESIZE ###

		lb_list = [self.dialog.Global_Leaderboard, self.dialog.Friends_Leaderboard, 
		self.dialog.Country_Leaderboard, self.dialog.Custom_Leaderboard, self.dialog.League]
		for l in lb_list:
			header = l.horizontalHeader()   
			header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
			header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
			header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
			header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
			header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
			header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
		
		self.load_leaderboard()

	def add_row(self, tab, username, cards, time, streak, month, retention):
		rowPosition = tab.rowCount()
		tab.setColumnCount(6)
		tab.insertRow(rowPosition)

		tab.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(username)))

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.DisplayRole, int(cards))
		tab.setItem(rowPosition, 1, item)
		item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.DisplayRole, float(time))
		tab.setItem(rowPosition, 2, item)
		item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.DisplayRole, int(streak))
		tab.setItem(rowPosition, 3, item)
		item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.DisplayRole, month)
		tab.setItem(rowPosition, 4, item)
		item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.DisplayRole, retention)
		tab.setItem(rowPosition, 5, item)
		item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

	def switchGroup(self):
		self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		config = mw.addonManager.getConfig(__name__)
		write_config("current_group", self.dialog.groups.currentText())
		self.dialog.Custom_Leaderboard.setRowCount(0)
		for i in self.groups_lb:
			if self.dialog.groups.currentText().replace(" ", "") in i[6]:
				self.add_row(self.dialog.Custom_Leaderboard, i[0], i[1], i[2], i[3], i[4], i[5])
		if config["refresh"] == True:
			self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		else:
			self.dialog.Custom_Leaderboard.setSortingEnabled(True)
		
	def load_leaderboard(self):

		### SYNC ###

		config = mw.addonManager.getConfig(__name__)
		streak, cards, time, cards_past_30_days, retention, league_reviews, league_time, league_retention, league_days_percent = Stats(self.season_start, self.season_end)

		if datetime.datetime.now() < self.season_end:
			data = {'Username': config['username'], "Streak": streak, "Cards": cards, "Time": time, "Sync_Date": datetime.datetime.now(),
			"Month": cards_past_30_days, "Country": config['country'].replace(" ", ""), "Retention": retention,
			"league_reviews": league_reviews, "league_time": league_time, "league_retention": league_retention, "league_days_percent": league_days_percent,
			"firebaseToken": config["firebaseToken"], "Version": version}
		else:
			data = {'Username': config['username'], "Streak": streak, "Cards": cards, "Time": time, "Sync_Date": datetime.datetime.now(),
			"Month": cards_past_30_days, "Country": config['country'].replace(" ", ""), "Retention": retention, "Update_League": False,
			"firebaseToken": config["firebaseToken"], "Version": version}

		x = connectToAPI("sync/", False, data, "Done!", "load_leaderboard sync")

		### ACHIEVEMENT ###

		achievement_streak = [7, 31, 100, 365, 500, 1000, 1500, 2000, 3000, 4000]
		if config["achievement"] == True and streak in achievement_streak:
			s = start_achievement(streak)
			if s.exec():
				pass

			write_config("achievement", False)

		### CLEAR TABLE ###

		self.dialog.Global_Leaderboard.setRowCount(0)
		self.dialog.Friends_Leaderboard.setRowCount(0)
		self.dialog.Country_Leaderboard.setRowCount(0)
		self.dialog.Custom_Leaderboard.setRowCount(0)
		self.dialog.League.setRowCount(0)

		### GET DATA ###

		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)
		sortby = {"sortby": config["sortby"]}
		data = connectToAPI("getdata/", True, sortby, False, "load_leaderboard getdata")

		### LEAGUE ###

		load_league(self, colors)
		time_remaining = self.season_end - datetime.datetime.now()
		tr_days = time_remaining.days
		tr_hours = int((time_remaining.seconds) / 60 / 60)

		if tr_days < 0:
			self.dialog.time_left.setText(f"The next season is going to start soon.")
		else:
			self.dialog.time_left.setText(f"{tr_days} days {tr_hours} hours remaining")
		self.dialog.time_left.setToolTip(f"Season start: {self.season_start} \nSeason end: {self.season_end} (local time)")

		### BUILD LEADERBOARD ###

		config = mw.addonManager.getConfig(__name__)
		medal_users = config["medal_users"]
		self.groups_lb = []
		c_groups = [x.replace(" ", "") for x in config["groups"]]

		for i in data:
			username = i[0]
			streak = i[1]
			cards = i[2]
			time = i[3]
			sync_date = i[4]
			sync_date = datetime.datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')
			try:
				month = int(i[5])
			except:
				month = ""
			groups = i[9]
			if i[6]:
				groups.append(i[6].replace(" ", ""))
			groups = [x.replace(" ", "") for x in groups]
			country = i[7]
			retention = i[8]
			try:
				retention = float(retention)
			except:
				retention = ""
				
			if config["show_medals"] == True:
				for i in medal_users:
					if username in i:
						username = f"{username} |"
						if i[1] > 0:
							username = f"{username} {i[1] if i[1] != 1 else ''}🥇"
						if i[2] > 0:
							username = f"{username} {i[2] if i[2] != 1 else ''}🥈"
						if i[3] > 0:
							username = f"{username} {i[3] if i[3] != 1 else ''}🥉"

			if sync_date > start_day and username.split(" |")[0] not in config["hidden_users"]:
				self.add_row(self.dialog.Global_Leaderboard, username, cards, time, streak, month, retention)

				if country == config['country'].replace(" ", "") and country != "Country":
					self.add_row(self.dialog.Country_Leaderboard, username, cards, time, streak, month, retention)

				c_groups = [x.replace(" ", "") for x in config["groups"]]
				if any(i in c_groups for i in groups):
					self.groups_lb.append([username, cards, time, streak, month, retention, groups])
					if config["current_group"].replace(" ", "") in groups:
						self.add_row(self.dialog.Custom_Leaderboard, username, cards, time, streak, month, retention)

				if username.split(" |")[0] in config['friends']:
					self.add_row(self.dialog.Friends_Leaderboard, username, cards, time, streak, month, retention)

		self.highlight(self.dialog.Global_Leaderboard)
		self.highlight(self.dialog.Friends_Leaderboard)
		self.highlight(self.dialog.Country_Leaderboard)
		self.highlight(self.dialog.Custom_Leaderboard)

		if config["refresh"] == True:
			global t
			t = threading.Timer(120.0, self.load_leaderboard)
			t.daemon = True
			t.start()
		else:
			pass

	def highlight(self, tab):
		if tab == self.dialog.Custom_Leaderboard:
			self.switchGroup()
		config = mw.addonManager.getConfig(__name__)
		for i in range(tab.rowCount()):
			item = tab.item(i, 0).text().split(" |")[0]
			if i % 2 == 0:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(colors['ROW_LIGHT']))
			else:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(colors['ROW_DARK']))
			if item in config['friends'] and tab != self.dialog.Friends_Leaderboard:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))
			if item == config['username']:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(colors['USER_COLOR']))
			if item == config['username'] and config["scroll"] == True:
				userposition = tab.item(i, 0)
				tab.selectRow(i)
				tab.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
				tab.clearSelection()

		if tab.rowCount() >= 3:
			for j in range(tab.columnCount()):
				tab.item(0, j).setBackground(QtGui.QColor(colors['GOLD_COLOR']))
				tab.item(1, j).setBackground(QtGui.QColor(colors['SILVER_COLOR']))
				tab.item(2, j).setBackground(QtGui.QColor(colors['BRONZE_COLOR']))

	def user_info(self, tab):
		for idx in tab.selectionModel().selectedIndexes():
			row = idx.row()
		user_clicked = tab.item(row, 0).text()
		if tab == self.dialog.Custom_Leaderboard:
			enabled = True
		else:
			enabled = False
		mw.user_info = start_user_info(user_clicked, enabled)
		mw.user_info.show()
		mw.user_info.raise_()
		mw.user_info.activateWindow()

	def closeEvent(self, event):
		config = mw.addonManager.getConfig(__name__)
		if config["refresh"] == True:
			global t
			t.cancel()
			event.accept()
		else:
			event.accept()