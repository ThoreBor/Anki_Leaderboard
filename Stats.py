import time
from datetime import date, timedelta
from aqt import mw
from aqt.utils import showInfo, tooltip
def Stats():
	###STREAK####

	reviews = mw.col.db.list("SELECT id FROM revlog")
	date_list = []
	Streak = 0
	for i in reviews:
		i = time.strftime('%Y-%m-%d', time.gmtime(int(i)/1000.0))
		date_list.append(i)

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

	###TIME SPEND TODAY###
	
	time_today = 0
	for i in studied_today:
		value = mw.col.db.scalar("SELECT time FROM revlog WHERE cid = (?) ORDER BY id DESC",(i))
		time_today = time_today + value
	time_today = round(time_today/60000, 1)

	return(Streak, len(studied_today), time_today)