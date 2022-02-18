from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from aqt.utils import tooltip, showWarning
from os.path import dirname, join, realpath

if qtmajor > 5:
	from .forms.pyqt6UI import reset_password
else:
	from .forms.pyqt5UI import reset_password
from .api_connect import connectToAPI

class start_resetPassword(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = reset_password.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.resetButton.clicked.connect(self.resetPassword)

		icon = QIcon()
		icon.addPixmap(QPixmap(join(dirname(realpath(__file__)), "designer/icons/person.png")), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

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
