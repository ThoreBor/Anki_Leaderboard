from datetime import datetime
from os.path import dirname, join, realpath

import hashlib
from PyQt5 import QtCore

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo, showWarning, askUser

from .forms import setup
from .Stats import Stats
from .config_manager import write_config
from .lb_on_homescreen import leaderboard_on_deck_browser
from .version import version, about_text
from .api_connect import connectToAPI

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
		self.dialog.account_forgot.hide()
		self.dialog.newday.setValue(int(config['newday']))
		self.dialog.Default_Tab.setCurrentIndex(config['tab'])
		self.dialog.scroll.setChecked(bool(config["scroll"]))
		self.dialog.refresh.setChecked(bool(config["refresh"]))
		self.update_friends_list(sorted(config["friends"], key=str.lower))
		self.update_hidden_list(sorted(config["hidden_users"], key=str.lower))
		self.update_group_list(sorted(config["groups"], key=str.lower))
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
		self.dialog.newday.setToolTip("This needs to be the same as in Ankis' preferences.")
		self.dialog.autosync.setToolTip("It will take a few extra seconds before you return to the homescreen after answering the last due card in a deck.")
		self.load_Group()
		self.load_status()

		_translate = QtCore.QCoreApplication.translate

		for i in range(1, 256):
			self.dialog.country.addItem("")

		country_list = ['Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil', 'British Indian Ocean Territory', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Canary Islands', 'Cape Verde', 'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic', 'Ceuta & Melilla', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo - Brazzaville', 'Congo - Kinshasa', 'Cook Islands', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czechia', 'Denmark', 'Diego Garcia', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Eurozone', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau SAR China', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territories', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'San Marino', 'São Tomé & Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia & South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Barthélemy', 'St. Helena', 'St. Kitts & Nevis', 'St. Lucia', 'St. Martin', 'St. Pierre & Miquelon', 'St. Vincent & Grenadines', 'Sudan', 'Suriname', 'Svalbard & Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad & Tobago', 'Tristan da Cunha', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks & Caicos Islands', 'Tuvalu', 'U.S. Outlying Islands', 'U.S. Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United Nations', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis & Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
		
		# item 0 is set by pyuic from the .ui file
		for i in country_list:
			self.dialog.country.setItemText(country_list.index(i), _translate("Dialog", i))

		self.dialog.country.setCurrentText(config["country"])

		self.dialog.account_button.clicked.connect(self.account_button)
		self.dialog.account_forgot.clicked.connect(self.account_forgot)
		self.dialog.account_action.currentIndexChanged.connect(self.account_action)
		self.dialog.account_mail.textChanged.connect(self.check_lineEdit)
		self.dialog.account_username.textChanged.connect(self.check_lineEdit)
		self.dialog.account_pwd.textChanged.connect(self.check_lineEdit)
		self.dialog.account_pwd_repeat.textChanged.connect(self.check_lineEdit)
		self.dialog.statusButton.clicked.connect(self.status)
		self.dialog.friend_username.returnPressed.connect(self.add_friend)
		self.dialog.add_friends_button.clicked.connect(self.add_friend)
		self.dialog.remove_friend_button.clicked.connect(self.remove_friend)
		self.dialog.newday.valueChanged.connect(self.set_time)
		self.dialog.joinGroup.clicked.connect(self.join_group)
		self.dialog.leaveGroup.clicked.connect(self.leave_group)
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

		self.dialog.about_text.setHtml(about_text)

	def account_action(self):
		index = self.dialog.account_action.currentIndex()
		self.check_lineEdit()
		if index == 0:
			self.dialog.account_button.setText("Sign-up")
			self.dialog.account_pwd_repeat.show()
			self.dialog.account_forgot.hide()
		if index == 1:
			self.dialog.account_button.setText("Log-in")
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.show()
		if index == 2:
			self.dialog.account_button.setText("Delete Account")
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.show()
		if index == 3:
			self.dialog.account_button.setText("Update Account")
			self.dialog.account_pwd_repeat.show()
			self.dialog.account_forgot.hide()
			self.dialog.account_username.setPlaceholderText("Username of your existing account")

	def account_button(self):
		index = self.dialog.account_action.currentIndex()
		if index == 0:
			self.sign_up()
		if index == 1:
			self.log_in()
		if index == 2:
			self.delete_account()
		if index == 3:
			self.update_account()

	def check_lineEdit(self):
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		pwd_repeat = self.dialog.account_pwd_repeat.text()
		index = self.dialog.account_action.currentIndex()
		if index == 0 or index == 3:
			if email and username:
				self.dialog.account_button.setEnabled(True)
				if pwd == pwd_repeat and pwd:
					self.dialog.account_button.setEnabled(True)
					self.dialog.account_pwd_repeat.setStyleSheet("background-color: #ffffff")
				if pwd != pwd_repeat and pwd:
					self.dialog.account_button.setEnabled(False)
					self.dialog.account_pwd_repeat.setStyleSheet("background-color: #ff4242")
				if not pwd:
					self.dialog.account_button.setEnabled(False)
			else:
				self.dialog.account_button.setEnabled(False)
		else:
			if email and username and pwd:
				self.dialog.account_button.setEnabled(True)
			else:
				self.dialog.account_button.setEnabled(False)

	def sign_up(self):
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		username_list = connectToAPI("allusers/", True, {}, False, "sign_up")

		if username in username_list:
			showWarning("This username is already taken")
			return
		if askUser("By creating an account, you agree that your email address will be saved on Firebase. It will only be used to be able to reset your password."):
			data = {"email": email, "username": username, "pwd": pwd, "sync_date": datetime.now(), "version": version}
			response = connectToAPI("signUp/", True, data, False, "sign_up")
			if response == "Firebase error":
				showWarning("Email address already exists, or password is too short.")
			else:
				write_config("firebaseToken", response)
				write_config("username", username)
				self.update_login_info(username)
				tooltip("Successfully signed-up")
		else:
			pass		

	def log_in(self):
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		data = {"email": email, "username": username, "pwd": pwd}
		response = connectToAPI("logIn/", True, data, False, "log_in")
		if response == "Firebase error":
			showWarning("Something went wrong.")
		else:
			write_config("firebaseToken", response)
			write_config("username", username)
			self.update_login_info(username)
			tooltip("Successfully logged-in")

	def delete_account(self):
		config = mw.addonManager.getConfig(__name__)
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		firebaseToken = config["firebaseToken"]
		data = {"email": email, "username": username, "pwd": pwd, "firebaseToken": firebaseToken}
		response = connectToAPI("deleteAccount/", False, data, "Deleted", "delete_account")
		if response.text == "Deleted":
			write_config("firebaseToken", None)
			write_config("username", "")
			self.update_login_info(username)
			tooltip("Successfully deleted account")

	def update_account(self):
		config = mw.addonManager.getConfig(__name__)
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		firebaseToken = config["firebaseToken"]
		if askUser("By creating an account, you agree that your email address will be saved on Firebase. It will only be used to be able to reset your password."):
			data = {"email": email, "username": username, "pwd": pwd, "firebaseToken": firebaseToken}
			response = connectToAPI("updateAccount/", True, data, False, "update_account")
			if "error" in response:
				showWarning(response)
			else:
				write_config("firebaseToken", response)
				write_config("username", username)
				self.update_login_info(username)
				tooltip("Successfully updated account")
		else:	
			pass		

	def account_forgot(self):
		email = self.dialog.account_mail.text()
		if not email:
			showWarning("Please enter your email address.")
			return
		response = connectToAPI("resetPassword/", True, {"email": email}, False, "account_forgot")
		if response == "Firebase error":
			showWarning("Something went wrong")
		else:
			tooltip("Email sent")
	
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

	def update_group_list(self, groups):
		group_list = self.dialog.group_list
		group_list.clear()
		for group in groups:
			group_list.addItem(group)

	def add_friend(self):
		username = self.dialog.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		username_list = connectToAPI("allusers/", True, {}, False, "add_friend")
		
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

	def remove_friend(self):
		for item in self.dialog.friends_list.selectedItems():
			username = item.text()
			config = mw.addonManager.getConfig(__name__)
			config['friends'].remove(username)
			write_config("friends", config["friends"])
			tooltip(f"{username} was removed from your friendlist")
			self.update_friends_list(sorted(config["friends"], key=str.lower))

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
			username_list = connectToAPI("allusers/", True, {}, False, "import_list")
			
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
		export_file = open(join(dirname(realpath(__file__)), "Friends.txt"), "w", encoding="utf-8") 
		for i in friends_list:
			export_file.write(i+"\n")
		export_file.close()
		tooltip("You can find the text file in the add-on folder.")

	def join_group(self):
		group = self.dialog.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		group_list = config["groups"]
		if group == "Join a group":
			group = "Custom"
		pwd = self.dialog.joinPwd.text()
		if pwd:
			pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
		else:
			pwd = None

		data = {"username": config["username"], "group": group, "pwd": pwd, "firebaseToken": config["firebaseToken"]}
		x = connectToAPI("joinGroup/", False, data, "Done!", "join_group")
		if x.text == "Done!":
			tooltip(f"You joined {group}")
			if not config["current_group"]:
				write_config("current_group", group)
			if group not in group_list:
				group_pwds = config["group_pwds"]
				if pwd:
					group_pwds.append(pwd)
					write_config("group_pwds", group_pwds)
				else:
					group_pwds.append(None)
				write_config("group_pwds", group_pwds)
				group_list.append(group)
				write_config("groups", group_list)
				self.update_group_list(sorted(group_list, key=str.lower))
			self.dialog.joinPwd.clear()

	def leave_group(self):
		for item in self.dialog.group_list.selectedItems():
			group = item.text()
			config = mw.addonManager.getConfig(__name__)
			group_pwds = config["group_pwds"]
			data = {"user": config["username"], "group": group, "firebaseToken": config["firebaseToken"]}
			x = connectToAPI("leaveGroup/", False, data, "Done!", "leave_group")
			if x.text == "Done!":
				group_pwds.remove(group_pwds[config["groups"].index(group)])
				write_config("group_pwds", group_pwds)
				config['groups'].remove(group)
				write_config("groups", config["groups"])
				if len(config['groups']) > 0:
					write_config("current_group", config["groups"][0])
				else:
					write_config("current_group", None)
				self.update_group_list(sorted(config["groups"], key=str.lower))
				tooltip(f"You left {group}.")

	def create_new_group(self):
		config = mw.addonManager.getConfig(__name__)
		Group_Name = self.dialog.newGroup.text()
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

		data = {'Group_Name': Group_Name, "User": config['username'], "Pwd": pwd}
		x = connectToAPI("create_group/", False, data, "Done!", "create_new_group")
		if x.text == "Done!":
			tooltip("Successfully created group. Re-open config.")
			self.dialog.newGroup.setText("")
			self.dialog.newPwd.setText("")
			self.dialog.newRepeat.setText("")

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

		data = {'group': group, "user": config["username"], "firebaseToken": config["firebaseToken"], "oldPwd": oldPwd, "newPwd": newPwd, "addAdmin": addAdmin}
		x = connectToAPI("manageGroup/", False, data, "Done!", "manage_group")
		if x.text == "Done!":
			tooltip(f"{group} was updated successfully.")
			config["group_pwds"][config["groups"].index(group)] = newPwd if oldPwd != newPwd else oldPwd
			write_config("group_pwds", config["group_pwds"])
			self.dialog.oldPwd.setText("")
			self.dialog.manage_newPwd.setText("")
			self.dialog.manage_newRepeat.setText("")
			self.dialog.newAdmin.setText("")
			

	def load_Group(self):
		config = mw.addonManager.getConfig(__name__)
		_translate = QtCore.QCoreApplication.translate
		Group_List = connectToAPI("groups/", True, {}, False, "load_Group")
		
		# item 0 is set by pyuic from the .ui file
		for i in range(1, len(Group_List) + 1):
			self.dialog.subject.addItem("")
			self.dialog.manageGroup.addItem("")

		index = 1
		for i in Group_List:
			self.dialog.subject.setItemText(index, _translate("Dialog", i))
			self.dialog.manageGroup.setItemText(index, _translate("Dialog", i))
			index += 1
		self.dialog.subject.setCurrentText(config["current_group"])

	def status(self):
		config = mw.addonManager.getConfig(__name__)
		statusMsg = self.dialog.statusMsg.toPlainText()
		if len(statusMsg) > 280:
			showWarning("The message can only be 280 characters long.", title="Leaderboard")
			return
		data = {"status": statusMsg, "username": config["username"], "Token_v3": config["token"]}
		x = connectToAPI("setStatus/", False, data, "Done!", "status")
		if x.text == "Done!":
			tooltip("Done")

	def load_status(self):
		config = mw.addonManager.getConfig(__name__)
		if config["username"]:
			status = connectToAPI("getStatus/", True, {"username": config["username"]}, False, "load_status")
			self.dialog.statusMsg.setText(status[0])

			
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