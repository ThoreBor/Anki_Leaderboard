from datetime import datetime
from os.path import dirname, join, realpath

import requests
import hashlib
from PyQt5 import QtCore

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo, showWarning

from .forms import setup
from .Stats import Stats
from .config_manager import write_config
from .lb_on_homescreen import leaderboard_on_deck_browser
from .version import version

class start_setup(QDialog):
	def __init__(self, season_start, season_end, parent=None):
		self.parent = parent
		self.season_start = season_start
		self.season_end = season_end
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = setup.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		config = mw.addonManager.getConfig(__name__)

		self.update_login_info(config["username"])
		self.dialog.newday.setValue(int(config['newday']))
		self.dialog.Default_Tab.setCurrentIndex(config['tab'])
		self.dialog.scroll.setChecked(bool(config["scroll"]))
		self.dialog.refresh.setChecked(bool(config["refresh"]))
		self.update_friends_list(sorted(config["friends"], key=str.lower))
		self.update_hidden_list(sorted(config["hidden_users"], key=str.lower))
		self.dialog.LB_DeckBrowser.setChecked(bool(config["homescreen"]))
		self.dialog.autosync.setChecked(bool(config["autosync"]))
		self.dialog.maxUsers.setValue(config["maxUsers"])
		self.dialog.lb_focus.setChecked(bool(config["focus_on_user"]))
		self.dialog.medals.setChecked(bool(config["show_medals"]))
		if config["sortby"] == "Time_Spend":
			self.dialog.sortby.setCurrentText("Time")
		if config["sortby"] == "Month":
			self.dialog.sortby.setCurrentText("Reviews past 30 days")
		else:
			self.dialog.sortby.setCurrentText(config["sortby"])

		self.dialog.Default_Tab.setToolTip("This affects the Leaderboard and, if enabled, the home screen leaderboard.")
		self.dialog.sortby.setToolTip("This affects the Leaderboard and, if enabled, the home screen leaderboard.")
		self.dialog.statusMsg.setToolTip("Message that everyone can see when clicking on your username (max. 280 characters). You can use markdown to embed links.")
		self.dialog.create_button.setToolTip("This might take a few seconds.")
		self.dialog.newday.setToolTip("This needs to be the same as in Ankis' preferences.")
		self.dialog.autosync.setToolTip("It will take a few extra seconds before you return to the homescreen after answering the last due card in a deck.")
		self.load_Group()

		_translate = QtCore.QCoreApplication.translate

		for i in range(1, 256):
			self.dialog.country.addItem("")

		country_list = ['Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil', 'British Indian Ocean Territory', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Canary Islands', 'Cape Verde', 'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic', 'Ceuta & Melilla', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo - Brazzaville', 'Congo - Kinshasa', 'Cook Islands', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czechia', 'Denmark', 'Diego Garcia', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Eurozone', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau SAR China', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territories', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'San Marino', 'São Tomé & Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia & South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Barthélemy', 'St. Helena', 'St. Kitts & Nevis', 'St. Lucia', 'St. Martin', 'St. Pierre & Miquelon', 'St. Vincent & Grenadines', 'Sudan', 'Suriname', 'Svalbard & Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad & Tobago', 'Tristan da Cunha', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks & Caicos Islands', 'Tuvalu', 'U.S. Outlying Islands', 'U.S. Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United Nations', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis & Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
		
		# item 0 is set by pyuic from the .ui file
		for i in country_list:
			self.dialog.country.setItemText(country_list.index(i), _translate("Dialog", i))

		self.dialog.country.setCurrentText(config["country"])

		self.dialog.create_username.returnPressed.connect(self.create_account)
		self.dialog.create_button.clicked.connect(self.create_account)
		self.dialog.login_username.returnPressed.connect(self.login)
		self.dialog.login_button.clicked.connect(self.login)
		self.dialog.delete_username.returnPressed.connect(self.delete)
		self.dialog.delete_button.clicked.connect(self.delete)
		self.dialog.statusButton.clicked.connect(self.status)
		self.dialog.statusMsg.returnPressed.connect(self.status)
		self.dialog.friend_username.returnPressed.connect(self.add_friend)
		self.dialog.add_friends_button.clicked.connect(self.add_friend)
		self.dialog.remove_friend_button.clicked.connect(self.remove_friend)
		self.dialog.newday.valueChanged.connect(self.set_time)
		self.dialog.joinGroup.clicked.connect(self.join_group)
		self.dialog.add_newGroup.clicked.connect(self.create_new_group)
		self.dialog.manageSave.clicked.connect(self.manage_group)
		self.dialog.country.currentTextChanged.connect(self.set_country)
		self.dialog.Default_Tab.currentTextChanged.connect(self.set_default_tab)
		self.dialog.sortby.currentTextChanged.connect(self.set_sortby)
		self.dialog.scroll.stateChanged.connect(self.set_scroll)
		self.dialog.refresh.stateChanged.connect(self.set_refresh)
		self.dialog.medals.stateChanged.connect(self.set_medals)
		self.dialog.import_friends.clicked.connect(self.import_list)
		self.dialog.export_friends.clicked.connect(self.export_list)
		self.dialog.unhideButton.clicked.connect(self.unhide)
		self.dialog.LB_DeckBrowser.stateChanged.connect(self.set_homescreen)
		self.dialog.autosync.stateChanged.connect(self.set_autosync)
		self.dialog.maxUsers.valueChanged.connect(self.set_maxUser)
		self.dialog.lb_focus.stateChanged.connect(self.set_focus)

		self.dialog.next_day_info1.setText(_translate("Dialog", "Next day starts"))
		self.dialog.next_day_info2.setText(_translate("Dialog", "hours past midnight"))

		about_text = f"""
<h2>Anki Leaderboard {version}</h2>
This add-on ranks all of its users by the number of cards reviewed today, time spend studying today, 
current streak, reviews in the past 31 days, and retention. You can also compete against friends, join a group, 
and join a country leaderboard. You'll only see users, that synced on the same day as you.<br><br>
In the league tab, you see everyone that synced at least once during the current season. There are four leagues
(Alpha, Beta, Gamma, and Delta). A season lasts two weeks. You don't have to sync every day.
<b>Starting from season 6,</b> the XP formula is:<br><code>XP = days studied percentage x ((6 x time) + (2 x reviews x retention))</code>
<i><a href="https://github.com/ThoreBor/Anki_Leaderboard/issues/122">See this issue for more info<a/></i><br>
At the end of each season, the top 20% will be promoted, and the last 20% will be relegated.<br><br>
The code for the add-on is available on <a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub.</a> 
It is licensed under the <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/LICENSE">MIT License.</a> 
If you like this add-on, rate and review it on <a href="https://ankiweb.net/shared/info/41708974">Anki Web.</a><br><br>
You can also check the leaderboard (past 24 hours) on this <a href="https://ankileaderboard.pythonanywhere.com/">website</a>.<br>
<div>Crown icon made by <a href="https://www.flaticon.com/de/autoren/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Person icon made by <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Confetti gif from <a href="https://giphy.com/stickers/giphycam-rainbow-WNJATm9pwnjpjI1i0g">Giphy</a></div>
<br>
<b>© Thore Tyborski 2020<br><br>
With contributions from <a href="https://github.com/khonkhortisan">khonkhortisan</a>, <a href="https://github.com/zjosua">zjosua</a>, 
<a href="https://www.reddit.com/user/SmallFluffyIPA/">SmallFluffyIPA</a> and <a href="https://github.com/AtilioA">Atílio Antônio Dadalto</a>.<br><br>
Also thank you to everyone who reported bugs and suggested new features!</b><br><br>
Contact: leaderboard_support@protonmail.com, <a href="https://www.reddit.com/user/Ttime5">Reddit</a> or 
<a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub</a>.
<h3>Change Log:</h3>
<b>{version}:</b><br>
- streak hotfix<br>
- increased window width<br>
<b>v1.6.3:</b><br>
- fixed odd number bug on home screen leaderboard<br>
- reduced home screen leaderboard server requests (improves performance)<br>
- home screen leaderboard users are clickable (for more info about user)<br>
- top three users of each league will get a medal that can be shown next to the username (optional) and will appear in the profile (starting from season 4)<br>
- season results are now being saved for each user and appear in their profile (starting from season 4)<br>
- "🥇", "🥈", "🥉" and "|" aren't allowed in usernames anymore<br>
- minor ui changes<br>
- improve the efficiency of statistical calculations (improves performance)<br>
- added "days studied" (in the current season) to league tab (a day counts when the user studied for at least 10 minutes)<br>
- users with 0 XP will be relegated in addition to the last 20%<br>
- notifications (server downtime, updates etc.) will only be shown once<br>
- new XP formula: <code>XP = days studied percentage x ((6 x time) + (2 x reviews x retention))</code> <b>starting from season 6<b>
"""

		self.dialog.about_text.setHtml(about_text)

	def create_account(self):
		username = self.dialog.create_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
		try:
			username_list = requests.get(url, timeout=20).json()
		except:
			showWarning("Timeout error [create_account] - No internet connection, or server response took too long.", title="Leaderboard error")

		if username in username_list:
			tooltip("Username already taken")
		else:
			url = 'https://ankileaderboard.pythonanywhere.com/sync/'

			streak, cards, time, cards_past_30_days, retention, league_reviews, league_time, league_retention, league_days_percent = Stats(self.season_start, self.season_end)
			config5 = config['subject'].replace(" ", "")
			config6 = config['country'].replace(" ", "")

			data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.now(), 
			"Month": cards_past_30_days, "Country": config["country"], "Retention": retention,
			"league_reviews": league_reviews, "league_time": league_time, "league_retention": league_retention, "league_days_percent": league_days_percent,
			"Version": version}
			
			try:
				x = requests.post(url, data = data)
				if x.text == "Done!":
					tooltip("Successfully created account.")
				else:
					showWarning(str(x.text))
				write_config("username", username)
				self.dialog.create_username.setText("")
				self.update_login_info(username)
			except:
				showWarning("Timeout error [create_account] - No internet connection, or server response took too long.", title="Leaderboard error")

	def update_login_info(self, username):
		login_info = self.dialog.login_info_2
		if username:
			login_info.setText(f"Logged in as {username}.")
		else:
			login_info.setText("You are not logged in.")

	def update_friends_list(self, friends):
		config = mw.addonManager.getConfig(__name__)
		friends_list = self.dialog.friends_list
		friends_list.clear()
		for friend in friends:
			if friend != config['username']:
				friends_list.addItem(friend)

	def login(self):
		username = self.dialog.login_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
		try:
			username_list = requests.get(url, timeout=20).json()
			if username in username_list:
				write_config("username", username)
				tooltip("Successfully logged in.")
				self.dialog.login_username.setText("")
				self.update_login_info(username)
			else:
				tooltip("Account doesn't exist.")
		except:
			showWarning("Timeout error [login] - No internet connection, or server response took too long.", title="Leaderboard error")

	def delete(self):
		username = self.dialog.delete_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/delete/'
		data = {'Username': username, "Token_v3": config["token"]}
		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Deleted":
				write_config("username", "")
				tooltip("Successfully deleted account.")
				self.dialog.delete_username.setText("")
			else:
				tooltip("Error")
		except:
			showWarning("Timeout error [delete] - No internet connection, or server response took too long.", title="Leaderboard error")

	def add_friend(self):
		username = self.dialog.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
		try:
			username_list = requests.get(url).json()
			if config['username'] and config['username'] not in config['friends']:
				config['friends'].append(config['username'])
			
			if username in username_list and username not in config['friends']:
				config['friends'].append(username)
				write_config("friends", config['friends'])
				tooltip(username + " is now your friend.")
				self.dialog.friend_username.setText("")
				self.update_friends_list(sorted(config["friends"], key=str.lower))
			else:
				tooltip("Couldn't find friend")
		except:
			showWarning("Timeout error [add_friend] - No internet connection, or server response took too long.", title="Leaderboard error")

	def remove_friend(self):
		for item in self.dialog.friends_list.selectedItems():
			username = item.text()
			config = mw.addonManager.getConfig(__name__)
			config['friends'].remove(username)
			write_config("friends", config["friends"])
			tooltip(f"{username} was removed from your friendlist")
			self.update_friends_list(config["friends"])

	def set_time(self):
		beginning_of_new_day = self.dialog.newday.value()
		write_config("newday", beginning_of_new_day)

	def set_country(self):
		country = self.dialog.country.currentText()
		write_config("country", country)

	def set_scroll(self):
		if self.dialog.scroll.isChecked():
			scroll = True
		else:
			scroll = False
		write_config("scroll", scroll)
	
	def set_refresh(self):
		if self.dialog.refresh.isChecked():
			refresh = True
		else:
			refresh = False
		write_config("refresh", refresh)
	
	def set_default_tab(self):
		config = mw.addonManager.getConfig(__name__)
		tab = self.dialog.Default_Tab.currentText()
		if tab == "Global":
			write_config("tab", 0)
		if tab == "Friends":
			write_config("tab", 1)
		if tab == "Country":
			write_config("tab", 2)
		if tab == "Group":
			write_config("tab", 3)
		if tab == "League":
			write_config("tab", 4)
		if config["homescreen"] == True:
			write_config("homescreen_data", [])
			leaderboard_on_deck_browser()

	def set_sortby(self):
		config = mw.addonManager.getConfig(__name__)
		sortby = self.dialog.sortby.currentText()
		if sortby == "Reviews":
			write_config("sortby", "Cards")
		if sortby == "Time":
			write_config("sortby", "Time_Spend")
		if sortby == "Streak":
			write_config("sortby", sortby)
		if sortby == "Reviews past 31 days":
			write_config("sortby", "Month")
		if sortby == "Retention":
			write_config("sortby", sortby)
		if config["homescreen"] == True:
			write_config("homescreen_data", [])
			leaderboard_on_deck_browser()

	def set_homescreen(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.LB_DeckBrowser.isChecked():
			homescreen = True
		else:
			homescreen = False
		write_config("homescreen", homescreen)
		leaderboard_on_deck_browser()

	def set_maxUser(self):
		config = mw.addonManager.getConfig(__name__)
		maxUsers = self.dialog.maxUsers.value()
		write_config("maxUsers", maxUsers)
		if config["homescreen"] == True:
			leaderboard_on_deck_browser()

	def set_autosync(self):
		if self.dialog.autosync.isChecked():
			autosync = True
		else:
			autosync = False
		write_config("autosync", autosync)

	def set_focus(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.lb_focus.isChecked():
			focus = True
		else:
			focus = False
		write_config("focus_on_user", focus)
		if config["homescreen"] == True:
			leaderboard_on_deck_browser()

	def set_medals(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.medals.isChecked():
			medals = True
		else:
			medals = False
		write_config("show_medals", medals)
		if config["homescreen"] == True:
			write_config("homescreen_data", [])
			leaderboard_on_deck_browser()

	def import_list(self):
		showInfo("The text file must contain one name per line.")
		config = mw.addonManager.getConfig(__name__)
		fname = QFileDialog.getOpenFileName(self, 'Open file', "C:\\","Text files (*.txt)")
		try:
			file = open(fname[0], "r", encoding= "utf-8")
			friends_list = config["friends"]
			url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
			try:
				username_list = requests.get(url).json()
			except:
				username_list = []
				showWarning("Timeout error [import_list] - No internet connection, or server response took too long.", title="Leaderboard error")
			
			for name in file:
				name = name.replace("\n", "")
				if name in username_list and name not in config["friends"]:
					friends_list.append(name)
			
			if config["username"] and config["username"] not in friends_list:
				friends_list.append(config["username"])
			
			self.update_friends_list(sorted(friends_list, key=str.lower))
			write_config("friends", friends_list)
		except:
			showInfo("Please pick a text file to import friends.")

	def export_list(self):
		config = mw.addonManager.getConfig(__name__)
		friends_list = config["friends"]
		export_file = open(join(dirname(realpath(__file__)), "Friends.txt"), "w", encoding="utf-8" ) 
		for i in friends_list:
			export_file.write(i+"\n")
		export_file.close()
		tooltip("You can find the text file in the add-on folder.")

	def join_group(self):
		group = self.dialog.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		if group == "Join a group":
			group = "Custom"
		pwd = self.dialog.joinPwd.text()
		if pwd:
			pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
		else:
			pwd = None

		url = 'https://ankileaderboard.pythonanywhere.com/joinGroup/'
		data = {"username": config["username"], "group": group, "pwd": pwd, "token": config["token"]}
		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				tooltip(f"You joined {group}")
				write_config("subject", group)
				write_config("group_pwd", pwd)
				self.dialog.joinPwd.clear()
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [join_group] - No internet connection, or server response took too long.", title="Leaderboard error")

	def create_new_group(self):
		config = mw.addonManager.getConfig(__name__)
		Group_Name = self.dialog.newGroup.text()
		mail = self.dialog.mailGroup.text()
		pwd = self.dialog.newPwd.text()
		r_pwd = self.dialog.newRepeat.text()

		if pwd != r_pwd:
			showWarning("Passwords are not the same.")
			self.dialog.newPwd.clear()
			self.dialog.newRepeat.clear()
			return
		else:
			if pwd != "":
				pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
			else:
				pwd = None

		url = 'https://ankileaderboard.pythonanywhere.com/create_group/'
		data = {'Group_Name': Group_Name, "User": config['username'], "Mail": mail, "Pwd": pwd}
		
		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				showInfo(f"{Group_Name} was requested successfully. The developer has been informed. It will normally be approved within 24 hours.")
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [create_new_group] - No internet connection, or server response took too long.", title="Leaderboard error")		

	def manage_group(self):
		config = mw.addonManager.getConfig(__name__)
		group = self.dialog.manageGroup.currentText()
		oldPwd = self.dialog.oldPwd.text()
		newPwd = self.dialog.manage_newPwd.text()
		rPwd = self.dialog.manage_newRepeat.text()
		addAdmin = self.dialog.newAdmin.text()

		if newPwd != rPwd:
			showWarning("Passwords are not the same.")
			self.dialog.manage_newPwd.clear()
			self.dialog.manage_newRepeat.clear()
			return
		else:
			if oldPwd == "":
				oldPwd = None
			else:
				oldPwd = hashlib.sha1(oldPwd.encode('utf-8')).hexdigest().upper()
			
			if newPwd == "":
				newPwd = oldPwd
			else:
				newPwd = hashlib.sha1(newPwd.encode('utf-8')).hexdigest().upper()
			
		url = 'https://ankileaderboard.pythonanywhere.com/manageGroup/'
		data = {'group': group, "user": config["username"], "token": config["token"], "oldPwd": oldPwd, "newPwd": newPwd, "addAdmin": addAdmin}

		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				tooltip(f"{group} was updated successfully.")
				write_config("group_pwd", newPwd) if oldPwd != newPwd else write_config("group_pwd", oldPwd)
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [manage_group] - No internet connection, or server response took too long.", title="Leaderboard error")		

	def load_Group(self):
		config = mw.addonManager.getConfig(__name__)
		_translate = QtCore.QCoreApplication.translate
		url = 'https://ankileaderboard.pythonanywhere.com/groups/'
		try:
			Group_List = requests.get(url, timeout=20).json()
		except:
			Group_List = []
			showWarning("Timeout error [load_Group] - No internet connection, or server response took too long.", title="Leaderboard error")
		
		# item 0 is set by pyuic from the .ui file
		for i in range(1, len(Group_List) + 1):
			self.dialog.subject.addItem("")
			self.dialog.manageGroup.addItem("")

		index = 1
		for i in Group_List:
			self.dialog.subject.setItemText(index, _translate("Dialog", i))
			self.dialog.manageGroup.setItemText(index, _translate("Dialog", i))
			index += 1

		self.dialog.subject.setCurrentText(config["subject"])

	def status(self):
		config = mw.addonManager.getConfig(__name__)
		statusMsg = self.dialog.statusMsg.text()
		url = 'https://ankileaderboard.pythonanywhere.com/setStatus/'
		data = {"status": statusMsg, "username": config["username"], "Token_v3": config["token"]}
		
		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				tooltip("Done")
			else:
				tooltip(str(x.text))
		except:
			showWarning("Timeout error [status] - No internet connection, or server response took too long.", title="Leaderboard error")

	def update_hidden_list(self, hidden):
		config = mw.addonManager.getConfig(__name__)
		hiddenUsers = self.dialog.hiddenUsers
		hiddenUsers.clear()
		for user in hidden:
			hiddenUsers.addItem(user)

	def unhide(self):
		for item in self.dialog.hiddenUsers.selectedItems():
			username = item.text()
			config = mw.addonManager.getConfig(__name__)
			config['hidden_users'].remove(username)
			write_config("hidden_users", config["hidden_users"])
			tooltip(f"{username} is now back on the leaderboard")
			self.update_hidden_list(config["hidden_users"])