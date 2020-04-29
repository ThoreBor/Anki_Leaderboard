from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *
from aqt.utils import showInfo
from os.path import dirname, join, realpath
from .Leaderboard import start_main
from .Setup import start_setup
import webbrowser
import time

def Main():
	config = mw.addonManager.getConfig(__name__)
	setup = config['new_user']
	if setup == "True":
		invoke_setup()
	else:
		mw.leaderboard = start_main()
		mw.leaderboard.show()
		mw.leaderboard.raise_()
		mw.leaderboard.activateWindow()

def invoke_setup():
	mw.lb_setup = start_setup()
	mw.lb_setup.show()
	mw.lb_setup.raise_()
	mw.lb_setup.activateWindow()

def config_setup():
	s = start_setup()
	if s.exec():
		pass

def github():
	webbrowser.open('https://github.com/ThoreBor/Anki_Leaderboard/issues')

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

add_menu('&Leaderboard',"&Leaderboard", Main, 'Shift+L')
add_menu('&Leaderboard',"&Make a feature request or report a bug", github)
add_menu('&Leaderboard',"&Config", invoke_setup)

mw.addonManager.setConfigAction(__name__, config_setup)
