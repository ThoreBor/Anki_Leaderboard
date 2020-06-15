from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import json
from datetime import datetime


@csrf_exempt
def sync(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()

	User = request.POST.get("Username", "")
	Streak = request.POST.get("Streak", "")
	Cards = request.POST.get("Cards", "")
	Time = request.POST.get("Time", "")
	Sync_Date = request.POST.get("Sync_Date", "")
	Month = request.POST.get("Month","")
	Subject = request.POST.get("Subject","")
	Country = request.POST.get("Country","")
	Retention = request.POST.get("Retention","")
	Token = request.POST.get("Token", None)

	if Retention == "":
		Retention = 0
	if Month == "":
		Month = 0

	### Filter ###

	if User == "" or len(User) > 15:
		return HttpResponse("Error - invalid username")

	if not Streak.isdigit():
		return HttpResponse("Error - invalid streak value")

	if not Cards.isdigit():
		return HttpResponse("Error - invalid cards value")

	try:
		float(Time)
	except:
		return HttpResponse("Error - invalid time value")

	try:
		check_sync_date = Sync_Date.replace(" ", "")
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

	### Commit to database ###

	if c.execute("SELECT Username FROM Leaderboard WHERE Username = (?)", (User,)).fetchone():
		t = c.execute("SELECT Username, Token FROM Leaderboard WHERE Username = (?)", (User,)).fetchone()
		if t[1] == Token or t[1] is None or t[1] == "":
			c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Subject = (?), Country = (?), Retention = (?), Token = (?) WHERE Username = (?) ", (Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention, Token, User))
			conn.commit()
			print("Updated entry: " + str(User))
			return HttpResponse("Done!")
		else:
			return HttpResponse("Error - invalid token")
	else:
		c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention, Token) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?)', (User, Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention, Token))
		conn.commit()
		print("Created new entry: " + str(User))
		return HttpResponse("Done!")


@csrf_exempt
def all_users(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Username_List = []
	c.execute("SELECT Username FROM Leaderboard")
	for i in c.fetchall():
		username = i[0]
		Username_List.append(username)
	return HttpResponse(json.dumps(Username_List))

@csrf_exempt
def get_data(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention FROM Leaderboard ORDER BY Cards DESC")
	return HttpResponse(json.dumps(c.fetchall()))

@csrf_exempt
def delete(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	User = request.POST.get("Username", "")
	Token = request.POST.get("Token", None)

	if c.execute("SELECT Username FROM Leaderboard WHERE Username = (?)", (User,)).fetchone():
		t = c.execute("SELECT Username, Token FROM Leaderboard WHERE Username = (?)", (User,)).fetchone()
		if t[1] == Token or t[1] is None or t[1] == "":
			c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (User,))
			conn.commit()
			print("Deleted account: " + str(User))
			return HttpResponse("Deleted")
		return HttpResponse("Failed")