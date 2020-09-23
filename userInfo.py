from aqt.qt import *
from aqt.utils import showWarning, tooltip
import requests
from aqt import mw

from .forms import user_info
from .config_manager import write_config

class start_user_info(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = user_info.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.username_label.setText(self.user_clicked)
		url = 'https://ankileaderboard.pythonanywhere.com/getStatus/'
		data = {"username": self.user_clicked}
		try:
			data = requests.post(url, data = data, timeout=20).json()
		except:
			showWarning("Timeout error - No internet connection, or server response took too long.")
		self.dialog.status_message.setMarkdown(data[0])
		self.dialog.hideUser.clicked.connect(self.hideUser)

	def hideUser(self):
		config = mw.addonManager.getConfig(__name__)
		hidden = config["hidden_users"]
		hidden.append(self.user_clicked)
		write_config("hidden_users", hidden)
		tooltip(f"{self.user_clicked} will be hidden next time you open the leaderboard.")
