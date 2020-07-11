from PyQt5.QtGui import QMovie
from aqt.qt import *
from os.path import dirname, join, realpath

from .forms import achievement

class start_achievement(QDialog):
	def __init__(self, value, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = achievement.Ui_Dialog()
		self.dialog.setupUi(self)
		self.value = value
		self.setupUI()

	def setupUI(self):
		self.gif = QMovie(join(dirname(realpath(__file__)), 'designer/gifs/confetti.gif'))
		self.dialog.confetti.setMovie(self.gif)
		self.gif.start()

		self.dialog.message.setText(str(self.value) + " day streak")