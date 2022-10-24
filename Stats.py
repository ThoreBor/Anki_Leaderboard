import time
from datetime import date, timedelta, time
import datetime

from aqt import mw

def Stats(season_start, season_end):
	config = mw.addonManager.getConfig(__name__)
	new_day = datetime.time(int(config['newday']),0,0)
	time_now = datetime.datetime.now().time()
	Streak = streak(config, new_day, time_now)

	cards_past_30_days = reviews_past_31_days(new_day, time_now)
	total_cards, retention = reviews_and_retention_today(new_day, time_now)
	time_today = time_spend_today(new_day, time_now)

	league_reviews, league_retention = league_reviews_and_retention(season_start, season_end)
	league_time = league_time_spend(season_start, season_end)
	league_days_percent = league_days_learned(season_start, season_end, new_day, time_now)

	return(Streak, total_cards, time_today, cards_past_30_days, retention, league_reviews, league_time, league_retention, league_days_percent)


def get_reviews_and_retention(start_date, end_date):
    start = int(start_date.timestamp() * 1000)
    end = int(end_date.timestamp() * 1000)
    reviews = mw.col.db.scalar("SELECT COUNT(*) FROM revlog WHERE id >= ? AND id < ? AND ease > 0", start, end)
    flunked_total = mw.col.db.scalar("SELECT COUNT(*) FROM revlog WHERE ease == 1 AND id >= ? AND id < ?", start, end) 
    
    if reviews == 0:
        return 0, 0
    
    retention = round((100 / reviews) * (reviews - flunked_total), 1)
    return reviews, retention

def get_time_spend(start_date, end_date):
	start = int(start_date.timestamp() * 1000)
	end = int(end_date.timestamp() * 1000)
    
	time = mw.col.db.scalar("SELECT SUM(time) FROM revlog WHERE id >= ? AND id < ?", start, end)
	if not time or time <= 0:
		return 0
	return round(time / 60000, 1)

###LEADERBOARD###

def streak(config, new_day, time_now):
	new_day_shift_in_ms= int(config['newday']) * 60 * 60 * 1000
	date_list = []
	Streak = 0

	date_list = mw.col.db.list("SELECT DISTINCT strftime('%Y-%m-%d', datetime((id - ?) / 1000, 'unixepoch', 'localtime')) FROM revlog WHERE ease > 0 ORDER BY id DESC;", new_day_shift_in_ms)
	
	if time_now < new_day:
		start_date = date.today() - timedelta(days=1)
	else:
		start_date = date.today()

	end_date = date(2006, 10, 15)
	delta = timedelta(days=1)
	while start_date >= end_date:
		if not start_date.strftime("%Y-%m-%d") in date_list:
			break	
		Streak = Streak + 1
		start_date -= delta
	return Streak

def reviews_past_31_days(new_day, time_now):
	if time_now < new_day:
		end_day = datetime.datetime.combine(date.today(), new_day)
	else:
		end_day = datetime.datetime.combine(date.today() + timedelta(days=1), new_day)

	start_day = end_day - timedelta(days=31)
	reviews, _ =  get_reviews_and_retention(start_day, end_day)
	return reviews

def reviews_and_retention_today(new_day, time_now):
	if time_now < new_day:
		start_day = datetime.datetime.combine(date.today() - timedelta(days=1), new_day)
	else:
		start_day = datetime.datetime.combine(date.today(), new_day)
	return get_reviews_and_retention(start_day, start_day + timedelta(days=1))

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

def league_days_learned(season_start, season_end, new_day, time_now):
	date_list = [datetime.datetime.combine(season_start, new_day) + timedelta(days=x) for x in range((season_end - season_start).days + 1)]
	days_learned = 0
	days_over = 0
	for i in date_list:
		time = get_time_spend(i, i + timedelta(days=1))
		if time >= 5:
			days_learned += 1
		if i.date() == date.today() and time_now < new_day:
			continue
		if i.date() <= date.today():
			days_over += 1

	return round((100 / days_over) * days_learned, 1)
