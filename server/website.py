from django.shortcuts import render
from django.http import HttpResponse
import sqlite3
from datetime import datetime, timedelta

def reviews(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Cards, Sync_Date FROM Leaderboard ORDER BY Cards DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "reviews.html", {"data": data})

def time(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Time_Spend, Sync_Date FROM Leaderboard ORDER BY Time_Spend DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "time.html", {"data": data})

def streak(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Sync_Date FROM Leaderboard ORDER BY Streak DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "streak.html", {"data": data})

def retention(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Retention, Sync_Date FROM Leaderboard ORDER BY Retention DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day and row[1] != "N/A" and row[1] != "":
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "retention.html", {"data": data})

def user(request, username):
    conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Leaderboard WHERE Username = (?)",(username,))
    user_data = c.fetchone()
    if user_data[7] == "Country" or "":
        country = "-"
    else:
        country = user_data[7]
    if user_data[6] == "Custom" or "":
        subject = "-"
    else:
        subject = user_data[6]
    data = [{"username": username, "streak": user_data[1], "cards": user_data[2], "time": user_data[3], "sync": user_data[4][:19], "month": user_data[5],
    "subject": subject, "country": country, "retention": user_data[8]}]

    return render(request, "user.html", {"data": data})