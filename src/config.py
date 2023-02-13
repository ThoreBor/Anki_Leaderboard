from datetime import datetime
from pathlib import Path
import hashlib
import json

from aqt import mw
from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from aqt.utils import tooltip, showInfo, showWarning, askUser

if qtmajor > 5:
	from ..forms.pyqt6UI import config
	from PyQt6 import QtCore
else:
	from ..forms.pyqt5UI import config
	from PyQt5 import QtCore
from .resetPassword import start_resetPassword
from .config_manager import write_config
from .version import version, about_text
from .api_connect import *

askUserCreateAccount = """
<h3>Sign-up</h3>
By signing up, you confirm that you read and accept the Privacy Policy of this add-on. 
You can read it <a href="https://ankileaderboard.pythonanywhere.com/privacy/">here</a>.
<br><br>
<b>Do you want to sign up now?</b>
"""

class start_config(QDialog):
	def __init__(self, season_start, season_end, parent=None):
		self.parent = parent
		self.season_start = season_start
		self.season_end = season_end
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = config.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setValues()
		self.connectSignals()
		self.loadGroup()
		self.loadStatus()
		self.accountAction()

	# General

	def connectSignals(self):
		self.dialog.account_button.clicked.connect(self.accountButton)
		self.dialog.account_forgot.clicked.connect(self.accountForgot)
		self.dialog.account_action.currentIndexChanged.connect(self.accountAction)
		self.dialog.account_mail.textChanged.connect(self.checkLineEdit)
		self.dialog.account_username.textChanged.connect(self.checkLineEdit)
		self.dialog.account_new_username.textChanged.connect(self.checkLineEdit)
		self.dialog.account_pwd.textChanged.connect(self.checkLineEdit)
		self.dialog.account_pwd_repeat.textChanged.connect(self.checkLineEdit)
		self.dialog.statusButton.clicked.connect(self.status)
		self.dialog.friend_username.returnPressed.connect(self.addFriend)
		self.dialog.add_friends_button.clicked.connect(self.addFriend)
		self.dialog.remove_friend_button.clicked.connect(self.removeFriend)
		self.dialog.newday.valueChanged.connect(self.setTime)
		self.dialog.joinGroup.clicked.connect(self.joinGroup)
		self.dialog.leaveGroup.clicked.connect(self.leaveGroup)
		self.dialog.add_newGroup.clicked.connect(self.createNewGroup)
		self.dialog.manageSave.clicked.connect(self.manageGroup)
		self.dialog.country.currentTextChanged.connect(self.setCountry)
		self.dialog.Default_Tab.currentTextChanged.connect(self.setDefaultTab)
		self.dialog.sortby.currentTextChanged.connect(self.setSortby)
		self.dialog.scroll.stateChanged.connect(self.setScroll)
		self.dialog.medals.stateChanged.connect(self.setMedals)
		self.dialog.import_friends.clicked.connect(self.importList)
		self.dialog.export_friends.clicked.connect(self.exportList)
		self.dialog.unhideButton.clicked.connect(self.unhide)
		self.dialog.LB_DeckBrowser.stateChanged.connect(self.setHomescreen)
		self.dialog.autosync.stateChanged.connect(self.setAutosync)
		self.dialog.maxUsers.valueChanged.connect(self.setMaxUser)
		self.dialog.lb_focus.stateChanged.connect(self.setFocus)

	def setValues(self):
		_translate = QtCore.QCoreApplication.translate
		config = mw.addonManager.getConfig(__name__)
		root = Path(__file__).parents[1]

		icon = QIcon()
		icon.addPixmap(QPixmap(f"{root}/designer/icons/settings.png"), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

		self.updateLoginInfo(config["username"])
		self.dialog.account_forgot.hide()
		self.dialog.newday.setValue(int(config['newday']))
		self.dialog.Default_Tab.setCurrentIndex(config['tab'])
		self.dialog.scroll.setChecked(bool(config["scroll"]))
		self.updateFriendsList(sorted(config["friends"], key=str.lower))
		self.updateHiddenList(sorted(config["hidden_users"], key=str.lower))
		self.updateGroupList(sorted(config["groups"], key=str.lower))
		self.dialog.LB_DeckBrowser.setChecked(bool(config["homescreen"]))
		self.dialog.autosync.setChecked(bool(config["autosync"]))
		self.dialog.maxUsers.setValue(config["maxUsers"])
		self.dialog.lb_focus.setChecked(bool(config["focus_on_user"]))
		self.dialog.medals.setChecked(bool(config["show_medals"]))
		self.dialog.about_text.setHtml(about_text)
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
		
		for i in range(1, 256):
			self.dialog.country.addItem("")
		country_list = ['Afghanistan', 'Åland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua & Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia & Herzegovina', 'Botswana', 'Brazil', 'British Indian Ocean Territory', 'British Virgin Islands', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Canary Islands', 'Cape Verde', 'Caribbean Netherlands', 'Cayman Islands', 'Central African Republic', 'Ceuta & Melilla', 'Chad', 'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo - Brazzaville', 'Congo - Kinshasa', 'Cook Islands', 'Costa Rica', 'Côte d’Ivoire', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czechia', 'Denmark', 'Diego Garcia', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Eurozone', 'Falkland Islands', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong SAR China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau SAR China', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territories', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn Islands', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russia', 'Rwanda', 'Samoa', 'San Marino', 'São Tomé & Príncipe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia & South Sandwich Islands', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'St. Barthélemy', 'St. Helena', 'St. Kitts & Nevis', 'St. Lucia', 'St. Martin', 'St. Pierre & Miquelon', 'St. Vincent & Grenadines', 'Sudan', 'Suriname', 'Svalbard & Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad & Tobago', 'Tristan da Cunha', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks & Caicos Islands', 'Tuvalu', 'U.S. Outlying Islands', 'U.S. Virgin Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United Nations', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Wallis & Futuna', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
		# item 0 is set by pyuic from the .ui file
		for i in country_list:
			self.dialog.country.setItemText(country_list.index(i), _translate("Dialog", i))

		self.dialog.country.setCurrentText(config["country"])
		
		if not config["authToken"]:
			self.dialog.tabWidget.setTabEnabled(2, False)

	def accountAction(self):
		self.dialog.account_mail.setText("")
		self.dialog.account_username.setText("")
		self.dialog.account_new_username.setText("")
		self.dialog.account_pwd.setText("")
		self.dialog.account_pwd_repeat.setText("")
		index = self.dialog.account_action.currentIndex()
		self.checkLineEdit()
		if index == 0:
			self.dialog.account_button.setText("Sign up")
			self.dialog.account_mail.show()
			self.dialog.account_username.show()
			self.dialog.account_new_username.hide()
			self.dialog.account_pwd.show()
			self.dialog.account_pwd_repeat.show()
			self.dialog.account_forgot.hide()
			self.dialog.account_username.setPlaceholderText("Username")
			self.dialog.account_button.setEnabled(False)
		if index == 1:
			self.dialog.account_button.setText("Log in")
			self.dialog.account_mail.hide()
			self.dialog.account_username.show()
			self.dialog.account_new_username.hide()
			self.dialog.account_pwd.show()
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.show()
			self.dialog.account_username.setPlaceholderText("Username")
			self.dialog.account_button.setEnabled(False)
		if index == 2:
			self.dialog.account_button.setText("Delete Account")
			self.dialog.account_mail.hide()
			self.dialog.account_username.show()
			self.dialog.account_new_username.hide()
			self.dialog.account_pwd.show()
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.show()
			self.dialog.account_username.setPlaceholderText("Username")
			self.dialog.account_button.setEnabled(False)
		if index == 3:
			self.dialog.account_button.setText("Log out")
			self.dialog.account_mail.hide()
			self.dialog.account_username.hide()
			self.dialog.account_new_username.hide()
			self.dialog.account_pwd.hide()
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.hide()
			self.dialog.account_button.setEnabled(True)
		if index == 4:
			self.dialog.account_button.setText("Change username")
			self.dialog.account_mail.hide()
			self.dialog.account_username.show()
			self.dialog.account_new_username.show()
			self.dialog.account_pwd.show()
			self.dialog.account_pwd_repeat.hide()
			self.dialog.account_forgot.show()
			self.dialog.account_username.setPlaceholderText("Username")
			self.dialog.account_button.setEnabled(False)

	def accountButton(self):
		index = self.dialog.account_action.currentIndex()
		if index == 0:
			self.signUp()
		if index == 1:
			self.logIn()
		if index == 2:
			self.deleteAccount()
		if index == 3:
			self.logOut()
		if index == 4:
			self.changeUsername()

	def checkLineEdit(self):
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		new_username = self.dialog.account_new_username.text()
		pwd = self.dialog.account_pwd.text()
		pwd_repeat = self.dialog.account_pwd_repeat.text()
		index = self.dialog.account_action.currentIndex()
		if index == 0 or index == 3:
			if email and username and pwd and pwd_repeat:
				if pwd == pwd_repeat:
					self.dialog.account_button.setEnabled(True)
					self.dialog.account_pwd_repeat.setStyleSheet("background-color: var(--window-bg)")
				if pwd != pwd_repeat:
					self.dialog.account_button.setEnabled(False)
					self.dialog.account_pwd_repeat.setStyleSheet("background-color: #ff4242")
			else:
				self.dialog.account_button.setEnabled(False)
		if index == 5:
			if username and pwd and new_username:
				self.dialog.account_button.setEnabled(True)
			else:
				self.dialog.account_button.setEnabled(False)
		if index == 1 or index == 2 or index == 4:
			if username and pwd:
				self.dialog.account_button.setEnabled(True)
			else:
				self.dialog.account_button.setEnabled(False)

	def updateLoginInfo(self, username):
		login_info = self.dialog.login_info_2
		if username:
			login_info.setText(f"Logged in as {username}.")
		else:
			login_info.setText("You are not logged in.")

	def updateFriendsList(self, friends):
		config = mw.addonManager.getConfig(__name__)
		friends_list = self.dialog.friends_list
		friends_list.clear()
		for friend in friends:
			if friend != config['username']:
				friends_list.addItem(friend)

	def updateGroupList(self, groups):
		group_list = self.dialog.group_list
		group_list.clear()
		for group in groups:
			group_list.addItem(group)
	
	# Account/API calls

	def signUp(self):
		email = self.dialog.account_mail.text()
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()

		if askUser(askUserCreateAccount):
			data = {"email": email, "username": username, "pwd": pwd, "syncDate": datetime.now(), "version": version}
			response = postRequest("signUp/", data, 201)
			if response:
				write_config("authToken", response.json())
				write_config("username", username)
				self.updateLoginInfo(username)
				tooltip("Successfully signed-up")
				self.dialog.tabWidget.setTabEnabled(2, True)
		else:
			pass	

	def logIn(self):
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		data = {"username": username, "pwd": pwd}
		
		response = postRequest("logIn/", data, 200)
		if response:
			write_config("authToken", response.json())
			write_config("username", username)
			self.updateLoginInfo(username)
			tooltip("Successfully logged-in")
			self.dialog.tabWidget.setTabEnabled(2, True)

	def deleteAccount(self):
		config = mw.addonManager.getConfig(__name__)
		username = self.dialog.account_username.text()
		pwd = self.dialog.account_pwd.text()
		if askUser("<h3>Deleting Account</h3>If you delete your account, all your data will be deleted. <br><br><b>Do you want to delete your account now?</b>"):
			data = {"username": username, "pwd": pwd}
			response = postRequest("deleteAccount/", data, 204)
			if response:
				write_config("authToken", None)
				write_config("username", "")
				self.updateLoginInfo("")
				tooltip("Successfully deleted account")
				self.dialog.tabWidget.setTabEnabled(2, False)

	def changeUsername(self):
		username = self.dialog.account_username.text()
		newUsername = self.dialog.account_new_username.text()
		pwd = self.dialog.account_pwd.text()

		if askUser("If someone added you as a friend, they will have to re-add you after you changed your username.<br><br><b>Do you want to proceed?</b>"):
			data = {"username": username,"newUsername": newUsername,"pwd": pwd}
			response = postRequest("changeUsername/", data, 200)
			if response:
				write_config("authToken", response.json())
				write_config("username", newUsername)
				self.updateLoginInfo(newUsername)
				tooltip("Successfully updated account")
		else:
			pass

	def logOut(self):
		write_config("authToken", None)
		write_config("username", "")
		self.updateLoginInfo("")
		tooltip("Successfully logged-out")
		self.dialog.tabWidget.setTabEnabled(2, False)

	def accountForgot(self):
		s = start_resetPassword()
		if s.exec():
			pass

	def loadGroup(self):
		config = mw.addonManager.getConfig(__name__)
		_translate = QtCore.QCoreApplication.translate
		groupList = getRequest("groups/")
		
		if groupList:
			# item 0 is set by pyuic from the .ui file
			for i in range(1, len(groupList.json()) + 1):
				self.dialog.subject.addItem("")
				self.dialog.manageGroup.addItem("")

			index = 1
			for i in groupList.json():
				self.dialog.subject.setItemText(index, _translate("Dialog", i))
				self.dialog.manageGroup.setItemText(index, _translate("Dialog", i))
				index += 1
			self.dialog.subject.setCurrentText(config["current_group"])

	def joinGroup(self):
		group = self.dialog.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		groupList = config["groups"]
		if group == "Join a group":
			return
		pwd = self.dialog.joinPwd.text()
		if pwd:
			pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
		else:
			pwd = None

		data = {"username": config["username"], "group": group, "pwd": pwd, "authToken": config["authToken"]}
		response = postRequest("joinGroup/", data, 200)
		if response:
			if not config["current_group"]:
				write_config("current_group", group)
			if group not in groupList:
				groupList.append(group)
				write_config("groups", groupList)
				self.updateGroupList(sorted(groupList, key=str.lower))
				tooltip(f"You joined {group}")
			self.dialog.joinPwd.clear()

	def leaveGroup(self):
		config = mw.addonManager.getConfig(__name__)
		for item in self.dialog.group_list.selectedItems():
			group = item.text()
			data = {"username": config["username"], "group": group, "authToken": config["authToken"]}
			response = postRequest("leaveGroup/", data, 200)
			if response:
				config['groups'].remove(group)
				write_config("groups", config["groups"])
				if len(config['groups']) > 0:
					write_config("current_group", config["groups"][0])
				else:
					write_config("current_group", None)
				self.updateGroupList(sorted(config["groups"], key=str.lower))
				tooltip(f"You left {group}.")

	def createNewGroup(self):
		config = mw.addonManager.getConfig(__name__)
		groupName = self.dialog.newGroup.text()
		pwd = self.dialog.newPwd.text()
		rpwd = self.dialog.newRepeat.text()

		if pwd != rpwd:
			showWarning("Passwords are not the same.")
			self.dialog.newPwd.clear()
			self.dialog.newRepeat.clear()
			return
		else:
			if pwd != "":
				pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
			else:
				pwd = None

		data = {'groupName': groupName, "username": config['username'], "pwd": pwd}
		response = postRequest("createGroup/", data, 200)
		if response:
			tooltip("Successfully created group. Re-open config.")
			self.dialog.newGroup.setText("")
			self.dialog.newPwd.setText("")
			self.dialog.newRepeat.setText("")

	def manageGroup(self):
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

		data = {'group': group, "username": config["username"], "authToken": config["authToken"], "oldPwd": oldPwd, "newPwd": newPwd, "addAdmin": addAdmin}
		response = postRequest("manageGroup/", data, 200)
		if response:
			tooltip(f"{group} was updated successfully.")
			self.dialog.oldPwd.setText("")
			self.dialog.manage_newPwd.setText("")
			self.dialog.manage_newRepeat.setText("")
			self.dialog.newAdmin.setText("")

	def status(self):
		config = mw.addonManager.getConfig(__name__)
		statusMsg = self.dialog.statusMsg.toPlainText()
		if len(statusMsg) > 280:
			showWarning("The message can only be 280 characters long.", title="Leaderboard")
			return
		data = {"status": statusMsg, "username": config["username"], "authToken": config["authToken"]}
		response = postRequest("setBio/", data, 200)
		if response:
			tooltip("Done")

	def loadStatus(self):
		config = mw.addonManager.getConfig(__name__)
		if config["username"]:
			response = postRequest("getBio/", {"username": config["username"]}, 200)
			if response:
				self.dialog.statusMsg.setText(response.json())
	
	# Change settings

	def addFriend(self):
		username = self.dialog.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		response = getRequest("users/")
		
		if response:
			username_list = response.json()
			if config['username'] and config['username'] not in config['friends']:
				config['friends'].append(config['username'])
			
			if username in username_list and username not in config['friends']:
				config['friends'].append(username)
				write_config("friends", config['friends'])
				tooltip(f"{username} is now your friend.")
				self.dialog.friend_username.setText("")
				self.updateFriendsList(sorted(config["friends"], key=str.lower))
			else:
				tooltip("Couldn't find friend")

	def removeFriend(self):
		for item in self.dialog.friends_list.selectedItems():
			username = item.text()
			config = mw.addonManager.getConfig(__name__)
			config['friends'].remove(username)
			write_config("friends", config["friends"])
			tooltip(f"{username} was removed from your friendlist")
			self.updateFriendsList(sorted(config["friends"], key=str.lower))

	def setTime(self):
		beginning_of_new_day = self.dialog.newday.value()
		write_config("newday", beginning_of_new_day)

	def setCountry(self):
		country = self.dialog.country.currentText()
		write_config("country", country)

	def setScroll(self):
		if self.dialog.scroll.isChecked():
			scroll = True
		else:
			scroll = False
		write_config("scroll", scroll)
	
	def setDefaultTab(self):
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
			tooltip("Changes will apply after the next sync")

	def setSortby(self):
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
			tooltip("Changes will apply after the next sync")

	def setHomescreen(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.LB_DeckBrowser.isChecked():
			homescreen = True
		else:
			homescreen = False
		write_config("homescreen", homescreen)
		tooltip("Changes will apply after the next sync")

	def setMaxUser(self):
		config = mw.addonManager.getConfig(__name__)
		maxUsers = self.dialog.maxUsers.value()
		write_config("maxUsers", maxUsers)
		if config["homescreen"] == True:
			tooltip("Changes will apply after the next sync")

	def setAutosync(self):
		if self.dialog.autosync.isChecked():
			autosync = True
		else:
			autosync = False
		write_config("autosync", autosync)

	def setFocus(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.lb_focus.isChecked():
			focus = True
		else:
			focus = False
		write_config("focus_on_user", focus)
		if config["homescreen"] == True:
			tooltip("Changes will apply after the next sync")

	def setMedals(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.medals.isChecked():
			medals = True
		else:
			medals = False
		write_config("show_medals", medals)
		if config["homescreen"] == True:
			write_config("homescreen_data", [])
			tooltip("Changes will apply after the next sync")

	def importList(self):
		showInfo("The text file must contain one name per line.")
		config = mw.addonManager.getConfig(__name__)
		fname = QFileDialog.getOpenFileName(self, 'Open file', "C:\\","Text files (*.txt)")
		try:
			file = open(fname[0], "r", encoding= "utf-8")
			friends_list = config["friends"]
			response = getRequest("users/")
			
			if response:
				response = response.json()
				for name in file:
					name = name.replace("\n", "")
					if name in username_list and name not in config["friends"]:
						friends_list.append(name)
				
				if config["username"] and config["username"] not in friends_list:
					friends_list.append(config["username"])
				
				self.updateFriendsList(sorted(friends_list, key=str.lower))
				write_config("friends", friends_list)
		except:
			showInfo("Please pick a text file to import friends.")

	def exportList(self):
		config = mw.addonManager.getConfig(__name__)
		friends_list = config["friends"]
		export_file = open(join(dirname(realpath(__file__)), "Friends.txt"), "w", encoding="utf-8") 
		for i in friends_list:
			export_file.write(i+"\n")
		export_file.close()
		tooltip("You can find the text file in the add-on folder.")
			
	def updateHiddenList(self, hidden):
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
