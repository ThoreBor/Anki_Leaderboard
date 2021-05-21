import time
from datetime import date, timedelta
import datetime
import sqlite3

def Stats(fname, timestamp, nextday, offset):
	###STREAK, REVIEWS PAST 31 DAYS###

	conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/media/'+fname)
	c = conn.cursor()
	new_day = datetime.time(int(nextday),0,0)
	time_now = timestamp.time()
	reviews = c.execute("SELECT id, cid FROM revlog").fetchall()

	###STREAK####

	date_list = []
	Streak = 0
	for i in reviews:
		i = i[0]
		i = datetime.datetime.fromtimestamp(i/1000.0) - timedelta(minutes=offset)
		i = i.timestamp()
		normal = time.strftime('%Y-%m-%d', time.localtime(i))
		i = time.strftime('%Y-%m-%d-%H', time.localtime(i))
		i = i.split("-")
		if int(i[3]) < int(nextday):
			old_date = datetime.date(int(i[0]), int(i[1]), int(i[2]))
			one_day = datetime.timedelta(1)
			new_date = old_date - one_day
			date_list.append(str(new_date))
		else:
			date_list.append(normal)

	if time_now < new_day:
		start_date = timestamp.date() - timedelta(days=1)
		start_date2 = timestamp.date() - timedelta(days=1)
	else:
		start_date = timestamp.date()
		start_date2 = timestamp.date()

	end_date = date(2006, 10, 15)
	delta = timedelta(days=1)
	while start_date >= end_date:
		if start_date.strftime("%Y-%m-%d") in date_list:
			Streak = Streak + 1
		else:
			break
		start_date -= delta

	###REVIEWS PAST 31 DAYS###

	if time_now < new_day:
		start_day = datetime.datetime.combine(timestamp.date(), new_day)
	else:
		start_day = datetime.datetime.combine(timestamp.date() + timedelta(days=1), new_day)

	end_day = datetime.datetime.combine(timestamp.date() - timedelta(days=30), new_day)

	cards_past_30_days = 0

	for i in reviews:
		i = i[0]
		i = datetime.datetime.fromtimestamp(i/1000.0) - timedelta(minutes=offset)
		if i >= end_day and i <= start_day:
			cards_past_30_days = cards_past_30_days + 1

	#REVIEWS TODAY AND RETENTION###

	if time_now < new_day:
			start_day = datetime.datetime.combine(timestamp.date() - timedelta(days=1), new_day)
	else:
		start_day = datetime.datetime.combine(timestamp.date(), new_day)

	total_cards = 0
	flunked_total = 0
	data = c.execute("SELECT * FROM revlog").fetchall()
	for i in data:
		id_time = i[0]
		flunked = i[3]
		type    = i[8]
		id_time = datetime.datetime.fromtimestamp(int(id_time)/1000.0) - timedelta(minutes=offset)
		if id_time > start_day and type != 0:
			total_cards += 1
			###RETENTION###
			if flunked == 1:
				flunked_total += 1
	try:
		retention = round(100 - (100/total_cards*flunked_total), 1)
	except:
		retention = 0

	##TIME SPEND TODAY###

	time_today = 0

	for i in data:
		id_time = i[0]
		id_time = datetime.datetime.fromtimestamp(int(id_time)/1000.0) - timedelta(minutes=offset)
		if id_time > start_day:
			time_today = time_today + int(i[7])
	time_today = round(time_today/60000, 1)

	return(Streak, cards_past_30_days, total_cards, retention, time_today)