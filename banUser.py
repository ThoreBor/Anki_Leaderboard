from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from aqt.utils import tooltip
from aqt import mw
import hashlib

if qtmajor > 5:
	from .forms.pyqt6UI import banUser
else:
	from .forms.pyqt5UI import banUser
from .api_connect import connectToAPI


class start_banUser(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = banUser.Ui_Dialog()
		self.dialog.setupUi(self)
		self.user_clicked = user_clicked
		self.setupUI()

	def setupUI(self):
		self.dialog.banButton.clicked.connect(self.banUser)
		
		icon = QIcon()
		icon.addPixmap(QPixmap(join(dirname(realpath(__file__)), "designer/icons/person.png")), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

	def banUser(self):
		config = mw.addonManager.getConfig(__name__)
		password = hashlib.sha1(self.dialog.groupPassword.text().encode('utf-8')).hexdigest().upper()
		toBan = self.user_clicked
		data = {"toBan": toBan, "group": config["current_group"], "pwd": password, "authToken": config["authToken"], "user": config["username"]}
		x = connectToAPI("banUser/", False, data, "Done!", "banUser")
		if x.text == "Done!":
			tooltip(f"{toBan} is now banned from {config['current_group']}")
		
