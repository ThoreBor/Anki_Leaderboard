from aqt.qt import QDialog, Qt, QIcon, QPixmap, qtmajor
from pathlib import Path
import json

if qtmajor > 5:
	from ...forms.pyqt6UI import achievement
	from PyQt6 import QtCore
else:
	from ...forms.pyqt5UI import achievement
	from PyQt5 import QtCore
	

class streak(QDialog):
	def __init__(self, days, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = achievement.Ui_Dialog()
		self.dialog.setupUi(self)
		self.days = days
		self.setupUI()
		self.loadWebpage()

	def setupUI(self):
		root = Path(__file__).parents[1]
		icon = QIcon()
		icon.addPixmap(QPixmap(f"{root}/designer/icons/krone.png"), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

	def loadWebpage(self):
		data = {
			"streak": self.days,
		}
		with open(f"{Path(__file__).parents[0]}/data.json", "w") as file:
			file.write(f"data = '{json.dumps(data)}';")

		sourceFile = f"{Path(__file__).parents[0]}/streak.html"
		self.dialog.webview.load(QtCore.QUrl.fromLocalFile(sourceFile))