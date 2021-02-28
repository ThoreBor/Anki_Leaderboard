from django.shortcuts import render, redirect
from django.http import HttpResponse
import sqlite3
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage
from .stats import Stats
import os

def reviews(request):
	data = []
	counter = 1
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Cards, Sync_Date FROM Leaderboard ORDER BY Cards DESC")

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
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Time_Spend, Sync_Date FROM Leaderboard ORDER BY Time_Spend DESC")

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
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Sync_Date FROM Leaderboard ORDER BY Streak DESC")

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
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Retention, Sync_Date FROM Leaderboard ORDER BY Retention DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = datetime.strptime(sync_date, '%Y-%m-%d %H:%M:%S.%f')

		if sync_date > start_day and row[1] != "N/A" and row[1] != "":
			x = {"place": counter, "username": row[0], "value": row[1]}
			data.append(x)
			counter += 1
	return render(request, "retention.html", {"data": data})

def user(request, username):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	user_data = c.execute("SELECT * FROM Leaderboard WHERE Username = (?)",(username,)).fetchone()
	league = c.execute("SELECT league, history FROM League WHERE Username = (?)",(username,)).fetchone()
	if user_data[7] == "Country" or "":
		country = "-"
	else:
		country = user_data[7]
	if user_data[6] == "Custom" or "":
		subject = "-"
	else:
		subject = user_data[6]
	data = [{"username": username, "streak": user_data[1], "cards": user_data[2], "time": user_data[3], "month": user_data[5],
	"subject": subject, "country": country, "retention": user_data[8], "status": user_data[10], "league": league[0], "history": league[1]}]

	return render(request, "user.html", {"data": data})

def alpha(request):
	data = []
	counter = 1
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league FROM League ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Alpha" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def beta(request):
	data = []
	counter = 1
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league FROM League ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Beta" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def gamma(request):
	data = []
	counter = 1
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league FROM League ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Gamma" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def delta(request):
	data = []
	counter = 1
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league FROM League ORDER BY xp DESC")

	for row in c.fetchall():
		if row[5] == "Delta" and row[1] != 0:
			x = {"place": counter, "username": row[0], "xp": row[1], "time": row[2], "reviews": row[3], "retention": row[4]}
			data.append(x)
			counter += 1
	return render(request, "leagues.html", {"data": data})

def upload(request):
	if request.method == "POST":
		print("Start mobile sync...")
		uploaded_file = request.FILES['database']
		username = request.POST.get("username", "")
		if username == "":
			return HttpResponse("Error - invalid username")
		offset = int(request.POST.get("offset",""))
		timestamp = datetime.now() - timedelta(minutes=offset)
		nextday = request.POST.get("newday", "")
		if nextday == "":
			nextday = 4
		fname = str(datetime.now().timestamp())+".anki2"
		fs = FileSystemStorage()
		fs.save(fname, uploaded_file)
		Streak, Month, Cards, Retention, Time = Stats(fname, timestamp, nextday, offset)
		os.remove('/home/ankileaderboard/anki_leaderboard_pythonanywhere/media/'+fname)

		### SYNC ###
		### Filter ###

		if username == "" or len(username) > 15:
			return HttpResponse("Error - invalid username")

		try:
			int(Streak)
		except:
			return HttpResponse("Error - invalid streak value")

		try:
			int(Cards)
		except:
			return HttpResponse("Error - invalid cards value")

		try:
			float(Time)
		except:
			return HttpResponse("Error - invalid time value")

		try:
			check_sync_date = str(timestamp).replace(" ", "")
			check_sync_date = datetime(int(check_sync_date[0:4]),int(check_sync_date[5:7]), int(check_sync_date[8:10]), int(check_sync_date[10:12]), int(check_sync_date[13:15]), int(check_sync_date[16:18]))
		except:
			return HttpResponse("Error invalid timestamp")

		try:
			int(Month)
		except:
			return HttpResponse("Error - invalid month value")

		try:
			float(Retention)
		except:
			return HttpResponse("Error - invalid retention value")

		###

		### UPDATE DATABASE ###

		conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
		c = conn.cursor()
		if c.execute("SELECT Username FROM Leaderboard WHERE Username = (?)", (username,)).fetchone():
			c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Retention = (?) WHERE Username = (?) ", (Streak, Cards, Time, str(timestamp), Month, Retention, username))
			conn.commit()
			print("Mobile sync - Updated entry: " + str(username))
			return redirect('/user/'+username)
		else:
			c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Retention) VALUES(?, ?, ?, ?, ?, ?,?)', (username, Streak, Cards, Time, str(timestamp), Month, Retention))
			conn.commit()
			print("Mobile sync - Created new entry: " + str(username))
			return redirect('/user/'+username)
	return render(request, "upload.html")