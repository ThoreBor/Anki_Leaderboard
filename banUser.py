from aqt.qt import *
from aqt.utils import tooltip
from aqt import mw
import hashlib

from .forms import banUser
from .api_connect import connectToAPI

class start_banUser(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = banUser.Ui_Dialog()
		self.dialog.setupUi(self)
		self.user_clicked = user_clicked
		self.setupUI()

	def setupUI(self):
		self.dialog.banButton.clicked.connect(self.banUser)

	def banUser(self):
		config = mw.addonManager.getConfig(__name__)
		password = hashlib.sha1(self.dialog.groupPassword.text().encode('utf-8')).hexdigest().upper()
		toBan = self.user_clicked
		data = {"toBan": toBan, "group": config["current_group"], "pwd": password, "authToken": config["authToken"], "user": config["username"]}
		x = connectToAPI("banUser/", False, data, "Done!", "banUser")
		if x.text == "Done!":
			tooltip(f"{toBan} is now banned from {config['current_group']}")
		
		