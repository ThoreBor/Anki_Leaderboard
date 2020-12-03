import sqlite3
import json

alpha_ranking = []
beta_ranking = []
gamma_ranking = []
delta_ranking = []

alpha_zero = []
beta_zero = []
gamma_zero = []

SEASON = int(input("Past season:"))

conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
#conn = sqlite3.connect('Leaderboard.db')
c = conn.cursor()

def rewrite_history(username, league, counter):
	data = c.execute("SELECT xp, history FROM League WHERE username = (?)", (username,)).fetchone()
	xp = data[0]
	try:
		history = json.loads(data[1])
	except:
		history = {"gold": 0, "silver": 0, "bronze": 0, "results": { "leagues": [], "seasons": [], "xp": [], "rank": []}}

	if counter == 1:
		history["gold"] += 1
	if counter == 2:
		history["silver"] += 1
	if counter == 3:
		history["bronze"] += 1

	results = history["results"]
	results["leagues"].append(league)
	results["seasons"].append(SEASON)
	results["xp"].append(xp)
	results["rank"].append(counter)

	new_history = {"gold": history["gold"], "silver": history["silver"], "bronze": history["bronze"], "results":{"leagues": results["leagues"], "seasons": results["seasons"], "xp": results["xp"], "rank": results["rank"]}}
	c.execute("""UPDATE League SET history = (?) WHERE username = (?) """, (json.dumps(new_history), username))


c.execute("SELECT username, league, xp FROM League ORDER BY xp DESC")

for row in c.fetchall():
	user = row[0]
	league_name = row[1]
	xp = row[2]


	if league_name == "Alpha":
		if xp != 0:
			alpha_ranking.append(user)
		else:
			alpha_zero.append(user)
	if league_name == "Beta":
		if xp != 0:
			beta_ranking.append(user)
		else:
			beta_zero.append(user)
	if league_name == "Gamma":
		if xp != 0:
			gamma_ranking.append(user)
		else:
			gamma_zero.append(user)
	if league_name == "Delta":
		if xp != 0:
			delta_ranking.append(user)

counter = 1
for i in alpha_ranking:
	rewrite_history(i, "Alpha", counter)
	counter += 1

counter = 1
for i in beta_ranking:
	rewrite_history(i, "Beta", counter)
	counter += 1

counter = 1
for i in gamma_ranking:
	rewrite_history(i, "Gamma", counter)
	counter += 1

counter = 1
for i in delta_ranking:
	rewrite_history(i, "Delta", counter)
	counter += 1


for i in alpha_ranking[-int((len(alpha_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))
for i in alpha_zero:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))

for i in beta_ranking[:int((len(beta_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Alpha", i))
for i in beta_ranking[-int((len(beta_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))
for i in beta_zero:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))

for i in gamma_ranking[:int((len(gamma_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))
for i in gamma_ranking[-int((len(gamma_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Delta", i))
for i in gamma_zero:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Delta", i))

for i in delta_ranking[:int((len(delta_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))

c.execute("UPDATE League SET xp = 0, time_spend = 0, reviews = 0, retention = 0")

alpha = c.execute("SELECT * FROM League WHERE league = 'Alpha' ").fetchall()
beta = c.execute("SELECT * FROM League WHERE league = 'Beta' ").fetchall()
gamma = c.execute("SELECT * FROM League WHERE league = 'Gamma' ").fetchall()
delta = c.execute("SELECT * FROM League WHERE league = 'Delta' ").fetchall()

print(f"Alpha: {len(alpha)} \nBeta: {len(beta)} \nGamma: {len(gamma)} \nDelta: {len(delta)}")
print("")

conn.commit()