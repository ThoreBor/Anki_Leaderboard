import time
from datetime import date, timedelta
import datetime

from aqt import mw
from aqt.utils import showInfo

def Stats(season_start, season_end):
	config = mw.addonManager.getConfig(__name__)
	new_day = datetime.time(int(config['newday']),0,0)
	time_now = datetime.datetime.now().time()
	Streak = streak(config, new_day, time_now)

	cards_past_30_days = reviews_past_31_days(new_day, time_now)
	total_cards, retention = reviews_and_retention_today(new_day, time_now)
	time_today = time_spend_today( new_day, time_now)

	league_reviews, league_retention = league_reviews_and_retention(season_start, season_end)
	league_time = league_time_spend(season_start, season_end)

	print(Streak, total_cards, time_today, cards_past_30_days, retention, league_reviews, league_time, league_retention)
	return(Streak, total_cards, time_today, cards_past_30_days, retention, league_reviews, league_time, league_retention)


def get_reviews_and_retention(start_date, end_date):
    start = int(start_date.timestamp()*1000)
    end = int (end_date.timestamp()*1000)
    reviews = mw.col.db.scalar("SELECT COUNT(*) FROM revlog WHERE id >= ? AND id < ?", start, end) 
    flunked_total = mw.col.db.scalar("SELECT COUNT(*) FROM revlog WHERE ease == 1 AND id >= ? AND id < ?", start, end) 
    
    if reviews == 0:
        return 0, 0
    
    retention = round((100/reviews)*(reviews-flunked_total) ,1)
    return reviews, retention

def get_time_spend(start_date, end_date):
	start = int(start_date.timestamp()*1000)
	end = int(end_date.timestamp()*1000)
    
	time = mw.col.db.scalar("SELECT SUM(time) FROM revlog WHERE id >= ? AND id < ?", start, end)
	if not time or time <= 0:
		return 0
	return round(time / 60000, 1)

###LEADERBOARD###

def streak(config, new_day, time_now):
	new_day_shift_in_ms= int(config['newday'])*60*60*1000
	date_list = []
	Streak = 0

	date_list = mw.col.db.list("SELECT DISTINCT strftime('%Y-%m-%d %H',datetime((id-?)/1000, 'unixepoch')) FROM revlog ORDER BY id DESC;", new_day_shift_in_ms)
	
	if time_now < new_day:
		start_date = date.today() - timedelta(days=1)
	else:
		start_date = date.today()

	end_date = date(2006, 10, 15)
	delta = timedelta(days=1)
	while start_date >= end_date:
		# The Anki day does not match the date day. For example the user might have set the next Anki day
		# to be at 2 AM their local time. This has edge cases like the following:
		#
		# Reviews:           X     X
		# Anki day:     [   day 0   ][   day 1   ][   day 2   ]
		# Date day:  [   day 0   ][   day 1   ][   day2   ]
		#
		#
		# Reviews:            X                 X
		# Anki day:     [   day 0   ][   day 1   ][   day 2   ]
		# Date day:  [   day 0   ][   day 1   ][   day2   ]
		#
		# As currently only an hourly offset can be selected, not only the date, but 
		# the hours have to be considered
		base = datetime.datetime.combine(start_date, new_day)
		for hours in range(24):
			if (base+timedelta(hours=hours)).strftime("%Y-%m-%d %H") in date_list:
				break
		else:
			#Nothing in list for 24 hours? Streak ends here
			break

		Streak = Streak + 1
		start_date -= delta

	return Streak

def reviews_past_31_days(new_day, time_now):
	if time_now < new_day:
		end_day = datetime.datetime.combine(date.today(), new_day)
	else:
		end_day = datetime.datetime.combine(date.today()+timedelta(days=1), new_day)

	start_day = end_day - timedelta(days=31)
	reviews, _ =  get_reviews_and_retention(start_day, end_day)
	return reviews

def reviews_and_retention_today(new_day, time_now):
	if time_now < new_day:
		start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
	else:
		start_day = datetime.datetime.combine(date.today(), new_day)
	return get_reviews_and_retention(start_day, start_day+timedelta(days=1))

def time_spend_today(new_day, time_now):	
	if time_now < new_day:
		start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
	else:
		start_day = datetime.datetime.combine(date.today(), new_day)

	return get_time_spend(start_day, start_day + timedelta(days=1))

###LEAGUE###

def league_reviews_and_retention(season_start, season_end):
	return get_reviews_and_retention(season_start, season_end)

def league_time_spend(season_start, season_end):
	return get_time_spend(season_start, season_end)
