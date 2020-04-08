from aqt.qt import *
from aqt import mw
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from os.path import dirname, join, realpath
from aqt.utils import tooltip
from datetime import date, datetime
from .Stats import Stats
from .Leaderboard import start_main

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(569, 240)
		Dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
		Dialog.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'person.png')))
		Dialog.setFixedSize(Dialog.size())
		Dialog.resize(568, 240)
		self.Accout = QtWidgets.QGroupBox(Dialog)
		self.Accout.setGeometry(QtCore.QRect(10, 0, 261, 231))
		self.Accout.setObjectName("Accout")
		self.layoutWidget = QtWidgets.QWidget(self.Accout)
		self.layoutWidget.setGeometry(QtCore.QRect(11, 21, 241, 201))
		self.layoutWidget.setObjectName("layoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.create_info = QtWidgets.QLabel(self.layoutWidget)
		self.create_info.setObjectName("create_info")
		self.gridLayout.addWidget(self.create_info, 0, 0, 1, 1)
		self.create_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.create_username.setText("")
		self.create_username.setMaxLength(10)
		self.create_username.setObjectName("create_username")
		self.gridLayout.addWidget(self.create_username, 1, 0, 1, 1)
		self.create_button = QtWidgets.QPushButton(self.layoutWidget)
		self.create_button.setObjectName("create_button")
		self.gridLayout.addWidget(self.create_button, 1, 1, 1, 1)
		self.login_info = QtWidgets.QLabel(self.layoutWidget)
		self.login_info.setObjectName("login_info")
		self.gridLayout.addWidget(self.login_info, 2, 0, 1, 1)
		self.login_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.login_username.setText("")
		self.login_username.setMaxLength(10)
		self.login_username.setObjectName("login_username")
		self.gridLayout.addWidget(self.login_username, 3, 0, 1, 1)
		self.login_button = QtWidgets.QPushButton(self.layoutWidget)
		self.login_button.setObjectName("login_button")
		self.gridLayout.addWidget(self.login_button, 3, 1, 1, 1)
		self.delete_info = QtWidgets.QLabel(self.layoutWidget)
		self.delete_info.setObjectName("delete_info")
		self.gridLayout.addWidget(self.delete_info, 4, 0, 1, 1)
		self.delete_username = QtWidgets.QLineEdit(self.layoutWidget)
		self.delete_username.setText("")
		self.delete_username.setMaxLength(10)
		self.delete_username.setObjectName("delete_username")
		self.gridLayout.addWidget(self.delete_username, 5, 0, 1, 1)
		self.delete_button = QtWidgets.QPushButton(self.layoutWidget)
		self.delete_button.setObjectName("delete_button")
		self.gridLayout.addWidget(self.delete_button, 5, 1, 1, 1)
		self.Friends = QtWidgets.QGroupBox(Dialog)
		self.Friends.setGeometry(QtCore.QRect(280, 0, 279, 141))
		self.Friends.setObjectName("Friends")
		self.layoutWidget1 = QtWidgets.QWidget(self.Friends)
		self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 261, 111))
		self.layoutWidget1.setObjectName("layoutWidget1")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.add_friends_info = QtWidgets.QLabel(self.layoutWidget1)
		self.add_friends_info.setObjectName("add_friends_info")
		self.gridLayout_2.addWidget(self.add_friends_info, 0, 0, 1, 1)
		self.friend_username = QtWidgets.QLineEdit(self.layoutWidget1)
		self.friend_username.setText("")
		self.friend_username.setMaxLength(10)
		self.friend_username.setObjectName("friend_username")
		self.gridLayout_2.addWidget(self.friend_username, 1, 0, 1, 1)
		self.add_friends_button = QtWidgets.QPushButton(self.layoutWidget1)
		self.add_friends_button.setObjectName("add_friends_button")
		self.gridLayout_2.addWidget(self.add_friends_button, 1, 1, 1, 1)
		self.remove_friend_info = QtWidgets.QLabel(self.layoutWidget1)
		self.remove_friend_info.setObjectName("remove_friend_info")
		self.gridLayout_2.addWidget(self.remove_friend_info, 2, 0, 1, 1)
		self.remove_friend_username = QtWidgets.QLineEdit(self.layoutWidget1)
		self.remove_friend_username.setText("")
		self.remove_friend_username.setMaxLength(10)
		self.remove_friend_username.setObjectName("remove_friend_username")
		self.gridLayout_2.addWidget(self.remove_friend_username, 3, 0, 1, 1)
		self.remove_friend_button = QtWidgets.QPushButton(self.layoutWidget1)
		self.remove_friend_button.setObjectName("remove_friend_button")
		self.gridLayout_2.addWidget(self.remove_friend_button, 3, 1, 1, 1)
		self.layoutWidget2 = QtWidgets.QWidget(Dialog)
		self.layoutWidget2.setGeometry(QtCore.QRect(280, 150, 281, 81))
		self.layoutWidget2.setObjectName("layoutWidget2")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget2)
		self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.newday = QtWidgets.QSpinBox(self.layoutWidget2)
		self.newday.setMaximum(23)
		self.newday.setObjectName("newday")
		self.gridLayout_4.addWidget(self.newday, 2, 1, 1, 1)
		self.subject = QtWidgets.QComboBox(self.layoutWidget2)
		self.subject.setObjectName("subject")
		self.subject.addItem("")
		self.subject.addItem("")
		self.subject.addItem("")
		self.subject.addItem("")
		self.gridLayout_4.addWidget(self.subject, 0, 0, 1, 3)
		self.next_day_info2 = QtWidgets.QLabel(self.layoutWidget2)
		self.next_day_info2.setObjectName("next_day_info2")
		self.gridLayout_4.addWidget(self.next_day_info2, 2, 2, 1, 1)
		self.next_day_info1 = QtWidgets.QLabel(self.layoutWidget2)
		self.next_day_info1.setObjectName("next_day_info1")
		self.gridLayout_4.addWidget(self.next_day_info1, 2, 0, 1, 1)
		self.country = QtWidgets.QComboBox(self.layoutWidget2)
		self.country.setObjectName("country")
		for i in range(0, 255):
			self.country.addItem("")
		self.gridLayout_4.addWidget(self.country, 1, 0, 1, 3)

		self.create_button.clicked.connect(self.create_account)
		self.login_button.clicked.connect(self.login)
		self.delete_button.clicked.connect(self.delete)
		self.add_friends_button.clicked.connect(self.add_friend)
		self.remove_friend_button.clicked.connect(self.remove_friend)
		self.newday.valueChanged.connect(self.set_time)
		self.subject.currentTextChanged.connect(self.set_subject)
		self.country.currentTextChanged.connect(self.set_country)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate

		config = mw.addonManager.getConfig(__name__)
		config4 = int(config['newday'])
		config5 = config["subject"]
		config6 = config["country"]
		self.newday.setValue(config4)

		Dialog.setWindowTitle(_translate("Dialog", "Config"))
		self.Accout.setTitle(_translate("Dialog", "Account"))
		self.create_info.setText(_translate("Dialog", "Create Account:"))
		self.create_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.create_button.setText(_translate("Dialog", "Create Account"))
		self.login_info.setText(_translate("Dialog", "Login:"))
		self.login_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.login_button.setText(_translate("Dialog", "Login"))
		self.delete_info.setText(_translate("Dialog", "Delete Account:"))
		self.delete_username.setPlaceholderText(_translate("Dialog", "Username"))
		self.delete_button.setText(_translate("Dialog", "Delete Account"))
		self.Friends.setTitle(_translate("Dialog", "Friends"))
		self.add_friends_info.setText(_translate("Dialog", "Add Friend:"))
		self.friend_username.setPlaceholderText(_translate("Dialog", "Friend"))
		self.add_friends_button.setText(_translate("Dialog", "Add Friend"))
		self.remove_friend_info.setText(_translate("Dialog", "Remove Friend:"))
		self.remove_friend_username.setPlaceholderText(_translate("Dialog", "Friend"))
		self.remove_friend_button.setText(_translate("Dialog", "Remove Friend"))
		
		self.subject.setItemText(0, _translate("Dialog", "What are you studying?"))
		self.subject.setItemText(1, _translate("Dialog", "Languages"))
		self.subject.setItemText(2, _translate("Dialog", "Medicine"))
		self.subject.setItemText(3, _translate("Dialog", "Law"))
		self.subject.setCurrentText(config5)
		
		self.country.setItemText(0, _translate("Dialog", "Country"))
		self.country.setItemText(1, _translate("Dialog", "Afghanistan"))
		self.country.setItemText(2, _translate("Dialog", "Åland Islands"))
		self.country.setItemText(3, _translate("Dialog", "Albania"))
		self.country.setItemText(4, _translate("Dialog", "Algeria"))
		self.country.setItemText(5, _translate("Dialog", "American Samoa"))
		self.country.setItemText(6, _translate("Dialog", "Andorra"))
		self.country.setItemText(7, _translate("Dialog", "Angola"))
		self.country.setItemText(8, _translate("Dialog", "Anguilla"))
		self.country.setItemText(9, _translate("Dialog", "Antarctica"))
		self.country.setItemText(10, _translate("Dialog", "Antigua & Barbuda"))
		self.country.setItemText(11, _translate("Dialog", "Argentina"))
		self.country.setItemText(12, _translate("Dialog", "Armenia"))
		self.country.setItemText(13, _translate("Dialog", "Aruba"))
		self.country.setItemText(14, _translate("Dialog", "Ascension Island"))
		self.country.setItemText(15, _translate("Dialog", "Australia"))
		self.country.setItemText(16, _translate("Dialog", "Austria"))
		self.country.setItemText(17, _translate("Dialog", "Azerbaijan"))
		self.country.setItemText(18, _translate("Dialog", "Bahamas"))
		self.country.setItemText(19, _translate("Dialog", "Bahrain"))
		self.country.setItemText(20, _translate("Dialog", "Bangladesh"))
		self.country.setItemText(21, _translate("Dialog", "Barbados"))
		self.country.setItemText(22, _translate("Dialog", "Belarus"))
		self.country.setItemText(23, _translate("Dialog", "Belgium"))
		self.country.setItemText(24, _translate("Dialog", "Belize"))
		self.country.setItemText(25, _translate("Dialog", "Benin"))
		self.country.setItemText(26, _translate("Dialog", "Bermuda"))
		self.country.setItemText(27, _translate("Dialog", "Bhutan"))
		self.country.setItemText(28, _translate("Dialog", "Bolivia"))
		self.country.setItemText(29, _translate("Dialog", "Bosnia & Herzegovina"))
		self.country.setItemText(30, _translate("Dialog", "Botswana"))
		self.country.setItemText(31, _translate("Dialog", "Brazil"))
		self.country.setItemText(32, _translate("Dialog", "British Indian Ocean Territory"))
		self.country.setItemText(33, _translate("Dialog", "British Virgin Islands"))
		self.country.setItemText(34, _translate("Dialog", "Brunei"))
		self.country.setItemText(35, _translate("Dialog", "Bulgaria"))
		self.country.setItemText(36, _translate("Dialog", "Burkina Faso"))
		self.country.setItemText(37, _translate("Dialog", "Burundi"))
		self.country.setItemText(38, _translate("Dialog", "Cambodia"))
		self.country.setItemText(39, _translate("Dialog", "Cameroon"))
		self.country.setItemText(40, _translate("Dialog", "Canada"))
		self.country.setItemText(41, _translate("Dialog", "Canary Islands"))
		self.country.setItemText(42, _translate("Dialog", "Cape Verde"))
		self.country.setItemText(43, _translate("Dialog", "Caribbean Netherlands"))
		self.country.setItemText(44, _translate("Dialog", "Cayman Islands"))
		self.country.setItemText(45, _translate("Dialog", "Central African Republic"))
		self.country.setItemText(46, _translate("Dialog", "Ceuta & Melilla"))
		self.country.setItemText(47, _translate("Dialog", "Chad"))
		self.country.setItemText(48, _translate("Dialog", "Chile"))
		self.country.setItemText(49, _translate("Dialog", "China"))
		self.country.setItemText(50, _translate("Dialog", "Christmas Island"))
		self.country.setItemText(51, _translate("Dialog", "Cocos (Keeling) Islands"))
		self.country.setItemText(52, _translate("Dialog", "Colombia"))
		self.country.setItemText(53, _translate("Dialog", "Comoros"))
		self.country.setItemText(54, _translate("Dialog", "Congo - Brazzaville"))
		self.country.setItemText(55, _translate("Dialog", "Congo - Kinshasa"))
		self.country.setItemText(56, _translate("Dialog", "Cook Islands"))
		self.country.setItemText(57, _translate("Dialog", "Costa Rica"))
		self.country.setItemText(58, _translate("Dialog", "Côte d’Ivoire"))
		self.country.setItemText(59, _translate("Dialog", "Croatia"))
		self.country.setItemText(60, _translate("Dialog", "Cuba"))
		self.country.setItemText(61, _translate("Dialog", "Curaçao"))
		self.country.setItemText(62, _translate("Dialog", "Cyprus"))
		self.country.setItemText(63, _translate("Dialog", "Czechia"))
		self.country.setItemText(64, _translate("Dialog", "Denmark"))
		self.country.setItemText(65, _translate("Dialog", "Diego Garcia"))
		self.country.setItemText(66, _translate("Dialog", "Djibouti"))
		self.country.setItemText(67, _translate("Dialog", "Dominica"))
		self.country.setItemText(68, _translate("Dialog", "Dominican Republic"))
		self.country.setItemText(69, _translate("Dialog", "Ecuador"))
		self.country.setItemText(70, _translate("Dialog", "Egypt"))
		self.country.setItemText(71, _translate("Dialog", "El Salvador"))
		self.country.setItemText(72, _translate("Dialog", "Equatorial Guinea"))
		self.country.setItemText(73, _translate("Dialog", "Eritrea"))
		self.country.setItemText(74, _translate("Dialog", "Estonia"))
		self.country.setItemText(75, _translate("Dialog", "Ethiopia"))
		self.country.setItemText(76, _translate("Dialog", "Eurozone"))
		self.country.setItemText(77, _translate("Dialog", "Falkland Islands"))
		self.country.setItemText(78, _translate("Dialog", "Faroe Islands"))
		self.country.setItemText(79, _translate("Dialog", "Fiji"))
		self.country.setItemText(80, _translate("Dialog", "Finland"))
		self.country.setItemText(81, _translate("Dialog", "France"))
		self.country.setItemText(82, _translate("Dialog", "French Guiana"))
		self.country.setItemText(83, _translate("Dialog", "French Polynesia"))
		self.country.setItemText(84, _translate("Dialog", "French Southern Territories"))
		self.country.setItemText(85, _translate("Dialog", "Gabon"))
		self.country.setItemText(86, _translate("Dialog", "Gambia"))
		self.country.setItemText(87, _translate("Dialog", "Georgia"))
		self.country.setItemText(88, _translate("Dialog", "Germany"))
		self.country.setItemText(89, _translate("Dialog", "Ghana"))
		self.country.setItemText(90, _translate("Dialog", "Gibraltar"))
		self.country.setItemText(91, _translate("Dialog", "Greece"))
		self.country.setItemText(92, _translate("Dialog", "Greenland"))
		self.country.setItemText(93, _translate("Dialog", "Grenada"))
		self.country.setItemText(94, _translate("Dialog", "Guadeloupe"))
		self.country.setItemText(95, _translate("Dialog", "Guam"))
		self.country.setItemText(96, _translate("Dialog", "Guatemala"))
		self.country.setItemText(97, _translate("Dialog", "Guernsey"))
		self.country.setItemText(98, _translate("Dialog", "Guinea"))
		self.country.setItemText(99, _translate("Dialog", "Guinea-Bissau"))
		self.country.setItemText(100, _translate("Dialog", "Guyana"))
		self.country.setItemText(101, _translate("Dialog", "Haiti"))
		self.country.setItemText(102, _translate("Dialog", "Honduras"))
		self.country.setItemText(103, _translate("Dialog", "Hong Kong SAR China"))
		self.country.setItemText(104, _translate("Dialog", "Hungary"))
		self.country.setItemText(105, _translate("Dialog", "Iceland"))
		self.country.setItemText(106, _translate("Dialog", "India"))
		self.country.setItemText(107, _translate("Dialog", "Indonesia"))
		self.country.setItemText(108, _translate("Dialog", "Iran"))
		self.country.setItemText(109, _translate("Dialog", "Iraq"))
		self.country.setItemText(110, _translate("Dialog", "Ireland"))
		self.country.setItemText(111, _translate("Dialog", "Isle of Man"))
		self.country.setItemText(112, _translate("Dialog", "Israel"))
		self.country.setItemText(113, _translate("Dialog", "Italy"))
		self.country.setItemText(114, _translate("Dialog", "Jamaica"))
		self.country.setItemText(115, _translate("Dialog", "Japan"))
		self.country.setItemText(116, _translate("Dialog", "Jersey"))
		self.country.setItemText(117, _translate("Dialog", "Jordan"))
		self.country.setItemText(118, _translate("Dialog", "Kazakhstan"))
		self.country.setItemText(119, _translate("Dialog", "Kenya"))
		self.country.setItemText(120, _translate("Dialog", "Kiribati"))
		self.country.setItemText(121, _translate("Dialog", "Kosovo"))
		self.country.setItemText(122, _translate("Dialog", "Kuwait"))
		self.country.setItemText(123, _translate("Dialog", "Kyrgyzstan"))
		self.country.setItemText(124, _translate("Dialog", "Laos"))
		self.country.setItemText(125, _translate("Dialog", "Latvia"))
		self.country.setItemText(126, _translate("Dialog", "Lebanon"))
		self.country.setItemText(127, _translate("Dialog", "Lesotho"))
		self.country.setItemText(128, _translate("Dialog", "Liberia"))
		self.country.setItemText(129, _translate("Dialog", "Libya"))
		self.country.setItemText(130, _translate("Dialog", "Liechtenstein"))
		self.country.setItemText(131, _translate("Dialog", "Lithuania"))
		self.country.setItemText(132, _translate("Dialog", "Luxembourg"))
		self.country.setItemText(133, _translate("Dialog", "Macau SAR China"))
		self.country.setItemText(134, _translate("Dialog", "Macedonia"))
		self.country.setItemText(135, _translate("Dialog", "Madagascar"))
		self.country.setItemText(136, _translate("Dialog", "Malawi"))
		self.country.setItemText(137, _translate("Dialog", "Malaysia"))
		self.country.setItemText(138, _translate("Dialog", "Maldives"))
		self.country.setItemText(139, _translate("Dialog", "Mali"))
		self.country.setItemText(140, _translate("Dialog", "Malta"))
		self.country.setItemText(141, _translate("Dialog", "Marshall Islands"))
		self.country.setItemText(142, _translate("Dialog", "Martinique"))
		self.country.setItemText(143, _translate("Dialog", "Mauritania"))
		self.country.setItemText(144, _translate("Dialog", "Mauritius"))
		self.country.setItemText(145, _translate("Dialog", "Mayotte"))
		self.country.setItemText(146, _translate("Dialog", "Mexico"))
		self.country.setItemText(147, _translate("Dialog", "Micronesia"))
		self.country.setItemText(148, _translate("Dialog", "Moldova"))
		self.country.setItemText(149, _translate("Dialog", "Monaco"))
		self.country.setItemText(150, _translate("Dialog", "Mongolia"))
		self.country.setItemText(151, _translate("Dialog", "Montenegro"))
		self.country.setItemText(152, _translate("Dialog", "Montserrat"))
		self.country.setItemText(153, _translate("Dialog", "Morocco"))
		self.country.setItemText(154, _translate("Dialog", "Mozambique"))
		self.country.setItemText(155, _translate("Dialog", "Myanmar (Burma)"))
		self.country.setItemText(156, _translate("Dialog", "Namibia"))
		self.country.setItemText(157, _translate("Dialog", "Nauru"))
		self.country.setItemText(158, _translate("Dialog", "Nepal"))
		self.country.setItemText(159, _translate("Dialog", "Netherlands"))
		self.country.setItemText(160, _translate("Dialog", "New Caledonia"))
		self.country.setItemText(161, _translate("Dialog", "New Zealand"))
		self.country.setItemText(162, _translate("Dialog", "Nicaragua"))
		self.country.setItemText(163, _translate("Dialog", "Niger"))
		self.country.setItemText(164, _translate("Dialog", "Nigeria"))
		self.country.setItemText(165, _translate("Dialog", "Niue"))
		self.country.setItemText(166, _translate("Dialog", "Norfolk Island"))
		self.country.setItemText(167, _translate("Dialog", "North Korea"))
		self.country.setItemText(168, _translate("Dialog", "Northern Mariana Islands"))
		self.country.setItemText(169, _translate("Dialog", "Norway"))
		self.country.setItemText(170, _translate("Dialog", "Oman"))
		self.country.setItemText(171, _translate("Dialog", "Pakistan"))
		self.country.setItemText(172, _translate("Dialog", "Palau"))
		self.country.setItemText(173, _translate("Dialog", "Palestinian Territories"))
		self.country.setItemText(174, _translate("Dialog", "Panama"))
		self.country.setItemText(175, _translate("Dialog", "Papua New Guinea"))
		self.country.setItemText(176, _translate("Dialog", "Paraguay"))
		self.country.setItemText(177, _translate("Dialog", "Peru"))
		self.country.setItemText(178, _translate("Dialog", "Philippines"))
		self.country.setItemText(179, _translate("Dialog", "Pitcairn Islands"))
		self.country.setItemText(180, _translate("Dialog", "Poland"))
		self.country.setItemText(181, _translate("Dialog", "Portugal"))
		self.country.setItemText(182, _translate("Dialog", "Puerto Rico"))
		self.country.setItemText(183, _translate("Dialog", "Qatar"))
		self.country.setItemText(184, _translate("Dialog", "Réunion"))
		self.country.setItemText(185, _translate("Dialog", "Romania"))
		self.country.setItemText(186, _translate("Dialog", "Russia"))
		self.country.setItemText(187, _translate("Dialog", "Rwanda"))
		self.country.setItemText(188, _translate("Dialog", "Samoa"))
		self.country.setItemText(189, _translate("Dialog", "San Marino"))
		self.country.setItemText(190, _translate("Dialog", "São Tomé & Príncipe"))
		self.country.setItemText(191, _translate("Dialog", "Saudi Arabia"))
		self.country.setItemText(192, _translate("Dialog", "Senegal"))
		self.country.setItemText(193, _translate("Dialog", "Serbia"))
		self.country.setItemText(194, _translate("Dialog", "Seychelles"))
		self.country.setItemText(195, _translate("Dialog", "Sierra Leone"))
		self.country.setItemText(196, _translate("Dialog", "Singapore"))
		self.country.setItemText(197, _translate("Dialog", "Sint Maarten"))
		self.country.setItemText(198, _translate("Dialog", "Slovakia"))
		self.country.setItemText(199, _translate("Dialog", "Slovenia"))
		self.country.setItemText(200, _translate("Dialog", "Solomon Islands"))
		self.country.setItemText(201, _translate("Dialog", "Somalia"))
		self.country.setItemText(202, _translate("Dialog", "South Africa"))
		self.country.setItemText(203, _translate("Dialog", "South Georgia & South Sandwich Islands"))
		self.country.setItemText(204, _translate("Dialog", "South Korea"))
		self.country.setItemText(205, _translate("Dialog", "South Sudan"))
		self.country.setItemText(206, _translate("Dialog", "Spain"))
		self.country.setItemText(207, _translate("Dialog", "Sri Lanka"))
		self.country.setItemText(208, _translate("Dialog", "St. Barthélemy"))
		self.country.setItemText(209, _translate("Dialog", "St. Helena"))
		self.country.setItemText(210, _translate("Dialog", "St. Kitts & Nevis"))
		self.country.setItemText(211, _translate("Dialog", "St. Lucia"))
		self.country.setItemText(212, _translate("Dialog", "St. Martin"))
		self.country.setItemText(213, _translate("Dialog", "St. Pierre & Miquelon"))
		self.country.setItemText(214, _translate("Dialog", "St. Vincent & Grenadines"))
		self.country.setItemText(215, _translate("Dialog", "Sudan"))
		self.country.setItemText(216, _translate("Dialog", "Suriname"))
		self.country.setItemText(217, _translate("Dialog", "Svalbard & Jan Mayen"))
		self.country.setItemText(218, _translate("Dialog", "Swaziland"))
		self.country.setItemText(219, _translate("Dialog", "Sweden"))
		self.country.setItemText(220, _translate("Dialog", "Switzerland"))
		self.country.setItemText(221, _translate("Dialog", "Syria"))
		self.country.setItemText(222, _translate("Dialog", "Taiwan"))
		self.country.setItemText(223, _translate("Dialog", "Tajikistan"))
		self.country.setItemText(224, _translate("Dialog", "Tanzania"))
		self.country.setItemText(225, _translate("Dialog", "Thailand"))
		self.country.setItemText(226, _translate("Dialog", "Timor-Leste"))
		self.country.setItemText(227, _translate("Dialog", "Togo"))
		self.country.setItemText(228, _translate("Dialog", "Tokelau"))
		self.country.setItemText(229, _translate("Dialog", "Tonga"))
		self.country.setItemText(230, _translate("Dialog", "Trinidad & Tobago"))
		self.country.setItemText(231, _translate("Dialog", "Tristan da Cunha"))
		self.country.setItemText(232, _translate("Dialog", "Tunisia"))
		self.country.setItemText(233, _translate("Dialog", "Turkey"))
		self.country.setItemText(234, _translate("Dialog", "Turkmenistan"))
		self.country.setItemText(235, _translate("Dialog", "Turks & Caicos Islands"))
		self.country.setItemText(236, _translate("Dialog", "Tuvalu"))
		self.country.setItemText(237, _translate("Dialog", "U.S. Outlying Islands"))
		self.country.setItemText(238, _translate("Dialog", "U.S. Virgin Islands"))
		self.country.setItemText(239, _translate("Dialog", "Uganda"))
		self.country.setItemText(240, _translate("Dialog", "Ukraine"))
		self.country.setItemText(241, _translate("Dialog", "United Arab Emirates"))
		self.country.setItemText(242, _translate("Dialog", "United Kingdom"))
		self.country.setItemText(243, _translate("Dialog", "United Nations"))
		self.country.setItemText(244, _translate("Dialog", "United States"))
		self.country.setItemText(245, _translate("Dialog", "Uruguay"))
		self.country.setItemText(246, _translate("Dialog", "Uzbekistan"))
		self.country.setItemText(247, _translate("Dialog", "Vanuatu"))
		self.country.setItemText(248, _translate("Dialog", "Vatican City"))
		self.country.setItemText(249, _translate("Dialog", "Venezuela"))
		self.country.setItemText(250, _translate("Dialog", "Vietnam"))
		self.country.setItemText(251, _translate("Dialog", "Wallis & Futuna"))
		self.country.setItemText(252, _translate("Dialog", "Western Sahara"))
		self.country.setItemText(253, _translate("Dialog", "Yemen"))
		self.country.setItemText(254, _translate("Dialog", "Zambia"))
		self.country.setItemText(255, _translate("Dialog", "Zimbabwe"))
		self.country.setCurrentText(config6)
		self.next_day_info1.setText(_translate("Dialog", "Next day starts"))
		self.next_day_info2.setText(_translate("Dialog", "hours past midnight"))
		

	def create_account(self):
		try:
			username = self.create_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/users/'
			x = requests.post(url)
			if username in eval(x.text):
				tooltip("Username already taken")
			else:
				url = 'https://ankileaderboard.pythonanywhere.com/sync/'
				streak, cards, time, cards_past_30_days = Stats()
				data = {'Username': username , "Streak": streak, "Cards": cards , "Time": time , "Sync_Date": datetime.now(), "Month": cards_past_30_days, "Subject": config5, "Country": config6}
				x = requests.post(url, data = data)
				config = {"new_user": "False","username": username, "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully created account.")
				self.create_username.setText("")
		except:
			pass

	def login(self):
		try:
			username = self.login_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/users/'
			x = requests.post(url)
			if username in eval(x.text):
				config = {"new_user": "False","username": username, "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully logged in.")
				self.login_username.setText("")
			else:
				tooltip("Account doesn't exist.")
		except:
			pass

	def delete(self):
		try:
			username = self.delete_username.text()
			config = mw.addonManager.getConfig(__name__)
			config3 = config['friends']
			config4 = config['newday']
			config5 = config['subject']
			config6 = config['country']
			url = 'https://ankileaderboard.pythonanywhere.com/delete/'
			data = {'Username': username}
			x = requests.post(url, data = data)
			if x.text == "Deleted":
				config = {"new_user": "True","username": "", "friends": config3, "newday": config4, "country": config6, "subject": config5}
				mw.addonManager.writeConfig(__name__, config)
				tooltip("Successfully deleted account.")
				self.delete_username.setText("")
			else:
				tooltip("Error")
		except:
			pass

	def add_friend(self):
		username = self.friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config6 = config['country']
		url = 'https://ankileaderboard.pythonanywhere.com/users/'
		x = requests.post(url)
		if config2 not in config3:
			config3.append(config2)
		if username in eval(x.text):
			config3.append(username)
			config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "country": config6, "subject": config5}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(username + " is now your friend.")
			self.friend_username.setText("")
		else:
			tooltip("Couldn't find friend")

	def remove_friend(self):
		username = self.remove_friend_username.text()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config6 = config['country']
		url = 'https://ankileaderboard.pythonanywhere.com/users/'
		x = requests.post(url)
		if username in config3:
			config3.remove(username)
			config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "country": config6, "subject": config5}
			mw.addonManager.writeConfig(__name__, config)
			tooltip(username + " was removed from your friendlist")
			self.remove_friend_username.setText("")
		else:
			tooltip("Couldn't find friend")

	def set_time(self):
		beginning_of_new_day = self.newday.value()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config5 = config['subject']
		config6 = config['country']
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": str(beginning_of_new_day), "country": config6, "subject": config5}
		mw.addonManager.writeConfig(__name__, config)

	def set_subject(self):
		subject = self.subject.currentText()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config6 = config['country']
		if subject == "What are you studying?":
			subject = "Custom"
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "subject": subject, "country": config6}
		mw.addonManager.writeConfig(__name__, config)

	def set_country(self):
		country = self.country.currentText()
		config = mw.addonManager.getConfig(__name__)
		config1 = config['new_user']
		config2 = config['username']
		config3 = config['friends']
		config4 = config['newday']
		config5 = config['subject']
		config = {"new_user": config1,"username": config2, "friends": config3, "newday": config4, "subject": config5 , "country": country}
		mw.addonManager.writeConfig(__name__, config)


class start_setup(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_Dialog()
		self.dialog.setupUi(self)
