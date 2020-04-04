from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *
from aqt.utils import showInfo
from os.path import dirname, join, realpath
from .Leaderboard import start_main
from .Setup import start_setup
import webbrowser


def Main():
	config = mw.addonManager.getConfig(__name__)
	setup = config['new_user']
	if setup == "True":
		s = start_setup()
		if s.exec():
			pass
	else:
		s = start_main()
		if s.exec():
			pass
		

def setup():
	s = start_setup()
	if s.exec():
		pass
	
def github():
	webbrowser.open('https://github.com/ThoreBor/Anki_Leaderboard/issues')

def about():
	showInfo('<h3>Anki Leaderboard v1.3.1</h3><br>The code for the add-on is available on <a href="https://github.com/ThoreBor/Anki_Leaderboard">GitHub.</a> It is licensed under the <a href="https://github.com/ThoreBor/Anki_Leaderboard/blob/master/LICENSE">MIT License.</a> If you like this add-on, rate and review it on <a href="https://ankiweb.net/shared/info/41708974">Anki Web.</a><br><div>Crown icon made by <a href="https://www.flaticon.com/de/autoren/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div><div>Person icon made by <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon">www.flaticon.com</a></div><br>© Thore Tyborski 2020')
	
def add_menu(Name, Button, exe, *sc):
	action = QAction(Button, mw)
	action.triggered.connect(exe)
	if not hasattr(mw, 'menu'):
		mw.menu = {}
	if Name not in mw.menu:
		add = QMenu(Name, mw)
		mw.menu[Name] = add
		mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(), add)
	mw.menu[Name].addAction(action)
	for i in sc:
		action.setShortcut(QKeySequence(i))

add_menu('Leaderboard',"Leaderboard", Main, 'Shift+L')
add_menu('Leaderboard',"Make a feature request or report a bug", github)
add_menu('Leaderboard',"Config", setup)
add_menu('Leaderboard',"About", about)