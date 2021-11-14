from aqt.qt import *
from aqt.utils import tooltip, showWarning
from aqt import mw

from .forms import reset_password
from .api_connect import connectToAPI

class start_resetPassword(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = reset_password.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.resetButton.clicked.connect(self.resetPassword)

	def resetPassword(self):
		email = self.dialog.resetEmail.text()
		username = self.dialog.resetUsername.text()
		if not email or not username:
			showWarning("Please enter your email address and username first.")
			return
		response = connectToAPI("resetPassword/", False, {"email": email, "username": username}, False, "account_forgot")
		if response.text == "Error":
			showWarning("Something went wrong")
		else:
			tooltip("Email sent")
		