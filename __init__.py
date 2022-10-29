from aqt import mw
from aqt.qt import QAction, QMenu, QKeySequence
from aqt.utils import showInfo, showWarning, tooltip, askUser
from aqt.operations import QueryOp

from os.path import dirname, join, realpath
import os
import webbrowser
import requests
from bs4 import BeautifulSoup
import datetime
import json

from .Leaderboard import start_main
from .config import start_config
from .Stats import Stats
from .config_manager import write_config
from .lb_on_homescreen import leaderboard_on_deck_browser
from .version import version
from .api_connect import *


class startup():
	def __init__(self):
		config = mw.addonManager.getConfig(__name__)

		# Create menu
		self.addMenu('&Leaderboard', "&Open", self.leaderboard, 'Shift+L')
		self.addMenu('&Leaderboard', "&Sync and update the home screen leaderboard", self.startBackgroundSync, "Shift+S")
		self.addMenu('&Leaderboard', "&Config", self.invokeSetup, "Alt+C")
		self.addMenu('&Leaderboard', "&Make a feature request or report a bug", self.github)
		mw.addonManager.setConfigAction(__name__, self.configSetup)

		try:
			from aqt import gui_hooks
			gui_hooks.profile_did_open.append(self.profileHook)
			gui_hooks.addons_dialog_will_delete_addons.append(self.deleteHook)
		except:
			if config["import_error"] == True:
				showInfo("Because you're using an older Anki version some features of the Leaderboard add-on can't be used.", title="Leaderboard")
				write_config("import_error", False)

	def profileHook(self):
		config = mw.addonManager.getConfig(__name__)
		self.checkInfo()
		self.checkBackup()	
		write_config("achievement", True)
		write_config("homescreen_data", [])
		self.addUsernameToFriendlist()
		self.season()
		if config["autosync"] == True:
			gui_hooks.reviewer_will_end.append(self.startBackgroundSync)
		if config["homescreen"] == True:
			self.startBackgroundSync()

	def leaderboard(self):
		config = mw.addonManager.getConfig(__name__)
		if config["username"] == "" or not config["authToken"]:
			invokeSetup()
		else:
			mw.leaderboard = start_main(self.start, self.end, self.currentSeason)

	def invokeSetup(self):
		mw.lb_setup = start_config(self.start, self.end)
		mw.lb_setup.show()
		mw.lb_setup.raise_()
		mw.lb_setup.activateWindow()

	def configSetup(self):
		s = start_config(self.start, self.end)
		if s.exec():
			pass

	def github(self):
		webbrowser.open('https://github.com/ThoreBor/Anki_Leaderboard/issues')

	def checkInfo(self):
		config = mw.addonManager.getConfig(__name__)
		try:
			url = 'https://ankileaderboardinfo.netlify.app'
			page = requests.get(url, timeout=10)
			soup = BeautifulSoup(page.content, 'html.parser')
			if soup.find(id='show_message').get_text() == "True":
				info = soup.find("div", id="Message")
				notification_id = soup.find("div", id="id").get_text()
				if config["notification_id"] != notification_id:
					showInfo(str(info), title="Leaderboard")
					write_config("notification_id", notification_id)
		except Exception as e:
			showWarning(f"Timeout error [checkInfo] - No internet connection, or server response took too long.\n {e}", title="Leaderboard error")

	def addUsernameToFriendlist(self):
		# Legacy
		config = mw.addonManager.getConfig(__name__)
		if config['username'] != "" and config['username'] not in config['friends']:
			friends = config["friends"]
			friends.append(config['username'])
			write_config("friends", friends)

	def startBackgroundSync(self):
		op = QueryOp(parent=mw, op=lambda col: self.backgroundSync(), success=self.on_success)
		op.with_progress().run_in_background()

	def backgroundSync(self):
		config = mw.addonManager.getConfig(__name__)
		streak, cards, time, cardsPast30Days, retention, leagueReviews, leagueTime, leagueRetention, leagueDaysPercent = Stats(self.start, self.end)

		if datetime.datetime.now() < self.end:
			data = {'username': config['username'], "streak": streak, "cards": cards, "time": time, "syncDate": datetime.datetime.now(),
			"month": cardsPast30Days, "country": config['country'].replace(" ", ""), "retention": retention,
			"leagueReviews": leagueReviews, "leagueTime": leagueTime, "leagueRetention": leagueRetention, "leagueDaysPercent": leagueDaysPercent,
			"authToken": config["authToken"], "version": version, "updateLeague": True, "sortby": config["sortby"]}
		else:
			data = {'username': config['username'], "streak": streak, "cards": cards, "time": time, "syncDate": datetime.datetime.now(),
			"month": cardsPast30Days, "country": config['country'].replace(" ", ""), "retention": retention,
			"authToken": config["authToken"], "version": version, "updateLeague": False, "sortby": config["sortby"]}

		self.response = postRequest("sync/", data, 200, False)
		try:
			if self.response.status_code == 200:
				write_config("homescreen_data", [])
				return False
			else:
				return self.response.text
		except:
			return self.response

	def on_success(self, result):
		if result:
			showWarning(result, title="Leaderboard Error")
		else:
			leaderboard_on_deck_browser(self.response.json())

	def season(self):
		response = getRequest("season/")
		if response:
			response = response.json()
			self.start = response[0]
			self.start = datetime.datetime(self.start[0],self.start[1],self.start[2],self.start[3],self.start[4],self.start[5])
			self.end = response[1]
			self.end = datetime.datetime(self.end[0],self.end[1],self.end[2],self.end[3],self.end[4],self.end[5])
			self.currentSeason = response[2]
		else:
			self.start = datetime.datetime.now()
			self.end = datetime.datetime.now()
			self.currentSeason = ""

	def deleteHook(self, dialog, ids):
		config = mw.addonManager.getConfig(__name__)
		showInfoDeleteAccount = """<h3>Deleting Leaderboard Account</h3>
		Keep in mind that deleting the add-on only removes the local files. If you also want to delete your account, go to
		Leaderboard>Config>Account>Delete account.
		"""
		askUserCreateMetaBackup = """
		<h3>Leaderboard Configuration Backup</h3>
		If you want to reinstall this add-on in the future, creating a backup of the configurations is recommended. Do you want to create a backup?
		"""
		if "41708974" in ids or "Anki_Leaderboard" in ids:
			showInfo(showInfoDeleteAccount)
			if askUser(askUserCreateMetaBackup):
				meta_backup = open(join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "leaderboard_meta_backup.json"), "w", encoding="utf-8")
				meta_backup.write(json.dumps({"config": config}))
				meta_backup.close()
				tooltip("Successfully created a backup")

	def checkBackup(self):
		askUserRestoreFromBackup = """<h3>Leaderboard configuration backup found</h3>
		Do you want to restore your configurations?
		"""
		backup_path = join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "leaderboard_meta_backup.json")
		if os.path.exists(backup_path):
			meta_backup = open(backup_path, "r", encoding="utf-8")
			if askUser(askUserRestoreFromBackup):
				new_meta = open(join(dirname(realpath(__file__)), "meta.json"), "w", encoding="utf-8") 
				new_meta.write(json.dumps(json.loads(meta_backup.read())))
				new_meta.close()
				meta_backup.close()
			os.remove(backup_path)

	def addMenu(self, parent, child, function, shortcut=None):
		menubar = [i for i in mw.form.menubar.actions()]
		if parent in [i.text() for i in menubar]:
			menu = [i.parent() for i in menubar][[i.text() for i in menubar].index(parent)]
		else:
			menu = mw.form.menubar.addMenu(parent)
		item = QAction(child, menu)
		item.triggered.connect(function)
		if shortcut:
			item.setShortcut(QKeySequence(shortcut))
		menu.addAction(item)

startup()