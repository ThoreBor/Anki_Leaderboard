from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from aqt.utils import tooltip
from aqt import mw
from pathlib import Path

if qtmajor > 5:
	from ..forms.pyqt6UI import report
else:
	from ..forms.pyqt5UI import report
from .api_connect import postRequest

class start_report(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = report.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		root = Path(__file__).parents[1]
		icon = QIcon()
		icon.addPixmap(QPixmap(f"{root}/designer/icons/person.png"), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)
		
		self.dialog.reportLabel.setText(f"Please explain why you want to report {self.user_clicked}:")
		self.dialog.sendReport.clicked.connect(self.sendReport)

	def sendReport(self):
		config = mw.addonManager.getConfig(__name__)
		data = {"username": config["username"], "reportUser": self.user_clicked, "message": self.dialog.reportReason.toPlainText()}
		response = postRequest("reportUser/", data, 200)
		if response:
			tooltip(f"{self.user_clicked} was succsessfully reported")
