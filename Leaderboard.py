import datetime
from datetime import date, timedelta
import json
from os.path import dirname, join, realpath

from aqt import mw
from aqt.theme import theme_manager
from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor, QAbstractItemView
from aqt.operations import QueryOp
from aqt.utils import showWarning

if qtmajor > 5:
	from .forms.pyqt6UI import Leaderboard
	from PyQt6 import QtCore, QtGui, QtWidgets
else:
	from .forms.pyqt5UI import Leaderboard
	from PyQt5 import QtCore, QtGui, QtWidgets
from .Stats import Stats
from .Achievement import start_achievement
from .config_manager import write_config
from .League import load_league
from .userInfo import start_user_info
from .version import version
from .api_connect import postRequest

class start_main(QDialog):
	def __init__(self, season_start, season_end, current_season, parent=None):
		self.parent = parent
		self.season_start = season_start
		self.season_end = season_end
		self.current_season = current_season
		self.groups_lb = []
		self.config = mw.addonManager.getConfig(__name__)
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = Leaderboard.Ui_dialog()
		self.dialog.setupUi(self)
		try:
			nightmode = theme_manager.night_mode
		except:
			#for older versions
			try:
				nightmode = mw.pm.night_mode()
			except:
				nightmode = False
			nightmode = False

		with open(join(dirname(realpath(__file__)), "colors.json"), "r") as colors_file:
			data = colors_file.read()
		colors_themes = json.loads(data)
		self.colors = colors_themes["dark"] if nightmode else colors_themes["light"]
		self.setupUI()

	def setupUI(self):
		_translate = QtCore.QCoreApplication.translate

		icon = QIcon()
		icon.addPixmap(QPixmap(join(dirname(realpath(__file__)), "designer/icons/krone.png")), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)
		
		header1 = self.dialog.Global_Leaderboard.horizontalHeader()
		header1.sectionClicked.connect(lambda: self.updateTable(self.dialog.Global_Leaderboard))
		header2 = self.dialog.Friends_Leaderboard.horizontalHeader()
		header2.sectionClicked.connect(lambda: self.updateTable(self.dialog.Friends_Leaderboard))
		header3 = self.dialog.Country_Leaderboard.horizontalHeader()
		header3.sectionClicked.connect(lambda: self.updateTable(self.dialog.Country_Leaderboard))
		header4 = self.dialog.Custom_Leaderboard.horizontalHeader()
		header4.sectionClicked.connect(lambda: self.updateTable(self.dialog.Custom_Leaderboard))

		tab_widget = self.dialog.Parent
		country_tab = tab_widget.indexOf(self.dialog.tab_3)
		subject_tab = tab_widget.indexOf(self.dialog.tab_4)
		tab_widget.setTabText(country_tab, self.config["country"])
		for i in range(0, len(self.config["groups"])):
			self.dialog.groups.addItem("")
			self.dialog.groups.setItemText(i, _translate("Dialog", self.config["groups"][i]))
		self.dialog.groups.setCurrentText(self.config["current_group"])
		self.dialog.groups.currentTextChanged.connect(lambda: self.updateTable(self.dialog.Custom_Leaderboard))
		self.dialog.Parent.setCurrentIndex(self.config["tab"])

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

		self.startSync()

	def header(self):
		lb_list = [self.dialog.Global_Leaderboard, self.dialog.Friends_Leaderboard, 
		self.dialog.Country_Leaderboard, self.dialog.Custom_Leaderboard, self.dialog.League]
		for l in lb_list:
			header = l.horizontalHeader()   
			header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
			header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Stretch)

			for i in range(0, 6):
				headerItem = l.horizontalHeaderItem(i)
				headerItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)

	def add_row(self, tab, username, cards, time, streak, month, retention):
		rowPosition = tab.rowCount()
		tab.setColumnCount(7)
		tab.insertRow(rowPosition)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(rowPosition + 1))
		tab.setItem(rowPosition, 0, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

		tab.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(username)))

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(cards))
		tab.setItem(rowPosition, 2, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, float(time))
		tab.setItem(rowPosition, 3, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(streak))
		tab.setItem(rowPosition, 4, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(month))
		tab.setItem(rowPosition, 5, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

		item = QtWidgets.QTableWidgetItem()
		item.setData(QtCore.Qt.ItemDataRole.DisplayRole, float(retention))
		tab.setItem(rowPosition, 6, item)
		item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

	def switchGroup(self):
		self.dialog.Custom_Leaderboard.setSortingEnabled(False)
		write_config("current_group", self.dialog.groups.currentText())
		self.dialog.Custom_Leaderboard.setRowCount(0)
		for i in self.groups_lb:
			if self.dialog.groups.currentText().replace(" ", "") in i[6]:
				self.add_row(self.dialog.Custom_Leaderboard, i[0], i[1], i[2], i[3], i[4], i[5])
		self.dialog.Custom_Leaderboard.setSortingEnabled(True)

	def achievement(self, streak):		
		achievement_streak = [7, 31, 100, 365, 500, 1000, 1500, 2000, 3000, 4000]
		if self.config["achievement"] == True and streak in achievement_streak:
			s = start_achievement(streak)
			if s.exec():
				pass
			write_config("achievement", False)
		
	def startSync(self):
		op = QueryOp(parent=mw, op=lambda col: self.sync(), success=self.on_success)
		op.with_progress().run_in_background()

	def sync(self):
		self.streak, cards, time, cardsPast30Days, retention, leagueReviews, leagueTime, leagueRetention, leagueDaysPercent = Stats(self.season_start, self.season_end)

		if datetime.datetime.now() < self.season_end:
			data = {"username": self.config["username"], "streak": self.streak, "cards": cards, "time": time, "syncDate": datetime.datetime.now(),
			"month": cardsPast30Days, "country": self.config["country"].replace(" ", ""), "retention": retention,
			"leagueReviews": leagueReviews, "leagueTime": leagueTime, "leagueRetention": leagueRetention, "leagueDaysPercent": leagueDaysPercent,
			"authToken": self.config["authToken"], "version": version, "updateLeague": True, "sortby": self.config["sortby"]}
		else:
			data = {"username": self.config["username"], "streak": self.streak, "cards": cards, "time": time, "syncDate": datetime.datetime.now(),
			"month": cardsPast30Days, "country": self.config["country"].replace(" ", ""), "retention": retention,
			"authToken": self.config["authToken"], "version": version, "updateLeague": False, "sortby": self.config["sortby"]}

		self.response = postRequest("sync/", data, 200, False)
		try:
			if self.response.status_code == 200:
				self.response = self.response.json()
				self.buildLeaderboard()
				load_league(self)
				return False
			else:
				return self.response.text
		except Exception as e:
			response = f"<h1>Something went wrong</h1>{self.response if isinstance(self.response, str) else ''}<br><br>{str(e)}"
			return response

	def on_success(self, result):
		if result:
			showWarning(result, title="Leaderboard Error")
		else:
			self.header()
			self.achievement(self.streak)
			self.show()
			self.activateWindow()
			
	def buildLeaderboard(self):

		### CLEAR TABLE ###

		self.dialog.Global_Leaderboard.setRowCount(0)
		self.dialog.Friends_Leaderboard.setRowCount(0)
		self.dialog.Country_Leaderboard.setRowCount(0)
		self.dialog.Custom_Leaderboard.setRowCount(0)
		self.dialog.League.setRowCount(0)

		new_day = datetime.time(int(self.config["newday"]),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		medal_users = self.config["medal_users"]
		self.groups_lb = []
		c_groups = [x.replace(" ", "") for x in self.config["groups"]]

		for i in self.response[0]:
			username = i[0]
			streak = i[1]
			cards = i[2]
			time = i[3]
			sync_date = i[4]
			sync_date = datetime.datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')
			month = i[5]
			groups = []
			if i[6]:
				groups.append(i[6].replace(" ", ""))
			country = i[7]
			retention = i[8]
			if i[9]:
				for group in json.loads(i[9]):
					groups.append(group)
			groups = [x.replace(" ", "") for x in groups]
				
			if self.config["show_medals"] == True:
				for i in medal_users:
					if username in i:
						username = f"{username} |"
						if i[1] > 0:
							username = f"{username} {i[1] if i[1] != 1 else ''}🥇"
						if i[2] > 0:
							username = f"{username} {i[2] if i[2] != 1 else ''}🥈"
						if i[3] > 0:
							username = f"{username} {i[3] if i[3] != 1 else ''}🥉"

			if sync_date > start_day and username.split(" |")[0] not in self.config["hidden_users"]:
				self.add_row(self.dialog.Global_Leaderboard, username, cards, time, streak, month, retention)

				if country == self.config["country"].replace(" ", "") and country != "Country":
					self.add_row(self.dialog.Country_Leaderboard, username, cards, time, streak, month, retention)

				c_groups = [x.replace(" ", "") for x in self.config["groups"]]
				if any(i in c_groups for i in groups):
					self.groups_lb.append([username, cards, time, streak, month, retention, groups])
					if self.config["current_group"].replace(" ", "") in groups:
						self.add_row(self.dialog.Custom_Leaderboard, username, cards, time, streak, month, retention)

				if username.split(" |")[0] in self.config["friends"]:
					self.add_row(self.dialog.Friends_Leaderboard, username, cards, time, streak, month, retention)

		self.highlight(self.dialog.Global_Leaderboard)
		self.highlight(self.dialog.Friends_Leaderboard)
		self.highlight(self.dialog.Country_Leaderboard)
		self.highlight(self.dialog.Custom_Leaderboard)

	def updateTable(self, tab):
		if tab == self.dialog.Custom_Leaderboard:
			self.switchGroup()
			self.updateNumbers(tab)
			self.highlight(tab)
		else:
			self.updateNumbers(tab)
			self.highlight(tab)
		
	def updateNumbers(self, tab):
		rows = tab.rowCount()
		for i in range(0, rows):
			item = QtWidgets.QTableWidgetItem()
			item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(i + 1))
			tab.setItem(i, 0, item)
			item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

	def highlight(self, tab):
		for i in range(tab.rowCount()):
			item = tab.item(i, 1).text().split(" |")[0]
			if i % 2 == 0:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(self.colors["ROW_LIGHT"]))
			else:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(self.colors["ROW_DARK"]))
			if item in self.config["friends"] and tab != self.dialog.Friends_Leaderboard:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(self.colors["FRIEND_COLOR"]))
			if item == self.config["username"]:
				for j in range(tab.columnCount()):
					tab.item(i, j).setBackground(QtGui.QColor(self.colors["USER_COLOR"]))
			if item == self.config["username"] and self.config["scroll"] == True:
				userposition = tab.item(i, 1)
				tab.selectRow(i)
				tab.scrollToItem(userposition, QAbstractItemView.PositionAtCenter)
				tab.clearSelection()

		if tab.rowCount() >= 3:
			for j in range(tab.columnCount()):
				tab.item(0, j).setBackground(QtGui.QColor(self.colors["GOLD_COLOR"]))
				tab.item(1, j).setBackground(QtGui.QColor(self.colors["SILVER_COLOR"]))
				tab.item(2, j).setBackground(QtGui.QColor(self.colors["BRONZE_COLOR"]))

	def user_info(self, tab):
		for idx in tab.selectionModel().selectedIndexes():
			row = idx.row()
		user_clicked = tab.item(row, 1).text()
		if tab == self.dialog.Custom_Leaderboard:
			enabled = True
		else:
			enabled = False
		mw.user_info = start_user_info(user_clicked, enabled)
		mw.user_info.show()
		mw.user_info.raise_()
		mw.user_info.activateWindow()