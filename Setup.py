from datetime import date, datetime
from os.path import dirname, join, realpath

import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo, showWarning

from .forms import setup
from .Leaderboard import start_main
from .Stats import Stats

class start_setup(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = setup.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		config = mw.addonManager.getConfig(__name__)
		config4 = int(config['newday'])
		config5 = config["subject"]
		config6 = config["country"]

		self.update_login_info(config["username"])
		self.dialog.newday.setValue(config4)
		self.dialog.subject.setCurrentText(config5)
		self.dialog.scroll.setChecked(bool(config["scroll"]))
		self.dialog.refresh.setChecked(bool(config["refresh"]))
		self.update_friends_list(sorted(config["friends"], key=str.lower))

		for i in range(1, 256):
			self.dialog.country.addItem("")

		_translate = QtCore.QCoreApplication.translate
		# item 0 is set by pyuic from the .ui file
		self.dialog.country.setItemText(1, _translate("Dialog", "Afghanistan"))
		self.dialog.country.setItemText(2, _translate("Dialog", "Åland Islands"))
		self.dialog.country.setItemText(3, _translate("Dialog", "Albania"))
		self.dialog.country.setItemText(4, _translate("Dialog", "Algeria"))
		self.dialog.country.setItemText(5, _translate("Dialog", "American Samoa"))
		self.dialog.country.setItemText(6, _translate("Dialog", "Andorra"))
		self.dialog.country.setItemText(7, _translate("Dialog", "Angola"))
		self.dialog.country.setItemText(8, _translate("Dialog", "Anguilla"))
		self.dialog.country.setItemText(9, _translate("Dialog", "Antarctica"))
		self.dialog.country.setItemText(10, _translate("Dialog", "Antigua & Barbuda"))
		self.dialog.country.setItemText(11, _translate("Dialog", "Argentina"))
		self.dialog.country.setItemText(12, _translate("Dialog", "Armenia"))
		self.dialog.country.setItemText(13, _translate("Dialog", "Aruba"))
		self.dialog.country.setItemText(14, _translate("Dialog", "Ascension Island"))
		self.dialog.country.setItemText(15, _translate("Dialog", "Australia"))
		self.dialog.country.setItemText(16, _translate("Dialog", "Austria"))
		self.dialog.country.setItemText(17, _translate("Dialog", "Azerbaijan"))
		self.dialog.country.setItemText(18, _translate("Dialog", "Bahamas"))
		self.dialog.country.setItemText(19, _translate("Dialog", "Bahrain"))
		self.dialog.country.setItemText(20, _translate("Dialog", "Bangladesh"))
		self.dialog.country.setItemText(21, _translate("Dialog", "Barbados"))
		self.dialog.country.setItemText(22, _translate("Dialog", "Belarus"))
		self.dialog.country.setItemText(23, _translate("Dialog", "Belgium"))
		self.dialog.country.setItemText(24, _translate("Dialog", "Belize"))
		self.dialog.country.setItemText(25, _translate("Dialog", "Benin"))
		self.dialog.country.setItemText(26, _translate("Dialog", "Bermuda"))
		self.dialog.country.setItemText(27, _translate("Dialog", "Bhutan"))
		self.dialog.country.setItemText(28, _translate("Dialog", "Bolivia"))
		self.dialog.country.setItemText(29, _translate("Dialog", "Bosnia & Herzegovina"))
		self.dialog.country.setItemText(30, _translate("Dialog", "Botswana"))
		self.dialog.country.setItemText(31, _translate("Dialog", "Brazil"))
		self.dialog.country.setItemText(32, _translate("Dialog", "British Indian Ocean Territory"))
		self.dialog.country.setItemText(33, _translate("Dialog", "British Virgin Islands"))
		self.dialog.country.setItemText(34, _translate("Dialog", "Brunei"))
		self.dialog.country.setItemText(35, _translate("Dialog", "Bulgaria"))
		self.dialog.country.setItemText(36, _translate("Dialog", "Burkina Faso"))
		self.dialog.country.setItemText(37, _translate("Dialog", "Burundi"))
		self.dialog.country.setItemText(38, _translate("Dialog", "Cambodia"))
		self.dialog.country.setItemText(39, _translate("Dialog", "Cameroon"))
		self.dialog.country.setItemText(40, _translate("Dialog", "Canada"))
		self.dialog.country.setItemText(41, _translate("Dialog", "Canary Islands"))
		self.dialog.country.setItemText(42, _translate("Dialog", "Cape Verde"))
		self.dialog.country.setItemText(43, _translate("Dialog", "Caribbean Netherlands"))
		self.dialog.country.setItemText(44, _translate("Dialog", "Cayman Islands"))
		self.dialog.country.setItemText(45, _translate("Dialog", "Central African Republic"))
		self.dialog.country.setItemText(46, _translate("Dialog", "Ceuta & Melilla"))
		self.dialog.country.setItemText(47, _translate("Dialog", "Chad"))
		self.dialog.country.setItemText(48, _translate("Dialog", "Chile"))
		self.dialog.country.setItemText(49, _translate("Dialog", "China"))
		self.dialog.country.setItemText(50, _translate("Dialog", "Christmas Island"))
		self.dialog.country.setItemText(51, _translate("Dialog", "Cocos (Keeling) Islands"))
		self.dialog.country.setItemText(52, _translate("Dialog", "Colombia"))
		self.dialog.country.setItemText(53, _translate("Dialog", "Comoros"))
		self.dialog.country.setItemText(54, _translate("Dialog", "Congo - Brazzaville"))
		self.dialog.country.setItemText(55, _translate("Dialog", "Congo - Kinshasa"))
		self.dialog.country.setItemText(56, _translate("Dialog", "Cook Islands"))
		self.dialog.country.setItemText(57, _translate("Dialog", "Costa Rica"))
		self.dialog.country.setItemText(58, _translate("Dialog", "Côte d’Ivoire"))
		self.dialog.country.setItemText(59, _translate("Dialog", "Croatia"))
		self.dialog.country.setItemText(60, _translate("Dialog", "Cuba"))
		self.dialog.country.setItemText(61, _translate("Dialog", "Curaçao"))
		self.dialog.country.setItemText(62, _translate("Dialog", "Cyprus"))
		self.dialog.country.setItemText(63, _translate("Dialog", "Czechia"))
		self.dialog.country.setItemText(64, _translate("Dialog", "Denmark"))
		self.dialog.country.setItemText(65, _translate("Dialog", "Diego Garcia"))
		self.dialog.country.setItemText(66, _translate("Dialog", "Djibouti"))
		self.dialog.country.setItemText(67, _translate("Dialog", "Dominica"))
		self.dialog.country.setItemText(68, _translate("Dialog", "Dominican Republic"))
		self.dialog.country.setItemText(69, _translate("Dialog", "Ecuador"))
		self.dialog.country.setItemText(70, _translate("Dialog", "Egypt"))
		self.dialog.country.setItemText(71, _translate("Dialog", "El Salvador"))
		self.dialog.country.setItemText(72, _translate("Dialog", "Equatorial Guinea"))
		self.dialog.country.setItemText(73, _translate("Dialog", "Eritrea"))
		self.dialog.country.setItemText(74, _translate("Dialog", "Estonia"))
		self.dialog.country.setItemText(75, _translate("Dialog", "Ethiopia"))
		self.dialog.country.setItemText(76, _translate("Dialog", "Eurozone"))
		self.dialog.country.setItemText(77, _translate("Dialog", "Falkland Islands"))
		self.dialog.country.setItemText(78, _translate("Dialog", "Faroe Islands"))
		self.dialog.country.setItemText(79, _translate("Dialog", "Fiji"))
		self.dialog.country.setItemText(80, _translate("Dialog", "Finland"))
		self.dialog.country.setItemText(81, _translate("Dialog", "France"))
		self.dialog.country.setItemText(82, _translate("Dialog", "French Guiana"))
		self.dialog.country.setItemText(83, _translate("Dialog", "French Polynesia"))
		self.dialog.country.setItemText(84, _translate("Dialog", "French Southern Territories"))
		self.dialog.country.setItemText(85, _translate("Dialog", "Gabon"))
		self.dialog.country.setItemText(86, _translate("Dialog", "Gambia"))
		self.dialog.country.setItemText(87, _translate("Dialog", "Georgia"))
		self.dialog.country.setItemText(88, _translate("Dialog", "Germany"))
		self.dialog.country.setItemText(89, _translate("Dialog", "Ghana"))
		self.dialog.country.setItemText(90, _translate("Dialog", "Gibraltar"))
		self.dialog.country.setItemText(91, _translate("Dialog", "Greece"))
		self.dialog.country.setItemText(92, _translate("Dialog", "Greenland"))
		self.dialog.country.setItemText(93, _translate("Dialog", "Grenada"))
		self.dialog.country.setItemText(94, _translate("Dialog", "Guadeloupe"))
		self.dialog.country.setItemText(95, _translate("Dialog", "Guam"))
		self.dialog.country.setItemText(96, _translate("Dialog", "Guatemala"))
		self.dialog.country.setItemText(97, _translate("Dialog", "Guernsey"))
		self.dialog.country.setItemText(98, _translate("Dialog", "Guinea"))
		self.dialog.country.setItemText(99, _translate("Dialog", "Guinea-Bissau"))
		self.dialog.country.setItemText(100, _translate("Dialog", "Guyana"))
		self.dialog.country.setItemText(101, _translate("Dialog", "Haiti"))
		self.dialog.country.setItemText(102, _translate("Dialog", "Honduras"))
		self.dialog.country.setItemText(103, _translate("Dialog", "Hong Kong SAR China"))
		self.dialog.country.setItemText(104, _translate("Dialog", "Hungary"))
		self.dialog.country.setItemText(105, _translate("Dialog", "Iceland"))
		self.dialog.country.setItemText(106, _translate("Dialog", "India"))
		self.dialog.country.setItemText(107, _translate("Dialog", "Indonesia"))
		self.dialog.country.setItemText(108, _translate("Dialog", "Iran"))
		self.dialog.country.setItemText(109, _translate("Dialog", "Iraq"))
		self.dialog.country.setItemText(110, _translate("Dialog", "Ireland"))
		self.dialog.country.setItemText(111, _translate("Dialog", "Isle of Man"))
		self.dialog.country.setItemText(112, _translate("Dialog", "Israel"))
		self.dialog.country.setItemText(113, _translate("Dialog", "Italy"))
		self.dialog.country.setItemText(114, _translate("Dialog", "Jamaica"))
		self.dialog.country.setItemText(115, _translate("Dialog", "Japan"))
		self.dialog.country.setItemText(116, _translate("Dialog", "Jersey"))
		self.dialog.country.setItemText(117, _translate("Dialog", "Jordan"))
		self.dialog.country.setItemText(118, _translate("Dialog", "Kazakhstan"))
		self.dialog.country.setItemText(119, _translate("Dialog", "Kenya"))
		self.dialog.country.setItemText(120, _translate("Dialog", "Kiribati"))
		self.dialog.country.setItemText(121, _translate("Dialog", "Kosovo"))
		self.dialog.country.setItemText(122, _translate("Dialog", "Kuwait"))
		self.dialog.country.setItemText(123, _translate("Dialog", "Kyrgyzstan"))
		self.dialog.country.setItemText(124, _translate("Dialog", "Laos"))
		self.dialog.country.setItemText(125, _translate("Dialog", "Latvia"))
		self.dialog.country.setItemText(126, _translate("Dialog", "Lebanon"))
		self.dialog.country.setItemText(127, _translate("Dialog", "Lesotho"))
		self.dialog.country.setItemText(128, _translate("Dialog", "Liberia"))
		self.dialog.country.setItemText(129, _translate("Dialog", "Libya"))
		self.dialog.country.setItemText(130, _translate("Dialog", "Liechtenstein"))
		self.dialog.country.setItemText(131, _translate("Dialog", "Lithuania"))
		self.dialog.country.setItemText(132, _translate("Dialog", "Luxembourg"))
		self.dialog.country.setItemText(133, _translate("Dialog", "Macau SAR China"))
		self.dialog.country.setItemText(134, _translate("Dialog", "Macedonia"))
		self.dialog.country.setItemText(135, _translate("Dialog", "Madagascar"))
		self.dialog.country.setItemText(136, _translate("Dialog", "Malawi"))
		self.dialog.country.setItemText(137, _translate("Dialog", "Malaysia"))
		self.dialog.country.setItemText(138, _translate("Dialog", "Maldives"))
		self.dialog.country.setItemText(139, _translate("Dialog", "Mali"))
		self.dialog.country.setItemText(140, _translate("Dialog", "Malta"))
		self.dialog.country.setItemText(141, _translate("Dialog", "Marshall Islands"))
		self.dialog.country.setItemText(142, _translate("Dialog", "Martinique"))
		self.dialog.country.setItemText(143, _translate("Dialog", "Mauritania"))
		self.dialog.country.setItemText(144, _translate("Dialog", "Mauritius"))
		self.dialog.country.setItemText(145, _translate("Dialog", "Mayotte"))
		self.dialog.country.setItemText(146, _translate("Dialog", "Mexico"))
		self.dialog.country.setItemText(147, _translate("Dialog", "Micronesia"))
		self.dialog.country.setItemText(148, _translate("Dialog", "Moldova"))
		self.dialog.country.setItemText(149, _translate("Dialog", "Monaco"))
		self.dialog.country.setItemText(150, _translate("Dialog", "Mongolia"))
		self.dialog.country.setItemText(151, _translate("Dialog", "Montenegro"))
		self.dialog.country.setItemText(152, _translate("Dialog", "Montserrat"))
		self.dialog.country.setItemText(153, _translate("Dialog", "Morocco"))
		self.dialog.country.setItemText(154, _translate("Dialog", "Mozambique"))
		self.dialog.country.setItemText(155, _translate("Dialog", "Myanmar (Burma)"))
		self.dialog.country.setItemText(156, _translate("Dialog", "Namibia"))
		self.dialog.country.setItemText(157, _translate("Dialog", "Nauru"))
		self.dialog.country.setItemText(158, _translate("Dialog", "Nepal"))
		self.dialog.country.setItemText(159, _translate("Dialog", "Netherlands"))
		self.dialog.country.setItemText(160, _translate("Dialog", "New Caledonia"))
		self.dialog.country.setItemText(161, _translate("Dialog", "New Zealand"))
		self.dialog.country.setItemText(162, _translate("Dialog", "Nicaragua"))
		self.dialog.country.setItemText(163, _translate("Dialog", "Niger"))
		self.dialog.country.setItemText(164, _translate("Dialog", "Nigeria"))
		self.dialog.country.setItemText(165, _translate("Dialog", "Niue"))
		self.dialog.country.setItemText(166, _translate("Dialog", "Norfolk Island"))
		self.dialog.country.setItemText(167, _translate("Dialog", "North Korea"))
		self.dialog.country.setItemText(168, _translate("Dialog", "Northern Mariana Islands"))
		self.dialog.country.setItemText(169, _translate("Dialog", "Norway"))
		self.dialog.country.setItemText(170, _translate("Dialog", "Oman"))
		self.dialog.country.setItemText(171, _translate("Dialog", "Pakistan"))
		self.dialog.country.setItemText(172, _translate("Dialog", "Palau"))
		self.dialog.country.setItemText(173, _translate("Dialog", "Palestinian Territories"))
		self.dialog.country.setItemText(174, _translate("Dialog", "Panama"))
		self.dialog.country.setItemText(175, _translate("Dialog", "Papua New Guinea"))
		self.dialog.country.setItemText(176, _translate("Dialog", "Paraguay"))
		self.dialog.country.setItemText(177, _translate("Dialog", "Peru"))
		self.dialog.country.setItemText(178, _translate("Dialog", "Philippines"))
		self.dialog.country.setItemText(179, _translate("Dialog", "Pitcairn Islands"))
		self.dialog.country.setItemText(180, _translate("Dialog", "Poland"))
		self.dialog.country.setItemText(181, _translate("Dialog", "Portugal"))
		self.dialog.country.setItemText(182, _translate("Dialog", "Puerto Rico"))
		self.dialog.country.setItemText(183, _translate("Dialog", "Qatar"))
		self.dialog.country.setItemText(184, _translate("Dialog", "Réunion"))
		self.dialog.country.setItemText(185, _translate("Dialog", "Romania"))
		self.dialog.country.setItemText(186, _translate("Dialog", "Russia"))
		self.dialog.country.setItemText(187, _translate("Dialog", "Rwanda"))
		self.dialog.country.setItemText(188, _translate("Dialog", "Samoa"))
		self.dialog.country.setItemText(189, _translate("Dialog", "San Marino"))
		self.dialog.country.setItemText(190, _translate("Dialog", "São Tomé & Príncipe"))
		self.dialog.country.setItemText(191, _translate("Dialog", "Saudi Arabia"))
		self.dialog.country.setItemText(192, _translate("Dialog", "Senegal"))
		self.dialog.country.setItemText(193, _translate("Dialog", "Serbia"))
		self.dialog.country.setItemText(194, _translate("Dialog", "Seychelles"))
		self.dialog.country.setItemText(195, _translate("Dialog", "Sierra Leone"))
		self.dialog.country.setItemText(196, _translate("Dialog", "Singapore"))
		self.dialog.country.setItemText(197, _translate("Dialog", "Sint Maarten"))
		self.dialog.country.setItemText(198, _translate("Dialog", "Slovakia"))
		self.dialog.country.setItemText(199, _translate("Dialog", "Slovenia"))
		self.dialog.country.setItemText(200, _translate("Dialog", "Solomon Islands"))
		self.dialog.country.setItemText(201, _translate("Dialog", "Somalia"))
		self.dialog.country.setItemText(202, _translate("Dialog", "South Africa"))
		self.dialog.country.setItemText(203, _translate("Dialog", "South Georgia & South Sandwich Islands"))
		self.dialog.country.setItemText(204, _translate("Dialog", "South Korea"))
		self.dialog.country.setItemText(205, _translate("Dialog", "South Sudan"))
		self.dialog.country.setItemText(206, _translate("Dialog", "Spain"))
		self.dialog.country.setItemText(207, _translate("Dialog", "Sri Lanka"))
		self.dialog.country.setItemText(208, _translate("Dialog", "St. Barthélemy"))
		self.dialog.country.setItemText(209, _translate("Dialog", "St. Helena"))
		self.dialog.country.setItemText(210, _translate("Dialog", "St. Kitts & Nevis"))
		self.dialog.country.setItemText(211, _translate("Dialog", "St. Lucia"))
		self.dialog.country.setItemText(212, _translate("Dialog", "St. Martin"))
		self.dialog.country.setItemText(213, _translate("Dialog", "St. Pierre & Miquelon"))
		self.dialog.country.setItemText(214, _translate("Dialog", "St. Vincent & Grenadines"))
		self.dialog.country.setItemText(215, _translate("Dialog", "Sudan"))
		self.dialog.country.setItemText(216, _translate("Dialog", "Suriname"))
		self.dialog.country.setItemText(217, _translate("Dialog", "Svalbard & Jan Mayen"))
		self.dialog.country.setItemText(218, _translate("Dialog", "Swaziland"))
		self.dialog.country.setItemText(219, _translate("Dialog", "Sweden"))
		self.dialog.country.setItemText(220, _translate("Dialog", "Switzerland"))
		self.dialog.country.setItemText(221, _translate("Dialog", "Syria"))
		self.dialog.country.setItemText(222, _translate("Dialog", "Taiwan"))
		self.dialog.country.setItemText(223, _translate("Dialog", "Tajikistan"))
		self.dialog.country.setItemText(224, _translate("Dialog", "Tanzania"))
		self.dialog.country.setItemText(225, _translate("Dialog", "Thailand"))
		self.dialog.country.setItemText(226, _translate("Dialog", "Timor-Leste"))
		self.dialog.country.setItemText(227, _translate("Dialog", "Togo"))
		self.dialog.country.setItemText(228, _translate("Dialog", "Tokelau"))
		self.dialog.country.setItemText(229, _translate("Dialog", "Tonga"))
		self.dialog.country.setItemText(230, _translate("Dialog", "Trinidad & Tobago"))
		self.dialog.country.setItemText(231, _translate("Dialog", "Tristan da Cunha"))
		self.dialog.country.setItemText(232, _translate("Dialog", "Tunisia"))
		self.dialog.country.setItemText(233, _translate("Dialog", "Turkey"))
		self.dialog.country.setItemText(234, _translate("Dialog", "Turkmenistan"))
		self.dialog.country.setItemText(235, _translate("Dialog", "Turks & Caicos Islands"))
		self.dialog.country.setItemText(236, _translate("Dialog", "Tuvalu"))
		self.dialog.country.setItemText(237, _translate("Dialog", "U.S. Outlying Islands"))
		self.dialog.country.setItemText(238, _translate("Dialog", "U.S. Virgin Islands"))
		self.dialog.country.setItemText(239, _translate("Dialog", "Uganda"))
		self.dialog.country.setItemText(240, _translate("Dialog", "Ukraine"))
		self.dialog.country.setItemText(241, _translate("Dialog", "United Arab Emirates"))
		self.dialog.country.setItemText(242, _translate("Dialog", "United Kingdom"))
		self.dialog.country.setItemText(243, _translate("Dialog", "United Nations"))
		self.dialog.country.setItemText(244, _translate("Dialog", "United States"))
		self.dialog.country.setItemText(245, _translate("Dialog", "Uruguay"))
		self.dialog.country.setItemText(246, _translate("Dialog", "Uzbekistan"))
		self.dialog.country.setItemText(247, _translate("Dialog", "Vanuatu"))
		self.dialog.country.setItemText(248, _translate("Dialog", "Vatican City"))
		self.dialog.country.setItemText(249, _translate("Dialog", "Venezuela"))
		self.dialog.country.setItemText(250, _translate("Dialog", "Vietnam"))
		self.dialog.country.setItemText(251, _translate("Dialog", "Wallis & Futuna"))
		self.dialog.country.setItemText(252, _translate("Dialog", "Western Sahara"))
		self.dialog.country.setItemText(253, _translate("Dialog", "Yemen"))
		self.dialog.country.setItemText(254, _translate("Dialog", "Zambia"))
		self.dialog.country.setItemText(255, _translate("Dialog", "Zimbabwe"))

		self.dialog.country.setCurrentText(config6)

		self.dialog.create_username.returnPressed.connect(self.create_account)
		self.dialog.create_button.clicked.connect(self.create_account)
		self.dialog.login_username.returnPressed.connect(self.login)
		self.dialog.login_button.clicked.connect(self.login)
		self.dialog.delete_username.returnPressed.connect(self.delete)
		self.dialog.delete_button.clicked.connect(self.delete)
		self.dialog.friend_username.returnPressed.connect(self.add_friend)
		self.dialog.add_friends_button.clicked.connect(self.add_friend)
		self.dialog.remove_friend_button.clicked.connect(self.remove_friend)
		self.dialog.newday.valueChanged.connect(self.set_time)
		self.dialog.subject.currentTextChanged.connect(self.set_subject)
		self.dialog.country.currentTextChanged.connect(self.set_country)
		self.dialog.scroll.stateChanged.connect(self.set_scroll)
		self.dialog.refresh.stateChanged.connect(self.set_refresh)
		self.dialog.import_friends.clicked.connect(self.import_list)
		self.dialog.export_friends.clicked.connect(self.export_list)

		self.dialog.next_day_info1.setText(_translate("Dialog", "Next day starts"))
		self.dialog.next_day_info2.setText(_translate("Dialog", "hours past midnight"))

		for button in self.dialog.buttonBox.buttons():
			button.setAutoDefault(False)

		about_text = """
<h3>Anki Leaderboard v1.4.6</h3>
The code for the add-on is available on <a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub.</a> 
It is licensed under the <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/LICENSE">MIT License.</a> 
If you like this add-on, rate and review it on <a href="https://ankiweb.net/shared/info/41708974">Anki Web.</a><br>
<div>Crown icon made by <a href="https://www.flaticon.com/de/autoren/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<div>Person icon made by <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div>
<h3>Change Log:</h3>
- Added retention to stats <br>
- Bug fixes<br><br>
<b>© Thore Tyborski 2020<br>
With contributions from <a href="https://github.com/khonkhortisan">khonkhortisan</a> and  <a href="https://github.com/zjosua">zjosua.</a></b>
"""

		self.dialog.about_text.setHtml(about_text)

	def create_account(self):
		username = self.dialog.create_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
		try:
			username_list = requests.get(url).json()
		except:
			showWarning("Make sure you're connected to the internet.")

		if username in username_list:
			tooltip("Username already taken")
		else:
			url = 'https://ankileaderboard.pythonanywhere.com/sync/'
			streak, cards, time, cards_past_30_days, retention = Stats()
			data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.now(), "Month": cards_past_30_days, 
			"Subject": config["subject"], "Country": config["country"], "Retention": retention}
			x = requests.post(url, data = data)

			config = {"new_user": "False", "username": username, "friends": config['friends'], "newday": config["newday"], 
			"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
			tooltip("Successfully created account.")
			self.dialog.create_username.setText("")
			self.update_login_info(username)

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
			username_list = requests.get(url).json()
		except:
			showWarning("Make sure you're connected to the internet.")

		if username in username_list:
			config = {"new_user": "False", "username": username, "friends": config['friends'], "newday": config["newday"], 
			"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
			tooltip("Successfully logged in.")
			self.dialog.login_username.setText("")
			self.update_login_info(username)
		else:
			tooltip("Account doesn't exist.")


	def delete(self):
		username = self.dialog.delete_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/delete/'
		data = {'Username': username}
		try:
			x = requests.post(url, data = data)
		except:
			showWarning("Make sure you're connected to the internet.")

		if x.text == "Deleted":
			config = {"new_user": "True", "username": "", "friends": config['friends'], "newday": config["newday"], 
			"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
			tooltip("Successfully deleted account.")
			self.dialog.delete_username.setText("")
		else:
			tooltip("Error")


	def add_friend(self):
		username = self.dialog.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/allusers/'
		try:
			username_list = requests.get(url).json()
		except:
			showWarning("Make sure you're connected to the internet.")

		if config['username'] and config['username'] not in config['friends']:
			config['friends'].append(config['username'])
		
		if username in username_list and username not in config['friends']:
			config['friends'].append(username)
			config = {"new_user": config['new_user'],"username": config['username'], "friends": config['friends'], "newday": config['newday'], "country": config['country'], "subject": config['subject'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(username + " is now your friend.")
			self.dialog.friend_username.setText("")
			self.update_friends_list(sorted(config["friends"], key=str.lower))
		else:
			tooltip("Couldn't find friend")

	def remove_friend(self):
		for item in self.dialog.friends_list.selectedItems():
			username = item.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config3.remove(username)
			config = {"new_user": config['new_user'], "username": config['username'], "friends": config3, "newday": config["newday"], 
			"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(f"{username} was removed from your friendlist")
			self.update_friends_list(config["friends"])

	def set_time(self):
		beginning_of_new_day = self.dialog.newday.value()
		config = mw.addonManager.getConfig(__name__)
		config = {"new_user": config['new_user'], "username": config['username'], "friends": config['friends'], "newday": str(beginning_of_new_day), 
		"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
		mw.addonManager.writeConfig(__name__, config)

	def set_subject(self):
		subject = self.dialog.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		if subject == "Join a group":
			subject = "Custom"
		config = {"new_user": config['new_user'], "username": config['username'], "friends": config['friends'], "newday": config['newday'], 
		"subject": subject, "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
		mw.addonManager.writeConfig(__name__, config)

	def set_country(self):
		country = self.dialog.country.currentText()
		config = mw.addonManager.getConfig(__name__)
		config = {"new_user": config['new_user'], "username": config['username'], "friends": config['friends'], "newday": config['newday'], 
		"subject": config['subject'], "country": country, "scroll": config['scroll'], "refresh": config["refresh"]}
		mw.addonManager.writeConfig(__name__, config)

	def set_scroll(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.scroll.isChecked():
			scroll = "True"
		else:
			scroll = ""
		config = {"new_user": config['new_user'], "username": config['username'], "friends": config['friends'], "newday": config['newday'], 
		"subject": config['subject'], "country": config['country'], "scroll": scroll, "refresh": config["refresh"]}
		mw.addonManager.writeConfig(__name__, config)

	def set_refresh(self):
		config = mw.addonManager.getConfig(__name__)
		if self.dialog.refresh.isChecked():
			refresh = "True"
		else:
			refresh = ""
		config = {"new_user": config['new_user'], "username": config['username'], "friends": config['friends'], "newday": config['newday'], 
		"subject": config['subject'], "country": config['country'], "scroll": config["scroll"], "refresh": refresh}
		mw.addonManager.writeConfig(__name__, config)


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
				showWarning("Make sure you're connected to the internet.")
			
			for name in file:
				name = name.replace("\n", "")
				if name in username_list and name not in config["friends"]:
					friends_list.append(name)
			
			if config["username"] and config["username"] not in friends_list:
				friends_list.append(config["username"])
			
			self.update_friends_list(sorted(friends_list, key=str.lower))
			config = {"new_user": config['new_user'], "username": config['username'], "friends": friends_list, "newday": config['newday'], 
			"subject": config['subject'], "country": config['country'], "scroll": config['scroll'], "refresh": config["refresh"]}
			mw.addonManager.writeConfig(__name__, config)
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