from aqt.qt import *
from aqt.utils import tooltip
from aqt import mw

from .forms import report
from .api_connect import connectToAPI

class start_report(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = report.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.reportLabel.setText(f"Please explain why you want to report {self.user_clicked}:")
		self.dialog.sendReport.clicked.connect(self.sendReport)

	def sendReport(self):
		config = mw.addonManager.getConfig(__name__)
		data = {"user": config["username"], "reportUser": self.user_clicked, "message": self.dialog.reportReason.toPlainText()}
		x = connectToAPI("reportUser/", False, data, "Done!", "sendReport")
		if x.text == "Done!":
			tooltip(f"{self.user_clicked} was succsessfully reported")
