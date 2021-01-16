from aqt.qt import *
from aqt.utils import showWarning, tooltip
from aqt import mw

import requests
import json
from PyQt5 import QtCore, QtGui, QtWidgets

from .forms import report

class start_report(QDialog):
	def __init__(self, user_clicked, parent=None):
		self.parent = parent
		self.user_clicked = user_clicked
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = report.Ui_Dialog()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		self.dialog.reportLabel.setText(f"Please explain why you want to report {self.user_clicked}:")
		self.dialog.sendReport.clicked.connect(self.sendReport)

	def sendReport(self):
		config = mw.addonManager.getConfig(__name__)
		url = 'https://ankileaderboard.pythonanywhere.com/reportUser/'
		data = {"user": config["username"], "reportUser": self.user_clicked, "message": self.dialog.reportReason.toPlainText()}

		try:
			x = requests.post(url, data = data, timeout=20)
			if x.text == "Done!":
				tooltip(f"{self.user_clicked} was succsessfully reported")
			else:
				showWarning(str(x.text))
		except:
			showWarning("Timeout error [sendReport] - No internet connection, or server response took too long.", title="Leaderboard error")