import time
from datetime import date, timedelta
import datetime
from aqt import mw
from os.path import dirname, join, realpath
from aqt.utils import showInfo, tooltip
def Stats():
	###STREAK####

	reviews = mw.col.db.list("SELECT id FROM revlog")
	date_list = []
	hour_list =["00","01","02","03"]
	Streak = 0
	for i in reviews:
		normal = time.strftime('%Y-%m-%d', time.gmtime(int(i)/1000.0))
		i = time.strftime('%Y-%m-%d-%H', time.gmtime(int(i)/1000.0))
		i = i.split("-")
		if str(i[3]) in hour_list:
			old_date = datetime.date(int(i[0]), int(i[1]), int(i[2]))
			one_day = datetime.timedelta(1)
			new_date = old_date - one_day
			date_list.append(str(new_date))
		else:
			date_list.append(normal)
	
	start_date = date.today()
	end_date = date(2000, 1, 1)
	delta = timedelta(days=1)
	while start_date >= end_date:
	    if start_date.strftime("%Y-%m-%d") in date_list:
	    	Streak = Streak + 1
	    else:
	    	break
	    start_date -= delta

	###REVIEWS TODAY####

	studied_today = mw.col.findCards('rated:1')
	total_cards = 0
	for i in studied_today:
		value = mw.col.db.execute("SELECT * FROM revlog WHERE cid = (?) ORDER BY id DESC",(i)).fetchall()
		for i in value:
			id_time = i[0]
			id_time = time.strftime('%Y-%m-%d', time.gmtime(int(id_time)/1000.0))
			if str(id_time) == str(date.today()):
				total_cards += 1

	###TIME SPEND TODAY###
	
	time_today = 0
	for i in studied_today:
		value = mw.col.db.execute("SELECT * FROM revlog WHERE cid = (?) ORDER BY id DESC",(i)).fetchall()
		for i in value:
			id_time = i[0]
			id_time = time.strftime('%Y-%m-%d', time.gmtime(int(id_time)/1000.0))
			# showInfo(str(id_time))
			# showInfo(str(date.today()))
			if str(id_time) == str(date.today()):
				time_today = time_today + int(i[7])
	time_today = round(time_today/60000, 1)

	return(Streak, total_cards, time_today)