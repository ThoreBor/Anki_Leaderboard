from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import sqlite3
import json
from datetime import datetime
import praw
from argon2 import PasswordHasher
import smtplib
from email.message import EmailMessage
import secrets

from .config import praw_config, smtp_config
from .checkInput import *

#database_path = '/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db'
database_path = 'Leaderboard.db'

# Authentication

def authUser(username, token):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Check if user exists
	doesExist = True if c.execute("SELECT EXISTS(SELECT 1 FROM Leaderboard WHERE Username = (?))", (username,)).fetchone()[0] == 1 else False

	# Authenticate user
	if doesExist:
		checkToken = c.execute("SELECT Token FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		if checkToken == token:
			return 200
		else:
			print("authUser 401")
			return 401
	else:
		return 404

def authGroup(username, group, pwd):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Check if group exists
	doesExist = True if c.execute("SELECT EXISTS(SELECT 1 FROM Groups WHERE Group_Name = (?))", (group,)).fetchone()[0] == 1 else False

	if doesExist:
		groupPwd = c.execute("SELECT pwd FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0]
		banned = json.loads(c.execute("SELECT banned FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
		
		# Authenticate group password, check if user is banned
		if groupPwd == pwd:
			if username in banned:
				print("authGroup 403")
				return 403
			else:
				return 200
		else:
			print("authGroup 401")
			return 401
	else:
		print("authGroup 404")
		return 404

def authAdmin(username, group):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Check if user is admin
	admins = json.loads(c.execute("SELECT admins FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
	if username in admins:
		return 200
	else:
		print("authAdmin 403")
		return 403

# Manage Account

@csrf_exempt
def signUp(request):
	# Connect to the database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	
	# Get data from client
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	syncDate = request.POST.get("syncDate", "")
	version = request.POST.get("version", "")
	
	# Check if username is valid
	isTaken = True if c.execute("SELECT EXISTS(SELECT 1 FROM Leaderboard WHERE Username= (?))", (username,)).fetchone()[0] == 1 else False
	if isTaken:
		response = HttpResponse("<h1>Sign-up Error</h1>This username is already taken. Please choose another one.")
		response.status_code = 400
		return response
	if not usernameIsValid(username):
		response = HttpResponse("<h1>Sign-up Error</h1>This username is too long. The username must have less than 15 characters and can't contain any of these characters: 🥇🥈🥉|")
		response.status_code = 400
		return response

	# Check other input
	if not emailIsValid(email) or not dateIsValid(syncDate):
		response = HttpResponse("<h1>Sign-up Error</h1>Invalid input.")
		response.status_code = 400
		return response
	
	# Hash password and create token
	ph = PasswordHasher()
	pwdHash = ph.hash(pwd)
	authToken = secrets.token_hex(nbytes=64)
	
	# Create user in database and return token for authentication
	c.execute('INSERT INTO Leaderboard (Username, Streak, Cards , Time_Spend, Sync_Date, Month, Country, Retention, Token, version, email, hash) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, 0, 0, 0, syncDate, 0, 0, 0, authToken, version, email, pwdHash))
	conn.commit()
	c.execute('INSERT INTO League (username, xp, time_spend, reviews, retention, league, days_learned) VALUES(?, ?, ?, ?, ?, ?, ?)', (username, xp, 0, 0, 0, "Delta", 0))
	conn.commit()
	response = HttpResponse(json.dumps(authToken))
	response.status_code = 201
	print("New sign-up")
	return response

@csrf_exempt
def logIn(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")

	# Authenticate user
	try:
		pwdHash = c.execute("SELECT hash FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		ph = PasswordHasher()
		ph.verify(pwdHash, pwd)
	except:
		response = HttpResponse("<h1>Log-in Error</h1>Wrong password or wrong username.")
		response.status_code = 400
		return response

	# Rehash password and create token for authentication
	pwdHash = ph.hash(pwd)
	authToken = secrets.token_hex(nbytes=64)

	# Update hash and token in database and return token
	c.execute("UPDATE Leaderboard SET Token = (?), hash = (?) WHERE Username = (?)", (authToken, pwdHash, username))
	conn.commit()
	response = HttpResponse(json.dumps(authToken))
	response.status_code = 200
	print("New login")
	return response

@csrf_exempt
def deleteAccount(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	
	# Authenticate user
	try:
		pwdHash = c.execute("SELECT hash FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		ph = PasswordHasher()
		ph.verify(pwdHash, pwd)
	except:
		response = HttpResponse("<h1>Delete Error</h1>Wrong password or wrong username.")
		response.status_code = 400
		return response

	# Update group member number of the groups the user was in
	groupList = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
	if not groupList:
		groups = []
	else:
		groups = json.loads(groupList)
	for i in groups:
		members = c.execute("SELECT members FROM Groups WHERE Group_Name = (?)", (i,)).fetchone()[0]
		c.execute("UPDATE Groups SET members = (?) WHERE Group_Name = (?)", (members - 1, i))
		conn.commit()
	
	# Delete data from leaderboard and leagues
	c.execute("DELETE FROM Leaderboard WHERE Username = (?)", (username,))
	conn.commit()
	c.execute("DELETE FROM League WHERE username = (?)", (username,))
	conn.commit()
	print("Deleted account")
	return HttpResponse(status=204)

@csrf_exempt
def changeUsername(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", None)
	newUsername = request.POST.get("newUsername", None)
	pwd = request.POST.get("pwd", None)

	# Check if new username is valid
	isTaken = True if c.execute("SELECT EXISTS(SELECT 1 FROM Leaderboard WHERE Username= (?))", (newUsername,)).fetchone()[0] == 1 else False
	if not usernameIsValid(username) or not usernameIsValid(newUsername):
		response = HttpResponse("<h1>Change Username Error</h1>This username is too long. The username must have less than 15 characters.")
		response.status_code = 400
		return response

	if not isTaken:
		# Authenticate user
		try:
			pwdHash = c.execute("SELECT hash FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
			ph = PasswordHasher()
			ph.verify(pwdHash, pwd)
		except:
			response = HttpResponse("<h1>Change Username Error</h1>Wrong password or wrong username.")
			response.status_code = 400
			return response

		# Rehash password and create token for authentication
		pwdHash = ph.hash(pwd)
		authToken = secrets.token_hex(nbytes=64)
		
		# Change username and update token and hash, return token
		c.execute("UPDATE Leaderboard SET Token = (?), hash = (?), Username = (?) WHERE Username = (?)", (authToken, pwdHash, newUsername, username))
		c.execute("UPDATE League SET username = (?) WHERE username = (?)", (newUsername, username))
		conn.commit()
		response = HttpResponse(json.dumps(authToken))
		response.status_code = 200
		print("Changed username")
		return response
	else:
		response = HttpResponse("<h1>Change Username Error</h1>This username is already taken. Please choose another one.")
		response.status_code = 400
		return response

@csrf_exempt
def resetPassword(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()
	
	# Get data from client
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")

	# Check if user with email exists
	doesExist = True if c.execute("SELECT EXISTS(SELECT 1 FROM Leaderboard WHERE Username = (?) AND email = (?))", (username, email)).fetchone()[0] == 1 else False
	
	if doesExist:
		# Create email reset token
		token = secrets.token_hex(nbytes=64)

		# Create email
		msg = EmailMessage()
		email_message = f"""
Hello {username},

To reset your leaderboard account password, click this link:
http://127.0.0.1:8000/api/v2/newPassword/{token}
Ignore this mail if you don't want to reset your password.

Your Leaderboard Team
"""
		msg.set_content(email_message)
		msg['Subject'] = 'Reset password'
		msg['From'] = smtp_config["sender_email"]
		msg['To'] = email
		
		try:
			# Send email
			server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
			server.ehlo()
			server.login(smtp_config["sender_email"], smtp_config["sender_pwd"])
			server.send_message(msg)
			server.close()

			# Commit token to database
			c.execute("UPDATE Leaderboard SET emailReset = (?) WHERE Username = (?) AND email = (?)", (token, username, email))
			conn.commit()
			print("Sent reset password email")
			return HttpResponse(status=200)
		except:
			response = HttpResponse("<h1>Reset Password Error</h1>A problem occurred while sending the email. Please try again, or contact leaderboard_support@protonmail.com if the problem persist.")
			response.status_code = 500
			return response
	else:
		response = HttpResponse("<h1>Reset Password Error</h1>Can't find username with that email address.")
		response.status_code = 400
		return response

def newPassword(request, token):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	if request.method == "POST":
		# Get data from html form and token from url
		username = request.POST.get("username", "")
		pwd = request.POST.get("pwd", "")
		rpwd = request.POST.get("rpwd", "")
		token = request.POST.get("token", "")

		# Check if passwords are the same
		if pwd != rpwd:
			messages.error(request, "Error - Passwords are not the same. Try again.")
			return HttpResponseRedirect('/')
		
		# Authenticate reset token
		emailReset = c.execute("SELECT emailReset FROM Leaderboard WHERE Username = (?) ", (username,)).fetchone()[0]
		if emailReset != token:
			return HttpResponse("<h1>Forbidden</h1>")
		
		# Create and commit hash, delete reset token
		ph = PasswordHasher()
		pwdHash = ph.hash(pwd)
		c.execute("UPDATE Leaderboard SET emailReset = (?), hash = (?) WHERE Username = (?) ", (None, pwdHash, username))
		conn.commit()
		messages.success(request, "Your password has been changed successfully!")
		return HttpResponseRedirect('/')
	else:
		return render(request, "newPassword.html", {"token": token})

#Manage groups

@csrf_exempt
def groups(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Return all groups
	groupList = [i[0] for i in c.execute("SELECT Group_Name FROM Groups WHERE verified = 1").fetchall()]
	response = HttpResponse(json.dumps((sorted(groupList, key=str.lower))))
	response.status_code = 200
	return response

@csrf_exempt
def joinGroup(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", None)
	group = request.POST.get("group", None)
	pwd = request.POST.get("pwd", None)
	authToken = request.POST.get("authToken", None)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		groupAuth = authGroup(username, group, pwd)
		if groupAuth == 200:
			# Get groups and add new group
			groupList = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
			if not groupList:
				groups = [group]
			else:
				groups = json.loads(groupList)
				if group not in groups:
					groups.append(group)
			# Update groups
			c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?)", (json.dumps(groups), username))
			conn.commit()
			# Update members
			members = c.execute("SELECT members FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0]
			c.execute("UPDATE Groups SET members = (?) WHERE Group_Name = (?)", (members + 1, group))
			conn.commit()
			
			print(f"Somebody joined {group}")
			return HttpResponse(status=200)
		
		if groupAuth == 401:
			response = HttpResponse("<h1>Join Group Error</h1>Wrong group password.")
			response.status_code = 401
			return response

		if groupAuth == 403:
			response = HttpResponse("<h1>Join Group Error</h1>You're banned from this group")
			response.status_code = 403
			return response

		if groupAuth == 404:
			response = HttpResponse("<h1>Join Group Error</h1>Couldn't find group.")
			response.status_code = 404
			return response
	
	if userAuth == 401:
		response = HttpResponse("<h1>Join Group Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if userAuth == 404:
		response = HttpResponse("<h1>Join Group Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def createGroup(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	groupName = request.POST.get("groupName", None).strip()
	username = request.POST.get("username", None)
	pwd = request.POST.get("pwd", None)

	# Check if group name is taken
	isTaken = True if c.execute("SELECT EXISTS(SELECT 1 FROM Groups WHERE Group_Name = (?))", (groupName,)).fetchone()[0] == 1 else False
	
	if isTaken or not strIsValid(groupName, 50):
		response = HttpResponse("<h1>Create Group Error</h1>This group name is already taken or too long.")
		response.status_code = 400
		return response
	else:
		# Create group
		c.execute('INSERT INTO Groups (Group_Name, verified, pwd, admins, banned, members) VALUES(?, ?, ?, ?, ?, ?)', (groupName, 1, pwd, json.dumps([username]), json.dumps([]), 0))
		conn.commit()
		print(f"New group: {groupName}")
		return HttpResponse(status=200)

@csrf_exempt
def leaveGroup(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	group = request.POST.get("group", None)
	authToken = request.POST.get("authToken", None)
	username = request.POST.get("username", None)

	# Check if group exists
	doesExist = True if c.execute("SELECT EXISTS(SELECT 1 FROM Groups WHERE Group_Name= (?))", (group,)).fetchone()[0] == 1 else False
	if not doesExist:
		return HttpResponse(status=200)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		# Remove group
		groupList = json.loads(c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0])
		if group in groupList:
			groupList.remove(group)
		else:
			pass
		c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?) ", (json.dumps(groupList), username))
		conn.commit()
		c.execute("UPDATE Leaderboard SET Subject = (?) WHERE Username = (?) ", ('', username))
		conn.commit()
		# Remove member
		members = c.execute("SELECT members FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0]
		c.execute("UPDATE Groups SET members = (?) WHERE Group_Name = (?)", (members - 1, group))
		conn.commit()
		print(f"Somebody left {group}")
		return HttpResponse(status=200)
	
	if userAuth == 401:
		response = HttpResponse("<h1>Leave Group Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if userAuth == 404:
		response = HttpResponse("<h1>Leave Group Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def manageGroup(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", None)
	group = request.POST.get("group", None)
	oldPwd = request.POST.get("oldPwd", None)
	newPwd = request.POST.get("newPwd", None)
	authToken = request.POST.get("authToken", None)
	addAdmin = request.POST.get("addAdmin", None)

	# Check input
	if not strIsValid(newPwd, 41) or not strIsValid(addAdmin, 16):
		response = HttpResponse("<h1>Manage Group Error</h1>Invalid input.")
		response = HttpResponse("<h1>Sign-up Error</h1>Invalid input.")
		response.status_code = 400
		return response

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		groupAuth = authGroup(username, group, oldPwd)
		if groupAuth == 200:
			adminAuth = authAdmin(username, group)
			
			if adminAuth == 200:
				admins = json.loads(c.execute("SELECT admins FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
				admins.append(addAdmin)
				c.execute("UPDATE Groups SET pwd = (?), admins = (?) WHERE Group_Name = (?) ", (newPwd, json.dumps(admins), group))
				conn.commit()
				print(f"Somebody made some changes to {group}")
				return HttpResponse(status=200)
			
			if adminAuth == 403:
				response = HttpResponse("<h1>Manage Group Error</h1>You're not an admin of this group.")
				response.status_code = 403
				return response
		
		if groupAuth == 401:
			response = HttpResponse("<h1>Manage Group Error</h1>Wrong group password.")
			response.status_code = 401
			return response

		if groupAuth == 403:
			response = HttpResponse("<h1>Manage Group Error</h1>You're banned from this group")
			response.status_code = 403
			return response

		if groupAuth == 404:
			response = HttpResponse("<h1>Manage Group Error</h1>Couldn't find group.")
			response.status_code = 404
			return response
	
	if userAuth == 401:
		response = HttpResponse("<h1>Manage Group Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if userAuth == 404:
		response = HttpResponse("<h1>Manage Group Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def banUser(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	toBan = request.POST.get("toBan", None)
	group = request.POST.get("group", None)
	pwd = request.POST.get("pwd", None)
	authToken = request.POST.get("authToken", None)
	username = request.POST.get("username", None)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		groupAuth = authGroup(username, group, pwd)
		if groupAuth == 200:
			adminAuth = authAdmin(username, group)
			if adminAuth == 200:
				# Remove group from user and ban user in group
				g = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (toBan,)).fetchone()[0]
				banned = json.loads(c.execute("SELECT banned FROM Groups WHERE Group_Name = (?)", (group,)).fetchone()[0])
				banned.append(toBan)
				if not g:
					groups = [group]
				else:
					groups = json.loads(g)
				groups.remove(group)
				
				c.execute("UPDATE Leaderboard SET groups = (?) WHERE Username = (?) ", (json.dumps(groups), toBan))
				conn.commit()
				c.execute("UPDATE Groups SET banned = (?) WHERE Group_Name = (?) ", (json.dumps(banned), group))
				conn.commit()
				c.execute("UPDATE Leaderboard SET Subject = (?) WHERE Username = (?) ", (None, toBan))
				conn.commit()
				print(f"Somebody was banned from {group}")
				return HttpResponse(status=200)
			
			if adminAuth == 403:
				response = HttpResponse("<h1>Ban User Error</h1>You're not an admin of this group.")
				response.status_code = 403
				return response
		
		if groupAuth == 401:
			response = HttpResponse("<h1>Ban User Error</h1>Wrong group password.")
			response.status_code = 401
			return response

		if groupAuth == 403:
			response = HttpResponse("<h1>Ban User Error</h1>You're banned from this group")
			response.status_code = 403
			return response

		if groupAuth == 404:
			response = HttpResponse("<h1>Ban User Error</h1>Couldn't find group.")
			response.status_code = 404
			return response

	if userAuth == 401:
		response = HttpResponse("<h1>Ban User Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if userAuth == 404:
		response = HttpResponse("<h1>Ban User Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

# Other

@csrf_exempt
def reportUser(request):
	# Get data from client
	username = request.POST.get("username", "")
	reportUser = request.POST.get("reportUser", "")
	message = request.POST.get("message", "")
	
	# Send message via reddit
	try:
		data = praw_config
		r = praw.Reddit(username = data["un"], password = data["pw"], client_id = data["cid"], client_secret = data["cs"], user_agent = data["ua"])
		r.redditor('Ttime5').message('Report', f"{username} reported {reportUser}. \n Message: {message}")
		return HttpResponse(status=200)
	except Exception as e:
		response = HttpResponse("<h1>Report User Error</h1>Something went wrong while reporting the user. Please try again.")
		response.status_code = 500
		print(e)
		return response

@csrf_exempt
def setBio(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	statusMsg = request.POST.get("status", None)
	if not strIsValid(statusMsg, 281):
		statusMsg = None
	username = request.POST.get("username", None)
	authToken = request.POST.get("authToken", None)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		# Set bio
		c.execute("UPDATE Leaderboard SET Status = (?) WHERE username = (?) ", (statusMsg, username))
		conn.commit()
		return HttpResponse(status=200)
	
	if userAuth == 401:
		response = HttpResponse("<h1>Set Bio Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if userAuth == 404:
		response = HttpResponse("<h1>Set Bio Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def getBio(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", None)

	# Return users bio
	try:
		bio = c.execute("SELECT Status FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		response = HttpResponse(json.dumps(bio))
		response.status_code = 200
		return response
	except:
		response = HttpResponse("<h1>Get Bio Error</h1>Couldn't find bio.")
		response.status_code = 500
		return response

@csrf_exempt
def getUserinfo(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", None)

	# Check if user exists
	doesExist = True if c.execute("SELECT EXISTS(SELECT 1 FROM Leaderboard WHERE Username= (?))", (username,)).fetchone()[0] == 1 else False
	
	if doesExist:
		# Get user info
		country = c.execute("SELECT Country FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		groups = c.execute("SELECT groups FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		if not groups:
			groups = []
		else:
			groups = json.loads(groups)
		league = c.execute("SELECT league, history FROM League WHERE username = (?)", (username,)).fetchone()
		status = c.execute("SELECT Status FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		response =  HttpResponse(json.dumps([country, groups, league[0], league[1], status]))
		response.status_code = 200
		return response
	else:
		response = HttpResponse("<h1>Get User Info Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def users(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# return list of all usernames
	c.execute("SELECT Username FROM Leaderboard")
	response = HttpResponse(json.dumps([i[0] for i in c.fetchall()]))
	response.status_code = 200
	return response

@csrf_exempt
def season(request):
	response = HttpResponse(json.dumps([[2022,10,26,0,0,0],[2022,11,7,0,0,0], "Season 53"]))
	response.status_code = 200
	return response

# Sync

@csrf_exempt
def sync(request):
	# Connect to database
	conn = sqlite3.connect(database_path)
	c = conn.cursor()

	# Get data from client
	username = request.POST.get("username", "")
	streak = request.POST.get("streak", 0)
	cards = request.POST.get("cards", 0)
	time = request.POST.get("time", 0)
	syncDate = request.POST.get("syncDate", "")
	month = request.POST.get("month", 0)
	country = request.POST.get("country","")
	retention = request.POST.get("retention", 0.0)
	leagueReviews = request.POST.get("leagueReviews", 0)
	leagueTime = request.POST.get("leagueTime", 0)
	leagueRetention = request.POST.get("leagueRetention", 0)
	leagueDaysLearned = request.POST.get("leagueDaysPercent", 0)
	updateLeague = request.POST.get("updateLeague", "True")
	authToken = request.POST.get("authToken", None)
	version = request.POST.get("version", None)
	sortby = request.POST.get("sortby", "Cards")

	# Check input
	if not syncIsValid(streak, cards, time, syncDate, month, country, retention, leagueReviews, leagueTime, leagueRetention, leagueDaysLearned):
		response = HttpResponse("<h1>Sync Error</h1>Invalid input.")
		response.status_code = 400
		return response


	# Calculate xp for leagues

	if float(leagueRetention) >= 85:
		retentionBonus = 1
	if float(leagueRetention) < 85 and float(leagueRetention) >= 70:
		retentionBonus = 0.85
	if float(leagueRetention) < 70 and float(leagueRetention) >= 55:
		retentionBonus = 0.70
	if float(leagueRetention) < 55 and float(leagueRetention) >= 40:
		retentionBonus = 0.55
	if float(leagueRetention) < 40 and float(leagueRetention) >= 25:
		retentionBonus = 0.40
	if float(leagueRetention) < 25 and float(leagueRetention) >= 10:
		retentionBonus = 0.25
	if float(leagueRetention) < 10:
		retentionBonus = 0

	xp = int(float(leagueDaysLearned) * ((6 * float(leagueTime) * 1) + (2 * int(leagueReviews) * float(retentionBonus))))
	
	# Authenticate and commit
	auth = authUser(username, authToken)
	if auth == 200:
		sus = c.execute("SELECT suspended FROM Leaderboard WHERE Username = (?)", (username,)).fetchone()[0]
		if sus:
			response =  HttpResponse(f"<h1>Account suspended</h1>This account was suspended due to the following reason:<br><br>{sus}<br><br>Please write an e-mail to leaderboard_support@protonmail.com or a message me on <a href='https://www.reddit.com/user/Ttime5'>Reddit</a>, if you think that this was a mistake.")
			response.status_code = 403
			return response
		
		c.execute("UPDATE Leaderboard SET Streak = (?), Cards = (?), Time_Spend = (?), Sync_Date = (?), Month = (?), Country = (?), Retention = (?), Token = (?), version = (?) WHERE Username = (?) ", (streak, cards, time, syncDate, month, country, retention, authToken, version, username))
		conn.commit()
		if updateLeague == "True":
			c.execute("UPDATE League SET xp = (?), time_spend = (?), reviews = (?), retention = (?), days_learned = (?) WHERE username = (?) ", (xp, leagueTime, leagueReviews, leagueRetention, leagueDaysLearned, username))
			conn.commit()

		# Get leaderboard data

		data = []
		if sortby == "Cards":
		    c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY Cards DESC")
		if sortby == "Streak":
		    c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY Streak DESC")
		if sortby == "Time_Spend":
		    c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY Time_Spend DESC")
		if sortby == "Month":
		    c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY Month DESC")
		if sortby == "Retention":
		    c.execute("SELECT Username, Streak, Cards, Time_Spend, Sync_Date, Month, Subject, Country, Retention, groups FROM Leaderboard WHERE suspended IS NULL ORDER BY Retention DESC")
		data.append(c.fetchall())

		# Get league data

		c.execute("SELECT username, xp, time_spend, reviews, retention, league, history, days_learned FROM League WHERE suspended IS NULL ORDER BY xp DESC")
		data.append(c.fetchall())

		print(f"Updated account ({version})")
		response = HttpResponse(json.dumps(data))
		response.status_code = 200
		return response
	
	if auth == 401:
		response = HttpResponse("<h1>Sync Error</h1>Couldn't authenticate user. Please go to Leaderboard>Config>Account and login, or use the 'reset password' option if you forgot your password.")
		response.status_code = 401
		return response
	
	if auth == 404:
		response = HttpResponse("<h1>Sync Error</h1>Couldn't find user.")
		response.status_code = 404
		return response
