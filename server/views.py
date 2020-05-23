from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import json
from datetime import datetime, timedelta

def reviews(request):
	data = []
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Cards, Sync_Date FROM Leaderboard ORDER BY Cards DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		if len(sync_date) == 10:
			sync_date = sync_date + "12:00:00"
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"username": row[0], "value": row[1]}
			data.append(x)
	return render(request, "reviews.html", {"data": data})

def time(request):
	data = []
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Time_Spend, Sync_Date FROM Leaderboard ORDER BY Time_Spend DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		if len(sync_date) == 10:
			sync_date = sync_date + "12:00:00"
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"username": row[0], "value": row[1]}
			data.append(x)
	return render(request, "time.html", {"data": data})

def streak(request):
	data = []
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Sync_Date FROM Leaderboard ORDER BY Streak DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		if len(sync_date) == 10:
			sync_date = sync_date + "12:00:00"
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day:
			x = {"username": row[0], "value": row[1]}
			data.append(x)
	return render(request, "streak.html", {"data": data})

def retention(request):
	data = []
	start_day = datetime.now() - timedelta(days=1)
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Retention, Sync_Date FROM Leaderboard ORDER BY Retention DESC")

	for row in c.fetchall():
		sync_date = row[2]
		sync_date = sync_date.replace(" ", "")
		if len(sync_date) == 10:
			sync_date = sync_date + "12:00:00"
		sync_date = datetime(int(sync_date[0:4]),int(sync_date[5:7]), int(sync_date[8:10]), int(sync_date[10:12]), int(sync_date[13:15]), int(sync_date[16:18]))

		if sync_date > start_day and row[1] != "N/A" and row[1] != "":
			x = {"username": row[0], "value": row[1]}
			data.append(x)
	return render(request, "retention.html", {"data": data})

@csrf_exempt
def sync(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Username_List = []
	c.execute("SELECT Username FROM Leaderboard")
	for i in c.fetchall():
		data = str(i)
		clean = ["(",")","'",",", "\\"]
		for j in clean:
		    data = data.replace(j, "")
		Username_List.append(data)

	try:
	    User = request.POST.get("Username", "")
	    Streak = request.POST.get("Streak", "")
	    Cards = request.POST.get("Cards", "")
	    Time = request.POST.get("Time", "")
	    Sync_Date = request.POST.get("Sync_Date", "")
	    Month = request.POST.get("Month","")
	    Subject = request.POST.get("Subject","")
	    Country = request.POST.get("Country","")
	    Retention = request.POST.get("Retention","")
	except:
	    print("sync error")

	if User == "":
		return HttpResponse("Error")

	if User not in Username_List:
		c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?)', (User, Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention))
		conn.commit()
		print("Created new entry: " + str(User))
	else:
		c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Subject = (?), Country = (?), Retention = (?) WHERE Username = (?) ", (Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention, User))
		conn.commit()
		print("Updated entry: " + str(User))
	return HttpResponse("Done!")

@csrf_exempt
def all_users(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Username_List = []
	c.execute("SELECT Username FROM Leaderboard")
	for i in c.fetchall():
		data = str(i)
		clean = ["(",")","'",","]
		for j in clean:
			data = data.replace(j, "")
		Username_List.append(data)
	return HttpResponse(json.dumps(Username_List))

@csrf_exempt
def get_data(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Leaderboard ORDER BY Cards DESC")
	data = []
	for row in c.fetchall():
		row = str(row)
		clean = ["(",")","'","[","]", " "]
		for i in clean:
			row = row.replace(i, "")
		data.append(row)
	return HttpResponse(json.dumps(data))


### OLD API ###


@csrf_exempt
def users(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Username_List = []
	c.execute("SELECT Username FROM Leaderboard")
	for i in c.fetchall():
		data = str(i)
		clean = ["(",")","'",",", "\\"]
		for j in clean:
		    data = data.replace(j, "")
		Username_List.append(data)
	return HttpResponse(str(Username_List))

@csrf_exempt
def getreviews(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Leaderboard ORDER BY Cards DESC")
	data = ""
	for row in c.fetchall():
	        data = data + str(row) + "<br>"
	clean = ["(",")","'","[","]", " "]
	for i in clean:
	    data = data.replace(i, "")
	return HttpResponse(str(data))

@csrf_exempt
def delete(request):
    conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
    c = conn.cursor()
    User = request.POST.get("Username", "")
    try:
        c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (User,))
        conn.commit()
        print("Deleted account: " + str(User))
        return HttpResponse("Deleted")
    except:
        return HttpResponse("Failed")

@csrf_exempt
def getstreaks(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Leaderboard ORDER BY Streak DESC")
	data = ""
	for row in c.fetchall():
	    data = data + str(row) + "<br>"
	clean = ["(",")","'","[","]", " "]
	for i in clean:
	    data = data.replace(i, "")
	return HttpResponse(str(data))

@csrf_exempt
def gettime(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT * FROM Leaderboard ORDER BY Time_Spend DESC")
	data = ""
	for row in c.fetchall():
	        data = data + str(row) + "<br>"
	clean = ["(",")","'","[","]", " "]
	for i in clean:
	    data = data.replace(i, "")
	return HttpResponse(str(data))
