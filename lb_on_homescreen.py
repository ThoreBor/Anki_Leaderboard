import datetime
from datetime import date, timedelta
import requests

from aqt import gui_hooks
from aqt.deckbrowser import DeckBrowser
from aqt import mw
from aqt.utils import showWarning

def getData():
	config = mw.addonManager.getConfig(__name__)
	if config["tab"] != 4:
		new_day = datetime.time(int(config['newday']),0,0)
		time_now = datetime.datetime.now().time()
		if time_now < new_day:
			start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
		else:
			start_day = datetime.datetime.combine(date.today(), new_day)

		url = 'https://ankileaderboard.pythonanywhere.com/getdata/'
		sortby = {"sortby": config["sortby"]}
		try:
			data = requests.post(url, data = sortby, timeout=20).json()
		except:
			data = []
			showWarning("Timeout error [getdata] - No internet connection, or server response took too long.", title="Leaderboard error")

		lb_list = []
		counter = 0

		for i in data:
			username = i[0]
			streak = i[1]
			cards = i[2]
			time = i[3]
			sync_date = i[4]
			sync_date = sync_date.replace(" ", "")
			sync_date = datetime.datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))
			try:
				month = int(i[5])
			except:
				month = ""
			subject = i[6]
			country = i[7]
			retention = i[8]
			try:
				retention = float(retention)
			except:
				retention = ""
			if sync_date > start_day and username not in config["hidden_users"]:

				if config["tab"] == 0:
					counter += 1
					lb_list.append([username, cards, time, streak, month, retention, counter])
				if config["tab"] == 1 and username in config["friends"]:
					counter += 1
					lb_list.append([username, cards, time, streak, month, retention, counter])
				if config["tab"] == 2 and country == config["country"]:
					counter += 1
					lb_list.append([username, cards, time, streak, month, retention, counter])
				if config["tab"] == 3 and subject == config["subject"]:
					counter += 1
					lb_list.append([username, cards, time, streak, month, retention, counter])
				if counter == config["maxUsers"]:
					break

	if config["tab"] == 4:
		url = 'https://ankileaderboard.pythonanywhere.com/league/'
		try:
			data = requests.get(url, timeout=20).json()
		except:
			data = []
			showWarning("Timeout error [load_league] - No internet connection, or server response took too long.", title="Leaderboard error")

		user_league_name = "Alpha"
		for i in data:
			if config["username"] in i:
				user_league_name = i[5]

		counter = 0
		lb_list = []

		for i in data:
			username = i[0]
			xp = i[1]
			reviews = i[2]
			time_spend = i[3]
			retention = i[4]
			league_name = i[5]

			if league_name == user_league_name and xp != 0:
				counter += 1
				lb_list.append([counter, username, xp, reviews, time_spend, retention])
				if counter == config["maxUsers"]:
					break

	return lb_list

def on_deck_browser_will_render_content(overview, content):
	config = mw.addonManager.getConfig(__name__)
	lb = getData()
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
				<th>Reviews</th>
				<th>Minutes</th>
				<th>Streak</th>
				<th>Past 31 days</th>
				<th>Retention</th>
			</tr>
		"""
		table_content = ""

		for i in lb:
			table_content = table_content + f"""
			<tr>
				<td>{i[6]}</td>
				<td>{i[0]}</td>
				<td>{i[1]}</td>
				<td>{i[2]}</td>
				<td>{i[3]}</td>
				<td>{i[4]}</td>
				<td>{i[5]}%</td>
			</tr>
			"""
	if config["tab"] == 4:
		table_header = """
		<br>
		<table class="lb_table">
			<tr>
				<th>#</th>
				<th>Username</th>
				<th>XP</th>
				<th>Minutes</th>
				<th>Reviews</th>
				<th>Retention</th>
			</tr>
		"""
		table_content = ""

		for i in lb:
			table_content = table_content + f"""
			<tr>
				<td>{i[0]}</td>
				<td>{i[1]}</td>
				<td>{i[2]}</td>
				<td>{i[3]}</td>
				<td>{i[4]}</td>
				<td>{i[5]}</td>
			</tr>
			"""

	content.stats += table_style + table_header + table_content + "</table>"

def leaderboard_on_deck_browser():
	config = mw.addonManager.getConfig(__name__)
	gui_hooks.deck_browser_will_render_content.remove(on_deck_browser_will_render_content)
	if config["homescreen"] == True:
		gui_hooks.deck_browser_will_render_content.append(on_deck_browser_will_render_content)
	DB = DeckBrowser(mw)
	DB.refresh()