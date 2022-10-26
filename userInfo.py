from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from aqt.utils import tooltip
from aqt import mw
import json
from os.path import dirname, join, realpath

if qtmajor > 5:
	from .forms.pyqt6UI import user_info
	from PyQt6 import QtCore, QtWidgets
else:
	from .forms.pyqt5UI import user_info
	from PyQt5 import QtCore, QtWidgets
from .reportUser import start_report
from .config_manager import write_config
from .api_connect import postRequest
from .banUser import start_banUser

class start_user_info(QDialog):
	def __init__(self, user_clicked, enabled, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked.split(" |")[0]
		self.enabled = enabled
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = user_info.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.username_label.setText(self.user_clicked)

		icon = QIcon()
		icon.addPixmap(QPixmap(join(dirname(realpath(__file__)), "designer/icons/person.png")), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

		if self.enabled == True:
			self.dialog.banUser.setEnabled(True)

		data = {"username": self.user_clicked}
		response = postRequest("getUserinfo/", data, 200)

		if response:
			response = response.json()
			if response[4]:
				self.dialog.status_message.setMarkdown(response[4])
			else:
				pass

			if response[0] == "Country":
				self.dialog.country_label.setText("")
			else:
				self.dialog.country_label.setText(f"Country: {response[0]}")
			for i in response[1]:
				self.dialog.group_list.addItem(i)
			self.dialog.league_label.setText(f"League: {response[2]}")
			

			header = self.dialog.history.horizontalHeader()   
			header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)
			header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Stretch)
			if response[3]:
				medals = ""
				history = json.loads(response[3])
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
					item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(results["seasons"][index]))
					self.dialog.history.setItem(rowPosition, 0, item)
					item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(results["xp"][index]))
					self.dialog.history.setItem(rowPosition, 2, item)
					item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.ItemDataRole.DisplayRole, int(results["rank"][index]))
					self.dialog.history.setItem(rowPosition, 1, item)
					item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignVCenter)

					index += 1
			
			self.dialog.hideUser.clicked.connect(self.hideUser)
			self.dialog.addFriend.clicked.connect(self.addFriend)
			self.dialog.banUser.clicked.connect(self.banUser)
			self.dialog.reportUser.clicked.connect(self.reportUser)
			self.dialog.history.sortItems(0, QtCore.Qt.SortOrder.DescendingOrder)

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
		s = start_banUser(self.user_clicked)
		if s.exec():
			pass
			
	def reportUser(self):
		s = start_report(self.user_clicked)
		if s.exec():
			pass
