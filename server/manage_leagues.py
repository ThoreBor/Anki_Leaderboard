import sqlite3

alpha_ranking = []
beta_ranking = []
gamma_ranking = []
delta_ranking = []

conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
#conn = sqlite3.connect('Leaderboard.db')
c = conn.cursor()

c.execute("SELECT username, league, xp FROM League ORDER BY xp DESC")

for row in c.fetchall():
	user = row[0]
	league_name = row[1]
	xp = row[2]

	if league_name == "Alpha" and xp != 0:
		alpha_ranking.append(user)
	if league_name == "Beta" and xp != 0:
		beta_ranking.append(user)
	if league_name == "Gamma" and xp != 0:
		gamma_ranking.append(user)
	if league_name == "Delta" and xp != 0:
		delta_ranking.append(user)

print(f"Alpha: {len(alpha_ranking)} \nBeta: {len(beta_ranking)} \nGamma: {len(gamma_ranking)} \nDelta: {len(delta_ranking)}")
print("")


for i in alpha_ranking[-int((len(alpha_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))

for i in beta_ranking[:int((len(beta_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Alpha", i))
for i in beta_ranking[-int((len(beta_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))

for i in gamma_ranking[:int((len(gamma_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))
for i in gamma_ranking[-int((len(gamma_ranking) / 100) * 20):]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Delta", i))

for i in delta_ranking[:int((len(delta_ranking) / 100) * 20)]:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))

c.execute("UPDATE League SET xp = 0, time_spend = 0, reviews = 0, retention = 0")

conn.commit()