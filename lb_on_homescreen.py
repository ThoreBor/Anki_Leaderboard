import datetime
from datetime import date, timedelta
import json

try:
	from aqt import gui_hooks
except:
	pass
from aqt.deckbrowser import DeckBrowser
from aqt import mw
from aqt.deckbrowser import DeckBrowser
from anki.hooks import wrap

from .userInfo import start_user_info
from .config_manager import write_config

def getData():
	config = mw.addonManager.getConfig(__name__)
	medal_users = config["medal_users"]
	if config["tab"] != 4:
		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		lb_list = []
		counter = 0
		for i in data[0]:
			username = i[0]
			streak = i[1]
			cards = i[2]
			time = i[3]
			sync_date = i[4]
			sync_date = datetime.datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')
			month = i[5]
			country = i[7]
			retention = i[8]
			groups = []
			if i[6]:
				groups.append(i[6].replace(" ", ""))
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
			
			if sync_date > start_day and username not in config["hidden_users"]:
				if config["tab"] == 0:
					counter += 1
					lb_list.append([counter, username, cards, time, streak, month, retention])
				if config["tab"] == 1 and username in config["friends"]:
					counter += 1
					lb_list.append([counter, username, cards, time, streak, month, retention])
				if config["tab"] == 2 and country == config["country"].replace(" ", ""):
					counter += 1
					lb_list.append([counter, username, cards, time, streak, month, retention])
				if config["tab"] == 3 and config["current_group"] in groups:
					counter += 1
					lb_list.append([counter, username, cards, time, streak, month, retention])

	if config["tab"] == 4:
		for i in data[1]:
			if config["username"] in i:
				user_league_name = i[5]

		counter = 0
		lb_list = []
		for i in data[1]:
			username = i[0]
			xp = i[1]
			reviews = i[2]
			time_spend = i[3]
			retention = i[4]
			league_name = i[5]
			days_learned = i[7]	

			for i in medal_users:
				if username in i:
					username = f"{username} |"
					if i[1] > 0:
						username = f"{username} {i[1] if i[1] != 1 else ''}🥇"
					if i[2] > 0:
						username = f"{username} {i[2] if i[2] != 1 else ''}🥈"
					if i[3] > 0:
						username = f"{username} {i[3] if i[3] != 1 else ''}🥉"

			if league_name == user_league_name and xp != 0:
				counter += 1
				lb_list.append([counter, username, xp, reviews, time_spend, retention, days_learned])

	write_config("homescreen_data", lb_list)
	return lb_list

def on_deck_browser_will_render_content(overview, content):
	config = mw.addonManager.getConfig(__name__)
	if config["homescreen_data"]:
		lb = config["homescreen_data"]
	else:
		lb = getData()
	result = []
	lb_length = len(lb)
	if config["maxUsers"] > lb_length:
		config["maxUsers"] = lb_length
	if config["focus_on_user"] == True and len(lb) > config["maxUsers"]:
		for i in lb:
			if config["username"] == i[1].split(" |")[0]:
				user_index = lb.index(i)	
				if int(config["maxUsers"]) % 2 == 0:
					if user_index + config["maxUsers"] / 2 > lb_length:
						for i in range((user_index - config["maxUsers"] + 1), user_index + 1):
							result.append(lb[i])
						break
					if user_index - config["maxUsers"] / 2 < 0:
						for i in range(user_index, (user_index + config["maxUsers"])):
							result.append(lb[i])
						break
					else:
						for i in range((user_index - int(config["maxUsers"] / 2)), (user_index + int(config["maxUsers"] / 2))):
							result.append(lb[i])
						break
				else:
					if user_index + (config["maxUsers"] / 2) + 1 > lb_length:
						for i in range((user_index - config["maxUsers"] + 1), user_index + 1):
							result.append(lb[i])
						break
					if user_index - config["maxUsers"] / 2 < 0:
						for i in range(user_index, (user_index + config["maxUsers"])):
							result.append(lb[i])
						break
					else:
						for i in range((user_index - int(config["maxUsers"] / 2)), (user_index + int(config["maxUsers"] / 2) + 1)):
							result.append(lb[i])
					break
	
		if not result:
			result = lb[:config["maxUsers"]]

		table_style = """
		<style>
			table.lb_table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
				width: 35%;
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
		</style>
		"""
	else:
		result = lb[:config["maxUsers"]]

		table_style = """
		<style>
			table.lb_table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
				width: 35%;
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
		table_header = """
		<br>
		<table class="lb_table">
			<tr>
				<th>#</th>
				<th>Username</th>
				<th style="text-align:right">Reviews</th>
				<th style="text-align:right">Minutes</th>
				<th style="text-align:right">Streak</th>
				<th style="text-align:right">Past 31 days</th>
				<th style="text-align:right">Retention</th>
			</tr>
		"""
		table_content = ""
		for i in result:
			table_content = table_content + f"""
			<tr>
				<td>{i[0]}</td>
				<td><button style="outline:0 !important; cursor:pointer; border: none; background: none;" type="button" onclick="pycmd('userinfo:{i[1]}')"><b>{i[1]}</b></button></td>
				<td style="text-align:right">{i[2]}</td>
				<td style="text-align:right">{i[3]}</td>
				<td style="text-align:right">{i[4]}</td>
				<td style="text-align:right">{i[5]}</td>
				<td style="text-align:right">{i[6]}%</td>
			</tr>
			"""
	if config["tab"] == 4:
		table_header = """
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
		table_content = ""

		for i in result:
			table_content = table_content + f"""
			<tr>
				<td>{i[0]}</td>
				<td><button style="outline:0 !important; cursor:pointer; border: none; background: none;" type="button" onclick="pycmd('userinfo:{i[1]}')"><b>{i[1]}</b></button></td>
				<td style="text-align:right">{i[2]}</td>
				<td style="text-align:right">{i[3]}</td>
				<td style="text-align:right">{i[4]}</td>
				<td style="text-align:right">{i[5]}%</td>
				<td style="text-align:right">{i[6]}%</td>
			</tr>
			"""

	content.stats += table_style + table_header + table_content + "</table>"

def leaderboard_on_deck_browser(response):
	global data
	data = response
	config = mw.addonManager.getConfig(__name__)
	gui_hooks.deck_browser_will_render_content.remove(on_deck_browser_will_render_content)
	if config["homescreen"] == True:
		gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)
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