from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import json
import praw
from argon2 import PasswordHasher
import secrets

from .config import praw_config
from .checkInput import *
from .models import Groups, User_Profile, User_Leaderboard, User_League


# Authentication

def authUser(username, token):
	# Authenticate user
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		if token == profile.auth_token:
			return 200
		else:
			print("authUser 401")
			return 401
	else:
		return 404

def authGroup(username, group, pwd):
	if Groups.objects.filter(group_name=group).exists():
		# Authenticate group password, check if user is banned
		group = Groups.objects.get(group_name=group)
		if group.pwd_hash == pwd:
			if username in group.banned:
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
	# Check if user is admin
	group = Groups.objects.get(group_name=group)
	if username in group.admins:
		return 200
	else:
		print("authAdmin 403")
		return 403

# Manage Account

@csrf_exempt
def signUp(request):
	# Get data from client
	email = request.POST.get("email", "")
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")
	syncDate = request.POST.get("syncDate", "")
	version = request.POST.get("version", "")
	authToken = secrets.token_hex(nbytes=64)

	# Check if username is valid
	if User.objects.filter(username=username).exists():
		response = HttpResponse("<h1>Sign-up Error</h1>This username is already taken. Please choose another one.")
		response.status_code = 400
		return response
	if not usernameIsValid(username):
		response = HttpResponse("<h1>Sign-up Error</h1>This username is too long. The username must have less than 15 characters and can't contain any of these characters: 🥇🥈🥉|")
		response.status_code = 400
		return response

	# Check email and date
	if not emailIsValid(email) or not dateIsValid(syncDate):
		response = HttpResponse("<h1>Sign-up Error</h1>Invalid input.")
		response.status_code = 400
		return response

	# Create User
	user = User.objects.create_user(username=username, password=pwd, email=email)
	user.save()

	user_profile = User_Profile.objects.create(
		user=user,
		auth_token=authToken,
		old_hash=None,
		country=None,
		groups=None,
		suspended=None,
		bio=None,
		version=version,
		sync_date=syncDate,
		league="Delta",
		history=None
	)

	user_leaderboard = User_Leaderboard.objects.create(
		user=user,
		streak=0,
		cards_today=0,
		cards_month=0,
		time_today=0,
		retention=0,
	)

	user_league = User_League.objects.create(
		user=user,
		xp=0,
		time_spent=0,
		cards=0,
		retention=0,
		days_studied=0,
	)

	response = HttpResponse(json.dumps(authToken))
	response.status_code = 201
	print("New sign-up")
	return response

@csrf_exempt
def logIn(request):
	# Get data from client
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")


	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)

		# Authenticate user
		# Check if user already has a usable password (after migrating the db it is unusable)
		if user.has_usable_password():
			user = authenticate(username=username, password=pwd)
			if not user:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response
		else:
			try:
				ph = PasswordHasher()
				ph.verify(profile.old_hash, pwd)
				user.set_password(pwd)
				user.save()
			except:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response

		# Create token for authentication
		authToken = secrets.token_hex(nbytes=64)

		# Update token in database and return token
		profile.auth_token = authToken
		profile.save()
		response = HttpResponse(json.dumps(authToken))
		response.status_code = 200
		print("New login")
		return response

	else:
		response = HttpResponse("<h1>Log-in Error</h1>This user doesn't exist.")
		response.status_code = 404
		return response

@csrf_exempt
def deleteAccount(request):
	# Get data from client
	username = request.POST.get("username", "")
	pwd = request.POST.get("pwd", "")

	# Authenticate user
	# Check if user already has a usable password (after migrating the db it is unusable)
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		if user.has_usable_password():
			user = authenticate(username=username, password=pwd)
			if not user:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response
		else:
			try:
				ph = PasswordHasher()
				ph.verify(profile.old_hash, pwd)
			except:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response

		# Update group member number of the groups the user was in
		groupList = profile.groups
		if not groupList:
			groups = []
		else:
			groups = groupList
		for i in groups:
			if Groups.objects.filter(group_name=i).exists():
				group = Groups.objects.get(group_name=i)
				group.members -= 1
				group.save()

		# Delete user
		user = User.objects.get(username=username)
		user.delete()
		print("Deleted account")
		return HttpResponse(status=204)

	else:
		response = HttpResponse("<h1>Delete Error</h1>This user doesn't exist.")
		response.status_code = 404
		return response

@csrf_exempt
def changeUsername(request):
	# Get data from client
	username = request.POST.get("username", None)
	newUsername = request.POST.get("newUsername", None)
	pwd = request.POST.get("pwd", None)

	authToken = secrets.token_hex(nbytes=64)

	# Check if new username is valid
	if not usernameIsValid(newUsername):
		response = HttpResponse("<h1>Change Username Error</h1>This username is too long. The username must have less than 15 characters.")
		response.status_code = 400
		return response

	if User.objects.filter(username=newUsername).exists():
		response = HttpResponse("<h1>Change Username Error</h1>This username is already taken. Please choose another one.")
		response.status_code = 401
		return response
	else:
		# Authenticate user
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		if user.has_usable_password():
			user = authenticate(username=username, password=pwd)
			if not user:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response
		else:
			try:
				ph = PasswordHasher()
				ph.verify(profile.old_hash, pwd)
				user.set_password(pwd)
				user.save()
			except:
				response = HttpResponse("<h1>Log-in Error</h1>Password and username doesn't match.")
				response.status_code = 401
				return response

		# Change username and update token and hash, return token
		user.username = newUsername
		user.save()
		response = HttpResponse(json.dumps(authToken))
		response.status_code = 200
		print("Changed username")
		return response

#Manage groups

@csrf_exempt
def groups(request):
	# Return all groups
	groups = Groups.objects.values_list("group_name", flat=True).order_by(Lower("group_name"))
	response = HttpResponse(json.dumps(list(groups)))
	response.status_code = 200
	return response

@csrf_exempt
def joinGroup(request):
	# Get data from client
	username = request.POST.get("username", None)
	group_name = request.POST.get("group", None)
	pwd = request.POST.get("pwd", None)
	authToken = request.POST.get("authToken", None)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		groupAuth = authGroup(username, group_name, pwd)
		if groupAuth == 200:
			# Get groups and add new group
			user = User.objects.get(username=username)
			profile = User_Profile.objects.get(user=user)
			userGroups = profile.groups

			userGroups.append(group_name)
			# Update members
			group = Groups.objects.get(group_name=group_name)
			group.members += 1
			group.save()
			profile.save()

			print(f"Somebody joined {group_name}")
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
	group_name = request.POST.get("groupName", None).strip()
	username = request.POST.get("username", None)
	pwd = request.POST.get("pwd", None)

	if Groups.objects.filter(group_name=group_name).exists() or not strIsValid(group_name, 50):
		response = HttpResponse("<h1>Create Group Error</h1>This group name is already taken or too long.")
		response.status_code = 400
		return response
	else:
		# Create group
		group = Groups.objects.create(
			group_name=group_name,
			pwd_hash=pwd,
			admins=[username],
			banned=[],
			members=1
		)
		group.save()
		print(f"New group: {group_name}")
		return HttpResponse(status=200)

@csrf_exempt
def leaveGroup(request):
	# Get data from client
	group_name = request.POST.get("group", None)
	authToken = request.POST.get("authToken", None)
	username = request.POST.get("username", None)

	# Check if group exists
	if not Groups.objects.filter(group_name=group_name).exists():
		# So that users can delete groups in the add-on even if it doesn't exist anymore
		return HttpResponse(status=200)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		# Remove group
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		profile.groups.remove(group_name)
		profile.save()
		# Remove member
		group = Groups.objects.get(group_name=group_name)
		group.members -= 1
		group.save()
		print(f"Somebody left {group_name}")
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
				group_to_change = Groups.objects.get(group_name=group)
				group_to_change.admins.append(addAdmin)
				group_to_change.pwd_hash = newPwd
				group_to_change.save()
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
				user = User.objects.get(username=toBan)
				profile = User_Profile.objects.get(user=user)
				profile.groups.remove(group)
				profile.save()
				group_to_change = Groups.objects.get(group_name=group)
				group_to_change.banned.append(toBan)
				group_to_change.members -= 1
				group_to_change.save()
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

# Sync

@csrf_exempt
def sync(request):
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
	sortby = request.POST.get("sortby", "cards_today")

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
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		leaderboard = User_Leaderboard.objects.get(user=user)
		league = User_League.objects.get(user=user)

		if profile.suspended:
			response =  HttpResponse(f"<h1>Account suspended</h1>This account was suspended due to the following reason:<br><br>{sus}<br><br>Please write an e-mail to leaderboard_support@protonmail.com or a message me on <a href='https://www.reddit.com/user/Ttime5'>Reddit</a>, if you think that this was a mistake.")
			response.status_code = 403
			return response

		leaderboard.streak = streak
		leaderboard.cards_today = cards
		leaderboard.cards_month = month
		leaderboard.time_today = time
		leaderboard.retention = retention
		leaderboard.save()
		profile.country = country
		profile.version = version
		profile.sync_date = syncDate
		profile.save()


		if updateLeague == "True":
			league.xp = xp
			league.time_spent = leagueTime
			league.cards = leagueReviews
			league.retention = leagueRetention
			league.days_studied = leagueDaysLearned
			league.save()
			(xp, leagueTime, leagueReviews, leagueRetention, leagueDaysLearned, username)


		# Get leaderboard data

		data = []
		user_data = User.objects.values_list(
			"user_profile__user__username",
			"user_leaderboard__streak",
			"user_leaderboard__cards_today",
			"user_leaderboard__time_today",
			"user_profile__sync_date",
			"user_leaderboard__cards_month",
			"user_profile__country",
			"user_leaderboard__retention",
			"user_profile__groups"
		).order_by("-user_leaderboard__{}".format(sortby))
		data.append(list(user_data))

		# Get league data
		user_data = User.objects.values_list(
			"user_profile__user__username",
			"user_league__xp",
			"user_league__time_spent",
			"user_league__cards",
			"user_league__retention",
			"user_profile__league",
			"user_profile__history",
			"user_league__days_studied",
		).order_by("-user_league__xp")

		data.append(list(user_data))
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
	# Get data from client
	statusMsg = request.POST.get("status", None)
	if not strIsValid(statusMsg, 281):
		statusMsg = None
	username = request.POST.get("username", None)
	authToken = request.POST.get("authToken", None)

	userAuth = authUser(username, authToken)
	if userAuth == 200:
		# Set bio
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		profile.bio = statusMsg
		profile.save()
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
	# Get data from client
	username = request.POST.get("username", None)

	# Return users bio
	if User.objects.filter(username=username).exists():
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		response = HttpResponse(json.dumps(profile.bio))
		response.status_code = 200
		return response
	else:
		response = HttpResponse("<h1>Get Bio Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def getUserinfo(request):
	# Get data from client
	username = request.POST.get("username", None)

	if User.objects.filter(username=username).exists():
		# Get user info
		user = User.objects.get(username=username)
		profile = User_Profile.objects.get(user=user)
		response =  HttpResponse(json.dumps([profile.country, profile.groups, profile.league, profile.history, profile.bio]))
		response.status_code = 200
		return response
	else:
		response = HttpResponse("<h1>Get User Info Error</h1>Couldn't find user.")
		response.status_code = 404
		return response

@csrf_exempt
def users(request):
	# return list of all usernames
	usernames = User.objects.values_list("username", flat=True)
	response = HttpResponse(json.dumps(list(usernames)))
	response.status_code = 200
	return response

@csrf_exempt
def season(request):
	response = HttpResponse(json.dumps([[2023,5,15,0,0,0],[2023,5,29,0,0,0], "Season 67"]))
	response.status_code = 200
	return response
