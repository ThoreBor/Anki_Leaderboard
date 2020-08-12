from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import json
from datetime import datetime
import praw

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

	league_reviews = request.POST.get("league_reviews", 0)
	league_time = request.POST.get("league_time", 0)
	league_retention = request.POST.get("league_retention", 0)

	Token = request.POST.get("Token_v3", None)
	Version = request.POST.get("Version", None)

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

	try:
		int(league_reviews)
	except:
		return HttpResponse("Error - invalid league_reviews value")

	try:
		float(league_time)
	except:
		return HttpResponse("Error - invalid league_time value")

	try:
		float(league_retention)
	except:
		return HttpResponse("Error - invalid league_retention value")

	xp = int((4 * float(league_time) + 2 * int(league_reviews)) * float(league_retention))

	### Commit to database ###

	if c.execute("SELECT Username FROM Leaderboard WHERE Username = (?)", (User,)).fetchone():
		t = c.execute("SELECT Username, Token FROM Leaderboard WHERE Username = (?)", (User,)).fetchone()
		if t[1] == Token or t[1] is None:
			c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Subject = (?), Country = (?), Retention = (?), Token = (?) WHERE Username = (?) ", (Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention, Token, User))
			conn.commit()

			if c.execute("SELECT username FROM League WHERE username = (?)", (User,)).fetchone():
			    c.execute("UPDATE League SET xp = (?), time_spend = (?), reviews = (?), retention = (?) WHERE username = (?) ", (xp, league_time, league_reviews, league_retention, User))
			    conn.commit()
			else:
			    c.execute('INSERT INTO League (username, xp, time_spend, reviews, retention, league) VALUES(?, ?, ?, ?, ?, ?)', (User, xp, league_time, league_reviews, league_retention, "Delta"))
			    conn.commit()

			print("Updated entry: " + str(User) + " (" + str(Version) + ")")
			return HttpResponse("Done!")
		else:
			with open('/home/ankileaderboard/anki_leaderboard_pythonanywhere/main/config.txt') as json_file:
				data = json.load(json_file)
			r = praw.Reddit(username = data["un"], password = data["pw"], client_id = data["cid"], client_secret = data["cs"], user_agent = data["ua"])
			r.redditor('Ttime5').message('Verification Error', "Username: " + str(User) + "\n" + "Token: " + str(Token) + "\n" + str(t[1]) + "\n" + "Version: " + str(Version))
			print("Verification error: " + str(User))
			return HttpResponse("<h3>Error - invalid token</h3>The verification token you send doesn't match the one in the database. Make sure that you're using the newest version. <br><br>If you recently changed devices, you need to copy your old meta.json file into the leaderboard add-on folder of your new device.<br><br>If you think that this error is a bug, please open a new issue on <a href='https://github.com/ThoreBor/Anki_Leaderboard/issues'>GitHub</a> or contact me on <a href='https://www.reddit.com/user/Ttime5'>Reddit</a>.")
	else:
		c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention, Token) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?)', (User, Streak, Cards, Time, Sync_Date, Month, Subject, Country, Retention, Token))
		conn.commit()
		c.execute('INSERT INTO League (username, xp, time_spend, reviews, retention, league) VALUES(?, ?, ?, ?, ?, ?)', (User, xp, league_time, league_reviews, league_retention, "Delta"))
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
	sortby = request.POST.get("sortby", "Cards")
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention FROM Leaderboard ORDER BY {} DESC".format(sortby))
	return HttpResponse(json.dumps(c.fetchall()))

@csrf_exempt
def league_data(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league FROM League ORDER BY xp DESC")
	return HttpResponse(json.dumps(c.fetchall()))

@csrf_exempt
def delete(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	User = request.POST.get("Username", "")
	Token = request.POST.get("Token_v3", None)

	if c.execute("SELECT Username FROM Leaderboard WHERE Username = (?)", (User,)).fetchone():
		t = c.execute("SELECT Username, Token FROM Leaderboard WHERE Username = (?)", (User,)).fetchone()
		if t[1] == Token or t[1] is None:
			c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (User,))
			conn.commit()
			c.execute("DELETE FROM League WHERE username = (?)", (User,))
			conn.commit()
			print("Deleted account: " + str(User))
			return HttpResponse("Deleted")
		return HttpResponse("Failed")
@csrf_exempt
def create_group(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Group_Name = request.POST.get("Group_Name", None)
	if c.execute("SELECT Group_Name FROM Groups WHERE Group_Name = (?)", (Group_Name,)).fetchone():
		pass
	else:
		if Group_Name:
			c.execute('INSERT INTO Groups (Group_Name) VALUES(?)', (Group_Name,))
			conn.commit()
			print(f"Created new group {Group_Name}")
			return HttpResponse("Done!")
@csrf_exempt
def groups(request):
	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
	c = conn.cursor()
	Group_List = []
	c.execute("SELECT Group_Name FROM Groups")
	for i in c.fetchall():
		Group_Name = i[0]
		Group_List.append(Group_Name)
	return HttpResponse(json.dumps((sorted(Group_List, key=str.lower))))

def season(request):
	return HttpResponse(json.dumps([[2020,8,1,0,0,0],[2020,9,1,0,0,0]]))