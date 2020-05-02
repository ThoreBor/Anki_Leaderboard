from aqt import mw
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *
from aqt.utils import showInfo, showWarning

from os.path import dirname, join, realpath
import webbrowser
import requests
from bs4 import BeautifulSoup

from .Leaderboard import start_main
from .Setup import start_setup

def Main():
	check_info()
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

def check_info():
	try:
		url = 'https://ankileaderboardinfo.netlify.app'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116'}
		page = requests.get(url, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		if soup.find(id='show_message').get_text() == "True":
			info = soup.find(id='Message').get_text()
			showInfo(info, title="Leaderboard")
		else:
			pass
	except:
		showWarning("Make sure you're connected to the internet.")

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
