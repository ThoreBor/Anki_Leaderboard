from aqt.qt import *
from aqt.utils import showWarning, tooltip
import requests
from aqt import mw

from .forms import user_info
from .config_manager import write_config

class start_user_info(QDialog):
	def __init__(self, user_clicked, enabled, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked.split(" |")[0]
		self.enabled = enabled
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = user_info.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.username_label.setText(self.user_clicked)
		if self.enabled == True:
			self.dialog.banUser.setEnabled(True)

		url = 'https://ankileaderboard.pythonanywhere.com/getStatus/'
		data = {"username": self.user_clicked}
		try:
			data = requests.post(url, data = data, timeout=20).json()
		except:
			data = []
			showWarning("Timeout error [user_info] - No internet connection, or server response took too long.", title="Leaderboard error")

		self.dialog.status_message.setMarkdown(data[0])

		url = 'https://ankileaderboard.pythonanywhere.com/getUserinfo/'
		data = {"user": self.user_clicked}
		try:
			data = requests.post(url, data = data, timeout=20).json()
		except:
			data = []
			showWarning("Timeout error [user_info] - No internet connection, or server response took too long.", title="Leaderboard error")

		if data[0] == "Country":
			data[0] = None
		if data[1] == "Custom":
			data[1] = None

		self.dialog.country_label.setText(f"Country: {data[0]}")
		self.dialog.group_label.setText(f"Group: {data[1]}")
		self.dialog.league_label.setText(f"League: {data[2]}")
		self.dialog.hideUser.clicked.connect(self.hideUser)
		self.dialog.addFriend.clicked.connect(self.addFriend)
		self.dialog.banUser.clicked.connect(self.banUser)

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
		config = mw.addonManager.getConfig(__name__)
		toBan = self.user_clicked
		group = config["subject"]
		pwd = config["group_pwd"]
		token = config["token"]
		user = config["username"]
		url = 'https://ankileaderboard.pythonanywhere.com/banUser/'
		data = {"toBan": toBan, "group": group, "pwd": pwd, "token": token, "user": user}

		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				tooltip(f"{toBan} is now banned from {group}")
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [banUser] - No internet connection, or server response took too long.", title="Leaderboard error")		


