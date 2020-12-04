import datetime
from datetime import date, timedelta
import threading
import requests
import json
from os.path import dirname, join, realpath
from PyQt5 import QtCore, QtGui, QtWidgets

from aqt import mw
from aqt.qt import *
from aqt.utils import showWarning

from .forms import Leaderboard
from .Stats import Stats
from .Achievement import start_achievement
from .config_manager import write_config
from .League import load_league
from .userInfo import start_user_info
from .lb_on_homescreen import leaderboard_on_deck_browser
from .version import version

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
		self.first_three_global = []
		self.first_three_friends = []
		self.first_three_country = []
		self.first_three_custom =[]
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Leaderboard.Ui_dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		config = mw.addonManager.getConfig(__name__)
		if config["refresh"] == True:
			self.dialog.Global_Leaderboard.setSortingEnabled(False)
			self.dialog.Friends_Leaderboard.setSortingEnabled(False)
			self.dialog.Country_Leaderboard.setSortingEnabled(False)
			self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		else:
			header1 = self.dialog.Global_Leaderboard.horizontalHeader()
			header1.sortIndicatorChanged.connect(lambda: self.change_colors(self.dialog.Global_Leaderboard))
			header2 = self.dialog.Friends_Leaderboard.horizontalHeader()
			header2.sortIndicatorChanged.connect(lambda: self.change_colors(self.dialog.Friends_Leaderboard))
			header3 = self.dialog.Country_Leaderboard.horizontalHeader()
			header3.sortIndicatorChanged.connect(lambda: self.change_colors(self.dialog.Country_Leaderboard))
			header4 = self.dialog.Custom_Leaderboard.horizontalHeader()
			header4.sortIndicatorChanged.connect(lambda: self.change_colors(self.dialog.Custom_Leaderboard))

		tab_widget = self.dialog.Parent
		country_tab = tab_widget.indexOf(self.dialog.tab_3)
		subject_tab = tab_widget.indexOf(self.dialog.tab_4)
		tab_widget.setTabText(country_tab, config["country"])
		tab_widget.setTabText(subject_tab, config["subject"])
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
		lb_list = [self.dialog.Global_Leaderboard, self.dialog.Friends_Leaderboard, self.dialog.Country_Leaderboard, self.dialog.Custom_Leaderboard, self.dialog.League]
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
		
	def load_leaderboard(self):

		### SYNC ###

		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/sync/'
		config5 = config['subject'].replace(" ", "")
		config6 = config['country'].replace(" ", "")

		streak, cards, time, cards_past_30_days, retention, league_reviews, league_time, league_retention, league_days_percent = Stats(self.season_start, self.season_end)

		if datetime.datetime.now() < self.season_end:
			data = {'Username': config['username'], "Streak": streak, "Cards": cards, "Time": time, "Sync_Date": datetime.datetime.now(),
			"Month": cards_past_30_days, "Country": config6, "Retention": retention,
			"league_reviews": league_reviews, "league_time": league_time, "league_retention": league_retention, "league_days_percent": league_days_percent,
			"Token_v3": config["token"], "Version": version}
		else:
			data = {'Username': config['username'], "Streak": streak, "Cards": cards, "Time": time, "Sync_Date": datetime.datetime.now(),
			"Month": cards_past_30_days, "Country": config6, "Retention": retention, "Update_League": False,
			"Token_v3": config["token"], "Version": version}

		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				pass
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [load_leaderboard sync] - No internet connection, or server response took too long.", title="Leaderboard error")

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

		url = 'https://ankileaderboard.pythonanywhere.com/getdata/'
		sortby = {"sortby": config["sortby"]}
		try:
			data = requests.post(url, data = sortby, timeout=20).json()
		except:
			data = []
			showWarning("Timeout error [load_leaderboard getData] - No internet connection, or server response took too long.", title="Leaderboard error")

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
				counter += 1
				self.add_row(self.dialog.Global_Leaderboard, username, cards, time, streak, month, retention)

				if country == config6 and country != "Country":
					country_counter += 1
					self.add_row(self.dialog.Country_Leaderboard, username, cards, time, streak, month, retention)

					if username.split(" |")[0] in config['friends']:
						for j in range(self.dialog.Country_Leaderboard.columnCount()):
							self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))

				if subject == config5 and subject != "Custom":
					custom_counter += 1
					self.add_row(self.dialog.Custom_Leaderboard, username, cards, time, streak, month, retention)

					if username.split(" |")[0] in config['friends']:
						for j in range(self.dialog.Custom_Leaderboard.columnCount()):
							self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))

				if username.split(" |")[0] in config['friends']:
					friend_counter += 1
					self.add_row(self.dialog.Friends_Leaderboard, username, cards, time, streak, month, retention)

					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))

				if username.split(" |")[0] == config['username']:
					for j in range(self.dialog.Global_Leaderboard.columnCount()):
						self.dialog.Global_Leaderboard.item(counter-1, j).setBackground(QtGui.QColor(colors['USER_COLOR']))
					if config['friends'] != []:
						for j in range(self.dialog.Friends_Leaderboard.columnCount()):
							self.dialog.Friends_Leaderboard.item(friend_counter-1, j).setBackground(QtGui.QColor(colors['USER_COLOR']))
					if config['country'] != "Country":
						for j in range(self.dialog.Country_Leaderboard.columnCount()):
							self.dialog.Country_Leaderboard.item(country_counter-1, j).setBackground(QtGui.QColor(colors['USER_COLOR']))
					if config["subject"] != "Custom":
						for j in range(self.dialog.Custom_Leaderboard.columnCount()):
							self.dialog.Custom_Leaderboard.item(custom_counter-1, j).setBackground(QtGui.QColor(colors['USER_COLOR']))

		### Highlight first three places###

		lb_list = [self.dialog.Global_Leaderboard, self.dialog.Friends_Leaderboard, self.dialog.Country_Leaderboard, self.dialog.Custom_Leaderboard, self.dialog.League]

		for index, l in zip(range(4), lb_list):
			if l.rowCount() >= 3:
				if l == self.dialog.Global_Leaderboard:
					for i in range(3):
						item = l.item(i, 0).text().split(" |")[0]
						self.first_three_global.append(item)
				if l == self.dialog.Friends_Leaderboard:
					for i in range(3):
						item = l.item(i, 0).text().split(" |")[0]
						self.first_three_friends.append(item)
				if l == self.dialog.Country_Leaderboard:
					for i in range(3):
						item = l.item(i, 0).text().split(" |")[0]
						self.first_three_country.append(item)
				if l == self.dialog.Custom_Leaderboard:
					for i in range(3):
						item = l.item(i, 0).text().split(" |")[0]
						self.first_three_custom.append(item)

				for j in range(l.columnCount()):
					l.item(0, j).setBackground(QtGui.QColor(colors['GOLD_COLOR']))
					l.item(1, j).setBackground(QtGui.QColor(colors['SILVER_COLOR']))
					l.item(2, j).setBackground(QtGui.QColor(colors['BRONZE_COLOR']))

		### SCROLL ###

		if config["scroll"] == True:
			for l in lb_list:
				for i in range(l.rowCount()):
					item = l.item(i, 0).text().split(" |")[0]
					if item == config['username']:
						userposition = l.item(i, 0)
						l.selectRow(i)
						l.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
						l.clearSelection()

		if config["refresh"] == True:
			global t
			t = threading.Timer(120.0, self.load_leaderboard)
			t.daemon = True
			t.start()
		else:
			pass

	def change_colors(self, tab):
		if tab == self.dialog.Global_Leaderboard:
			top_list = self.first_three_global
		if tab == self.dialog.Friends_Leaderboard:
			top_list = self.first_three_friends
		if tab == self.dialog.Country_Leaderboard:
			top_list = self.first_three_country
		if tab == self.dialog.Custom_Leaderboard:
			top_list = self.first_three_custom

		if tab.rowCount() >= 3:
			config = mw.addonManager.getConfig(__name__)
			current_ranking_list = []

			for i in range(tab.rowCount()):
				item = tab.item(i, 0).text().split(" |")[0]
				current_ranking_list.append(item)
				if item == config['username'] and config["scroll"] == True:
					userposition = tab.item(current_ranking_list.index(item), 0)
					tab.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)

			for i in top_list:
				for j in range(tab.columnCount()):
					if current_ranking_list.index(i) % 2 == 0:
						tab.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor(colors['ROW_LIGHT']))
					else:
						tab.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor(colors['ROW_DARK']))

					if i.split(" |")[0] in config['friends']:
						tab.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor(colors['FRIEND_COLOR']))
					if i.split(" |")[0] == config['username']:
						tab.item(current_ranking_list.index(i), j).setBackground(QtGui.QColor(colors['USER_COLOR']))

			for j in range(tab.columnCount()):
				tab.item(0, j).setBackground(QtGui.QColor(colors['GOLD_COLOR']))
				tab.item(1, j).setBackground(QtGui.QColor(colors['SILVER_COLOR']))
				tab.item(2, j).setBackground(QtGui.QColor(colors['BRONZE_COLOR']))

			
			if tab == self.dialog.Global_Leaderboard:
				self.first_three_global = []
				for i in range(3):
					item = tab.item(i, 0).text().split(" |")[0]
					self.first_three_global.append(item)

			if tab == self.dialog.Friends_Leaderboard:
				self.first_three_friends = []
				for i in range(3):
					item = tab.item(i, 0).text().split(" |")[0]
					self.first_three_friends.append(item)
			
			if tab == self.dialog.Country_Leaderboard:
				self.first_three_country = []
				for i in range(3):
					item = tab.item(i, 0).text().split(" |")[0]
					self.first_three_country.append(item)
			
			if tab == self.dialog.Custom_Leaderboard:
				self.first_three_custom = []
				for i in range(3):
					item = tab.item(i, 0).text().split(" |")[0]
					self.first_three_custom.append(item)

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