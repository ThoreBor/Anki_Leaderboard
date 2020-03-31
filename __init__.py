from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *
from aqt.utils import showInfo
import time
from os.path import dirname, join, realpath
from datetime import date, timedelta
from .Leaderboard import start_main
from .Setup import start_setup

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
		
def github():
	pass

def about():
	pass
	
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

add_menu('Leaderboard',"Leaderboard", Main, 'Shift+S')
add_menu('Leaderboard',"Make a feature request or report a bug", github)
add_menu('Leaderboard',"About", about)