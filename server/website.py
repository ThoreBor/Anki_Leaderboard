from django.shortcuts import render
import sqlite3
from datetime import datetime, timedelta
import json

database_path = '/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db'
#database_path = 'Leaderboard.db'

def reviews(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT Username, Cards, Sync_Date FROM Leaderboard WHERE suspended IS NULL ORDER BY Cards DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "reviews.html", {"data": data})

def time(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT Username, Time_Spend, Sync_Date FROM Leaderboard WHERE suspended IS NULL ORDER BY Time_Spend DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "time.html", {"data": data})

def streak(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Sync_Date FROM Leaderboard WHERE suspended IS NULL ORDER BY Streak DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "streak.html", {"data": data})

def retention(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT Username, Retention, Sync_Date FROM Leaderboard WHERE suspended IS NULL ORDER BY Retention DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')

		if sync_date > start_day and row[1] != "N/A" and row[1] != "":
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "retention.html", {"data": data})

def user(request, username):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	user_data = c.execute("SELECT * FROM Leaderboard WHERE Username = (?)",(username,)).fetchone()
	league = c.execute("SELECT league, history FROM League WHERE Username = (?)",(username,)).fetchone()
	if not league:
		league = ["None", "None"]
	if user_data[7] == "Country" or "":
		country = "-"
	else:
		country = user_data[7]
	if user_data[12]:
		groups = json.loads(user_data[12])
	else:
		groups = []
	if user_data[6] == "Custom" or user_data[6] == "" or user_data[6] == None:
		groups = ["-"]
	else:
		subject = user_data[6]
		if subject not in [group.replace(" ", "") for group in groups]:
			groups.append(subject)
	data = [{"username": username, "streak": user_data[1], "cards": user_data[2], "time": user_data[3], "month": user_data[5],
	"subject": ', '.join(groups), "country": country, "retention": user_data[8], "league": league[0]}]
	return render(request, "user.html", {"data": data})

def alpha(request):
	data = []
	counter = 1
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Alpha" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4], "days_learned": row[6]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def beta(request):
	data = []
	counter = 1
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Beta" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4], "days_learned": row[6]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def gamma(request):
	data = []
	counter = 1
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Gamma" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4], "days_learned": row[6]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def delta(request):
	data = []
	counter = 1
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Delta" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4], "days_learned": row[6]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})