import datetime
from datetime import date, timedelta
import json

from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from anki.hooks import wrap

from .userInfo import start_user_info
from .config_manager import write_config


class homescreenLeaderboard():
	def __init__(self):
		pass

	def getData(self):
		config = mw.addonManager.getConfig(__name__)
		medal_users = config["medal_users"]
		if config["tab"] != 4:
			newDay = datetime.time(int(config['newday']),0,0)
			timeNow = datetime.datetime.now().time()
			if timeNow < newDay:
				startDay = datetime.datetime.combine(date.today() - timedelta(days=1), newDay)
			else:
				startDay = datetime.datetime.combine(date.today(), newDay)

			counter = 0
			for i in self.data[0]:
				username = i[0]
				streak = i[1]
				cards = i[2]
				time = i[3]
				syncDate = i[4]
				syncDate = datetime.datetime.strptime(syncDate, '%Y-%m-%d %H:%M:%S.%f')
				month = i[5]
				country = i[7]
				retention = i[8]
				groups = []
				if i[6]:
					groups.append(i[6])
				if i[9]:
					for group in json.loads(i[9]):
						groups.append(group)
				groups = [x.replace(" ", "") for x in groups]	

				if config["show_medals"] == True:
					for i in medal_users:
						if username in i:
							username = f"{username} |"
							if i[1] > 0:
								username = f"{username} {i[1] if i[1] != 1 else ''}🥇"
							if i[2] > 0:
								username = f"{username} {i[2] if i[2] != 1 else ''}🥈"
							if i[3] > 0:
								username = f"{username} {i[3] if i[3] != 1 else ''}🥉"
				
				if syncDate > startDay and username not in config["hidden_users"]:
					if config["tab"] == 0:
						counter += 1
						self.lbList.append([counter, username, cards, time, streak, month, retention])
					if config["tab"] == 1 and username in config["friends"]:
						counter += 1
						self.lbList.append([counter, username, cards, time, streak, month, retention])
					if config["tab"] == 2 and country == config["country"].replace(" ", ""):
						counter += 1
						self.lbList.append([counter, username, cards, time, streak, month, retention])
					if config["tab"] == 3 and config["current_group"].replace(" ", "") in groups:
						counter += 1
						self.lbList.append([counter, username, cards, time, streak, month, retention])

		if config["tab"] == 4:
			for i in self.data[1]:
				if config["username"] in i:
					userLeagueName = i[5]
			counter = 0
			for i in self.data[1]:
				username = i[0]
				xp = i[1]
				reviews = i[2]
				time = i[3]
				retention = i[4]
				leagueName = i[5]
				daysLearned = i[7]

				for i in medal_users:
					if username in i:
						username = f"{username} |"
						if i[1] > 0:
							username = f"{username} {i[1] if i[1] != 1 else ''}🥇"
						if i[2] > 0:
							username = f"{username} {i[2] if i[2] != 1 else ''}🥈"
						if i[3] > 0:
							username = f"{username} {i[3] if i[3] != 1 else ''}🥉"

				if leagueName == userLeagueName and xp != 0:
					counter += 1
					self.lbList.append([counter, username, xp, reviews, time, retention, daysLearned])

		write_config("homescreen_data", self.lbList)

	def userSublist(self, n, index):
	    startIdx = index - (n-1) // 2
	    endIdx = index + n // 2
	    return self.lbList[startIdx:endIdx+1]
	
	def on_deck_browser_will_render_content(self, overview, content):
		config = mw.addonManager.getConfig(__name__)
		result = []
		if not self.lbList:
			self.getData()

		if config["tab"] == 0:
			title = "<h3>Global</h3>"
		if config["tab"] == 1:
			title = "<h3>Friends</h3>"
		if config["tab"] == 2:
			title = f"<h3>{config['country']}</h3>"
		if config["tab"] == 3:
			title = f"<h3>{config['current_group']}</h3>"
		if config["tab"] == 4:
			title = "<h3>League</h3>"

		if config["focus_on_user"] == True and len(self.lbList) > config["maxUsers"]:
			for i in self.lbList:
				if config["username"] == i[1].split(" |")[0]:
					userIndex = self.lbList.index(i)
					result = self.userSublist(config["maxUsers"], userIndex)

			if not result:
				result = self.lbList[:config["maxUsers"]]
			
			tableStyle = """
			<style>
				table.lb_table {
					font-family: arial, sans-serif;
					border: none;
					border-collapse: collapse;
					width: 45%;
					margin-left:auto;
					margin-right:auto;
					font-weight: bold;
				}

				table.lb_table td{
					white-space: nowrap;
				}

				table.lb_table td, th {
					text-align: left;
					padding: 8px;
				}
			</style>
			"""

		else:
			result = self.lbList[:config["maxUsers"]]

			tableStyle = """
			<style>
				table.lb_table {
					font-family: arial, sans-serif;
					border-collapse: collapse;
					border: none;
					width: 45%;
					margin-left:auto;
					margin-right:auto;
					font-weight: bold;
				}

				table.lb_table td{
					white-space: nowrap;  /** added **/
				}

				table.lb_table td, th {
					text-align: left;
					padding: 8px;
				}

				table.lb_table tr:nth-child(2) {
					background-color: #ccac00;
				}

				table.lb_table tr:nth-child(3) {
					background-color: #999999;
				}

				table.lb_table tr:nth-child(4) {
					background-color: #a7684a;
				}
			</style>
			"""

		if config["tab"] != 4:
			tableHeader = """
			<br>
			<table class="lb_table">
				<tr>
					<th>#</th>
					<th>Username</th>
					<th style="text-align:right">Reviews</th>
					<th style="text-align:right">Minutes</th>
					<th style="text-align:right">Streak</th>
					<th style="text-align:right">Past month</th>
					<th style="text-align:right">Retention</th>
				</tr>
			"""
			tableContent = ""
			for i in result:
				tableContent += f"""
				<tr>
					<td>{i[0]}</td>
					<td><button style="all: revert; outline:0 !important; cursor:pointer; border: none; background: none;" type="button" onclick="pycmd('userinfo:{i[1]}')"><b>{i[1]}</b></button></td>
					<td style="text-align:right">{i[2]}</td>
					<td style="text-align:right">{i[3]}</td>
					<td style="text-align:right">{i[4]}</td>
					<td style="text-align:right">{i[5]}</td>
					<td style="text-align:right">{i[6]}%</td>
				</tr>
				"""
		if config["tab"] == 4:
			tableHeader = """
			<br>
			<table class="lb_table">
				<tr>
					<th>#</th>
					<th>Username</th>
					<th style="text-align:right">XP</th>
					<th style="text-align:right">Minutes</th>
					<th style="text-align:right">Reviews</th>
					<th style="text-align:right">Retention</th>
					<th style="text-align:right">Days learned</th>
				</tr>
			"""
			tableContent = ""
			for i in result:
				tableContent += f"""
				<tr>
					<td>{i[0]}</td>
					<td><button style="all: revert; outline:0 !important; cursor:pointer; border: none; background: none;" type="button" onclick="pycmd('userinfo:{i[1]}')"><b>{i[1]}</b></button></td>
					<td style="text-align:right">{i[2]}</td>
					<td style="text-align:right">{i[3]}</td>
					<td style="text-align:right">{i[4]}</td>
					<td style="text-align:right">{i[5]}%</td>
					<td style="text-align:right">{i[6]}%</td>
				</tr>
				"""

		content.stats += title + tableStyle + tableHeader + tableContent + "</table>"

	def leaderboard_on_deck_browser(self, response):
		config = mw.addonManager.getConfig(__name__)
		self.data = response
		self.lbList = config["homescreen_data"]
		gui_hooks.deck_browser_will_render_content.remove(self.on_deck_browser_will_render_content)
		if config["homescreen"] == True:
			gui_hooks.deck_browser_will_render_content.append(self.on_deck_browser_will_render_content)
		DB = DeckBrowser(mw)
		DB.refresh()
		

def deckbrowser_linkHandler_wrapper(overview, url):
	url = url.split(":")
	if url[0] == "userinfo":
		mw.user_info = start_user_info(url[1], False)
		mw.user_info.show()
		mw.user_info.raise_()
		mw.user_info.activateWindow()

DeckBrowser._linkHandler = wrap(DeckBrowser._linkHandler, deckbrowser_linkHandler_wrapper, "after")