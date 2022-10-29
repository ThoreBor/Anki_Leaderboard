from datetime import datetime
import re

# To make sure nothing unwanted gets in the database

def syncIsValid(streak, cards, time, syncDate, month, country, retention, leagueReviews, leagueTime, leagueRetention, leagueDaysLearned):
	if not intIsValid(streak, 10000):
		return False
	if not intIsValid(cards, 10000):
		return False
	if not floatIsValid(time, 1000):
		return False
	if not dateIsValid(syncDate):
		return False
	if not intIsValid(month, 300000):
		return False
	if not strIsValid(country, 50):
		return False
	if not floatIsValid(retention, 101):
		return False
	if not intIsValid(leagueReviews, 300000):
		return False
	if not floatIsValid(leagueTime, 30000):
		return False
	if not floatIsValid(leagueRetention, 101):
		return False
	if not floatIsValid(leagueDaysLearned, 101):
		return False
	return True

def usernameIsValid(username):
	if username != "" and len(username) < 16 and "🥇" not in username and "🥈" not in username and "🥉" not in username and "|" not in username:
		return True
	else:
		return False

def emailIsValid(email):
	if "@" in email and "." in email and len(email) < 250:
		return True
	else:
		return False

def dateIsValid(date):
	try:
		date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
		return True
	except:
		return False

def intIsValid(i, maximum):
	try:
		int(i)
		if int(i) < maximum:
			return True
		else:
			return False
	except Exception as e:
		return False

def floatIsValid(i, maximum):
	try:
		float(i)
		if float(i) < maximum:
			return True
		else:
			return False
	except:
		return False

def strIsValid(s, maximum):
	try:
		str(s)
		if len(str(s)) < maximum:
			return True
		else:
			return False
	except:
		return False