from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import json
from datetime import datetime, timedelta

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