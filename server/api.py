from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ratelimit.decorators import ratelimit
import sqlite3
import json
from datetime import datetime
import praw
import pyrebase
from .config import praw_config, firebase_config
#database_path = '/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db'
database_path = 'Leaderboard.db'

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def signUp(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	firebase = pyrebase.initialize_app(firebase_config)
	auth = firebase.auth()
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	sync_date = request.POST.get("sync_date", "")
	version = request.POST.get("version", "")
	try:
		response = auth.create_user_with_email_and_password(email, pwd)
	except:
		return HttpResponse(json.dumps("Firebase error"))	
	token = response['idToken']
	c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Country, Retention, Token, version) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?)', (username, 0, 0, 0, sync_date, 0, 0, 0, token, version))
	conn.commit()
	return HttpResponse(json.dumps(token))

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def logIn(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	firebase = pyrebase.initialize_app(firebase_config)
	auth = firebase.auth()
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	try:
		response = auth.sign_in_with_email_and_password(email, pwd)
	except Exception as e:
		print(str(e))
		return HttpResponse(json.dumps("Firebase error"))	
	token = response['idToken']
	c.execute("UPDATE Leaderboard SET Token = (?) WHERE Username = (?) ", (token, username))
	conn.commit()
	return HttpResponse(json.dumps(token))

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def deleteAccount(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	firebase = pyrebase.initialize_app(firebase_config)
	auth = firebase.auth()
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	firebaseToken = request.POST.get("firebaseToken", "")
	auth_local = auth_user(username, firebaseToken)
	if auth_local == 200:
		try:
			response = auth.sign_in_with_email_and_password(email, pwd)
			auth.delete_user_account(response['idToken'])
		except:
			return HttpResponse("<h3>404 error</h3>Wrong e-mail address or wrong password.")
		c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (username,))
		conn.commit()
		c.execute("DELETE FROM League WHERE username = (?)", (username,))
		conn.commit()
		print(f"Deleted account: {username}")
		return HttpResponse("Deleted")
	if auth_local == 401:
		return render(request, "authError.html")
	if auth_local == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def updateAccount(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	firebase = pyrebase.initialize_app(firebase_config)
	auth = firebase.auth()
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	old_token = request.POST.get("old_token", "")
	auth_local = auth_user(username, old_token)
	if auth_local == 200:
		try:
			response = auth.create_user_with_email_and_password(email, pwd)
		except:
			return HttpResponse(json.dumps("<h3>404 error</h3>E-Mail address already exists, or password is too short."))
		token = response['idToken']
		c.execute("UPDATE Leaderboard SET Token = (?) WHERE Username = (?) ", (token, username))
		conn.commit()
		print(f"Updated account: {username}")
		return HttpResponse(json.dumps(token))
	else:
		return HttpResponse(json.dumps("<h3>404 error</h3>Couldn't find user, or token invalid."))

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def resetPassword(request):
	email = request.POST.get("email", "")
	firebase = pyrebase.initialize_app(firebase_config)
	auth = firebase.auth()
	try:
		response = auth.send_password_reset_email(email)
	except:
		return HttpResponse(json.dumps("Firebase error"))
	return HttpResponse(json.dumps("Done!"))

def auth_user(user, token):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	t = c.execute("SELECT Token FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()
	if not t:
		return 404
	if t[0] == token or t[0] is None:
		return 200
	else:
		print(f"auth_user 401: {user}")
		return 401

def auth_group(group, pwd, user):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	p = c.execute("SELECT pwd FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()
	banned = json.loads(c.execute("SELECT banned FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
	if not p:
		print(f"auth_group 404: {user} {group}")
		return "<h3>404 error</h3>This group doesn't exist."
	if p[0] == pwd or p[0] is None:
		if user in banned:
			print(f"auth_group 403: {user} {group}")
			return "<h3>403 error</h3>You're banned from this group."
		return 200
	else:
		print(f"auth_group 401: {user} {group}")
		return "<h3>401 error</h3>Wrong group password."

def auth_admin(user, group):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	admins = json.loads(c.execute("SELECT admins FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
	if user in admins:
		return 200
	else:
		print(f"auth_admin 403: {user} {group}")
		return "<h3>401 error</h3>You are not an admin of this group."

def filter(User, Streak, Cards, Time, Sync_Date, Month, Retention, league_reviews, league_time, league_retention, league_days_learned):
	if User == "" or len(User) > 15:
		return "Error - invalid username"

	if "🥇" in User or "🥈" in User or "🥉" in User or "|" in User:
		return """<h3>Error - invalid username</h3>
			🥇, 🥈, 🥉 and | aren't allowed in usernames anymore.<br><br>
			If you already have an account that is affected by this, please write an e-mail
			to leaderboard_support@protonmail.com or dm me on <a href="https://www.reddit.com/user/Ttime5">Reddit</a> so we can sort this out.
			Alternatively, you can also create a new account, but keep in mind that this would reset your league progress."""

	if not Streak.isdigit():
		return "Error - invalid streak value"

	if not Cards.isdigit():
		return "Error - invalid cards value"

	try:
		float(Time)
	except:
		return "Error - invalid time value"

	try:
		check_sync_date = datetime.strptime(Sync_Date, '%Y-%m-%d %H:%M:%S.%f')
	except:
		return "Error invalid timestamp"

	try:
		int(Month)
	except:
		return "Error - invalid month value"

	try:
		float(Retention)
	except:
		return "Error - invalid retention value"

	try:
		int(league_reviews)
	except:
		return "Error - invalid league_reviews value"

	try:
		float(league_time)
	except:
		return "Error - invalid league_time value"

	try:
		float(league_retention)
	except:
		return "Error - invalid league_retention value"

	try:
		float(league_days_learned)
	except:
		return "Error - invalid league_days_learned value"

	return False

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def sync(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	User = request.POST.get("Username", "")
	Streak = request.POST.get("Streak", 0)
	Cards = request.POST.get("Cards", 0)
	Time = request.POST.get("Time", 0)
	Sync_Date = request.POST.get("Sync_Date", "")
	Month = request.POST.get("Month", 0)
	Country = request.POST.get("Country","")
	Retention = request.POST.get("Retention", 0.0)

	league_reviews = request.POST.get("league_reviews", 0)
	league_time = request.POST.get("league_time", 0)
	league_retention = request.POST.get("league_retention", 0)
	league_days_learned = request.POST.get("league_days_percent", 0)
	Update_League = request.POST.get("Update_League", True)

	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	Token = firebaseToken if firebaseToken else Token_v3
	Version = request.POST.get("Version", None)

	try:
		sus = c.execute("SELECT suspended FROM Leaderboard WHERE Username = (?)", (User,)).fetchone()[0]
		if sus:
			return HttpResponse(f"<h3>Account suspended</h3>This account was suspended due to the following reason:<br><br>{sus}<br><br>Please write an e-mail to leaderboard_support@protonmail.com or a message me on <a href='https://www.reddit.com/user/Ttime5'>Reddit</a>, if you think that this was a mistake.")
	except:
		pass

	f = filter(User, Streak, Cards, Time, Sync_Date, Month, Retention, league_reviews, league_time, league_retention, league_days_learned)
	if f:
		return HttpResponse(f)

	### XP ###

	if float(league_retention) >= 85:
		retention_bonus = 1
	if float(league_retention) < 85 and float(league_retention) >= 70:
		retention_bonus = 0.85
	if float(league_retention) < 70 and float(league_retention) >= 55:
		retention_bonus = 0.70
	if float(league_retention) < 55 and float(league_retention) >= 40:
		retention_bonus = 0.55
	if float(league_retention) < 40 and float(league_retention) >= 25:
		retention_bonus = 0.40
	if float(league_retention) < 25 and float(league_retention) >= 10:
		retention_bonus = 0.25
	if float(league_retention) < 10:
		retention_bonus = 0

	xp = int(float(league_days_learned) * ((6 * float(league_time) * 1) + (2 * int(league_reviews) * float(retention_bonus))))

	### Commit to database ###

	auth = auth_user(User, Token)
	if auth == 200:
		c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Country = (?), Retention = (?), Token = (?), version = (?) WHERE Username = (?) ", (Streak, Cards, Time, Sync_Date, Month, Country, Retention, Token, Version, User))
		conn.commit()
		if Update_League == True:
			if c.execute("SELECT username FROM League WHERE username = (?)", (User,)).fetchone():
				c.execute("UPDATE League SET xp = (?), time_spend = (?), reviews = (?), retention = (?), days_learned = (?) WHERE username = (?) ", (xp, league_time, league_reviews, league_retention, league_days_learned, User))
				conn.commit()
			else:
				c.execute('INSERT INTO League (username, xp, time_spend, reviews, retention, league, days_learned) VALUES(?, ?, ?, ?, ?, ?, ?)', (User, xp, league_time, league_reviews, league_retention, "Delta", league_days_learned))
				conn.commit()

		print(f"Updated account: {User} ({Version})")
		return HttpResponse("Done!")
	if auth == 401:
		return render(request, "authError.html")
	if auth == 404:
		c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Country, Retention, Token, version) VALUES(?, ?, ?, ?, ?, ?, ?, ?,?,?)', (User, Streak, Cards, Time, Sync_Date, Month, Country, Retention, Token, Version))
		conn.commit()
		if Update_League == True:
			c.execute('INSERT INTO League (username, xp, time_spend, reviews, retention, league, days_learned) VALUES(?, ?, ?, ?, ?, ?, ?)', (User, xp, league_time, league_reviews, league_retention, "Delta", league_days_learned))
			conn.commit()
		print(f"Created new account: {User}")
		return HttpResponse("Done!")

### OLD, for < v1.7.0
@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def delete(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	User = request.POST.get("Username", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	Token = firebaseToken if firebaseToken else Token_v3

	auth = auth_user(User, Token)
	if auth == 200:
		c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (User,))
		conn.commit()
		c.execute("DELETE FROM League WHERE username = (?)", (User,))
		conn.commit()
		print(f"Deleted account: {User}")
		return HttpResponse("Deleted")
	if auth == 401:
		return render(request, "authError.html")
	if auth == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def all_users(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	Username_List = []
	c.execute("SELECT Username FROM Leaderboard")
	for i in c.fetchall():
		username = i[0]
		Username_List.append(username)
	return HttpResponse(json.dumps(Username_List))

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def get_data(request):
	sortby = request.POST.get("sortby", "Cards")
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY {} DESC".format(sortby))
	data = []
	for row in c.fetchall():
		if row[9]:
			data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], json.loads(row[9])])
		else:
			data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], []])
	return HttpResponse(json.dumps(data))

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def league_data(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	c.execute("SELECT username, xp, time_spend, reviews, retention, league, history, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")
	return HttpResponse(json.dumps(c.fetchall()))

@ratelimit(key='ip', rate='10/h', block=True)
@csrf_exempt
def create_group(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	Group_Name = request.POST.get("Group_Name", None).strip()
	User = request.POST.get("User", None)
	Pwd = request.POST.get("Pwd", None)

	if c.execute("SELECT Group_Name FROM Groups WHERE Group_Name = (?)", (Group_Name,)).fetchone():
		return HttpResponse("This group already exists.")
	else:
		c.execute('INSERT INTO Groups (Group_Name, pwd, admins, banned) VALUES(?, ?, ?, ?)', (Group_Name, Pwd, json.dumps([User]), json.dumps([])))
		conn.commit()
		data = praw_config
		r = praw.Reddit(username = data["un"], password = data["pw"], client_id = data["cid"], client_secret = data["cs"], user_agent = data["ua"])
		#r.redditor('Ttime5').message('Group Request', f"{User} requested a new group: {Group_Name}")
		print(f"{User} requested a new group: {Group_Name}")
		return HttpResponse("Done!")

@csrf_exempt
def joinGroup(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	username = request.POST.get("username", None)
	group = request.POST.get("group", None)
	pwd = request.POST.get("pwd", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	token = firebaseToken if firebaseToken else Token_v3

	group_list = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
	if not group_list:
		groups = [group]
	else:
		groups = json.loads(group_list)
		if group not in groups:
			groups.append(group)

	authUser = auth_user(username, token)
	if authUser == 200:
		authGroup = auth_group(group, pwd, username)
		if authGroup == 200:
			c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?)", (json.dumps(groups), username))
			conn.commit()
			c.execute("UPDATE Leaderboard SET Subject = (?) WHERE Username = (?)", (group.replace(" ", ""), username))
			conn.commit()
			print(f"{username} joined {group}")
			return HttpResponse("Done!")
		else:
			return HttpResponse(authGroup)
	if authUser == 401:
		return render(request, "authError.html")
	if authUser == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
def manageGroup(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	username = request.POST.get("user", None)
	group = request.POST.get("group", None)
	oldPwd = request.POST.get("oldPwd", None)
	newPwd = request.POST.get("newPwd", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	token = firebaseToken if firebaseToken else Token_v3
	addAdmin = request.POST.get("addAdmin", None)
	admins = json.loads(c.execute("SELECT admins FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
	admins.append(addAdmin)

	authUser = auth_user(username, token)
	if authUser == 200:
		authGroup = auth_group(group, oldPwd, username)
		if authGroup == 200:
			authAdmin = auth_admin(username, group)
			if authAdmin == 200:
				c.execute("UPDATE Groups SET pwd = (?), admins = (?) WHERE Group_Name = (?) ", (newPwd, json.dumps(admins), group))
				conn.commit()
				print(f"{username} made some changes to {group}")
				return HttpResponse("Done!")
			else:
				return HttpResponse(authAdmin)
		else:
			return HttpResponse(authGroup)
	if authUser == 401:
		return render(request, "authError.html")
	if authUser == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
def leaveGroup(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	group = request.POST.get("group", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	token = firebaseToken if firebaseToken else Token_v3
	user = request.POST.get("user", None)
	group_list = json.loads(c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()[0])

	authUser = auth_user(user, token)
	if authUser == 200:
		group_list.remove(group)
		c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?) ", (json.dumps(group_list), user))
		conn.commit()
		c.execute("UPDATE Leaderboard SET Subject = (?) WHERE Username = (?) ", ('', user))
		conn.commit()
		print(f"{user} left {group}")
		return HttpResponse("Done!")
	if authUser == 401:
		return render(request, "authError.html")
	if authUser == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
def groups(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	Group_List = []
	c.execute("SELECT Group_Name FROM Groups WHERE verified = 1")
	for i in c.fetchall():
		Group_Name = i[0]
		Group_List.append(Group_Name)
	return HttpResponse(json.dumps((sorted(Group_List, key=str.lower))))

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def banUser(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	toBan = request.POST.get("toBan", None)
	group = request.POST.get("group", None)
	pwd = request.POST.get("pwd", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	token = firebaseToken if firebaseToken else Token_v3
	user = request.POST.get("user", None)
	g = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (toBan,)).fetchone()[0]
	banned = json.loads(c.execute("SELECT banned FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
	banned.append(toBan)
	if not g:
		groups = [group]
	else:
		groups = json.loads(g)

	authUser = auth_user(user, token)
	if authUser == 200:
		authGroup = auth_group(group, pwd, user)
		if authGroup == 200:
			authAdmin = auth_admin(user, group)
			if authAdmin == 200:
				groups.remove(group)
				c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?) ", (json.dumps(groups), toBan))
				conn.commit()
				c.execute("UPDATE Groups SET banned = (?) WHERE Group_Name = (?) ", (json.dumps(banned), group))
				conn.commit()
				c.execute("UPDATE Leaderboard SET Subject = (?) WHERE Username = (?) ", (None, toBan))
				conn.commit()
				print(f"{toBan} was banned from {group} by {user}")
				return HttpResponse("Done!")
			else:
				return HttpResponse(authAdmin)
		else:
			return HttpResponse(authGroup)
	if authUser == 401:
		return render(request, "authError.html")
	if authUser == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
@ratelimit(key='ip', rate='10/h', block=True)
def setStatus(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	statusMsg = request.POST.get("status", None)
	if len(statusMsg) > 280:
		statusMsg = None
	username = request.POST.get("username", None)
	Token_v3 = request.POST.get("Token_v3", None)
	firebaseToken = request.POST.get("firebaseToken", None)
	Token = firebaseToken if firebaseToken else Token_v3

	auth = auth_user(username, Token)
	if auth == 200:
		c.execute("UPDATE Leaderboard SET Status = (?) WHERE username = (?) ", (statusMsg, username))
		conn.commit()
		return HttpResponse("Done!")
	if auth == 401:
		return render(request, "authError.html")
	if auth == 404:
		return HttpResponse("<h3>404 error</h3>Couldn't find user.")

@csrf_exempt
def getStatus(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	username = request.POST.get("username", None)
	return HttpResponse(json.dumps(c.execute("SELECT Status FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()))

@csrf_exempt
def getUserinfo(request):
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	user = request.POST.get("user", None)
	a = request.POST.get("a", False)
	if a:
		country = c.execute("SELECT Country FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()[0]
		group = c.execute("SELECT Subject, groups FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()
		g_old = group[0]
		if not group[1]:
			g_new = []
		else:
			g_new = json.loads(group[1])
		if g_old not in [group.replace(" ", "") for group in g_new]:
			g_new.append(g_old)
		league = c.execute("SELECT league, history FROM League WHERE username = (?)", (user,)).fetchone()
		status = c.execute("SELECT Status FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()[0]
		return HttpResponse(json.dumps([country, g_new, league[0], league[1], status]))
	else:
		u1 = c.execute("SELECT Country, Subject FROM Leaderboard WHERE Username = (?)", (user,)).fetchone()
		u2 = c.execute("SELECT league, history FROM League WHERE username = (?)", (user,)).fetchone()
		return HttpResponse(json.dumps(u1 + u2))

@csrf_exempt
@ratelimit(key='ip', rate='100/h', block=True)
def reportUser(request):
	user = request.POST.get("user", "")
	report_user = request.POST.get("reportUser", "")
	message = request.POST.get("message", "")
	data = praw_config
	r = praw.Reddit(username = data["un"], password = data["pw"], client_id = data["cid"], client_secret = data["cs"], user_agent = data["ua"])
	r.redditor('Ttime5').message('Report', f"{user} reported {report_user}. \n Message: {message}")
	return HttpResponse("Done!")

def season(request):
	return HttpResponse(json.dumps([[2021,7,23,0,0,0],[2021,8,6,0,0,0], "Season 22"]))