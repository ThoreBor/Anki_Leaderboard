from aqt.qt import QMovie, QDialog, Qt, QIcon, QPixmap, qtmajor
from pathlib import Path

if qtmajor > 5:
	from ..forms.pyqt6UI import achievement
else:
	from ..forms.pyqt5UI import achievement
	

class start_achievement(QDialog):
	def __init__(self, value, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.WindowType.Window)
		self.dialog = achievement.Ui_Dialog()
		self.dialog.setupUi(self)
		self.value = value
		self.setupUI()

	def setupUI(self):
		root = Path(__file__).parents[1]
		self.gif = QMovie(f"{root}/designer/gifs/confetti.gif")
		self.dialog.confetti.setMovie(self.gif)
		self.gif.start()

		icon = QIcon()
		icon.addPixmap(QPixmap(f"{root}/designer/icons/krone.png"), QIcon.Mode.Normal, QIcon.State.Off)
		self.setWindowIcon(icon)

		self.dialog.message.setText(f"{self.value} day streak")
