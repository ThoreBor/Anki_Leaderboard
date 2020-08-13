import sqlite3

alpha_ranking = []
alpha_bottom = []

beta_ranking = []
beta_top = []
beta_bottom = []

gamma_ranking = []
gamma_top = []
gamma_bottom = []

delta_ranking = []
delta_top = []

#conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
conn = sqlite3.connect('Leaderboard.db')
c = conn.cursor()
c.execute("SELECT username, league FROM League ORDER BY xp DESC")

for row in c.fetchall():
	user = row[0]
	league_name = row[1]

	if league_name == "Alpha":
		alpha_ranking.append(user)
	if league_name == "Beta":
		beta_ranking.append(user)
	if league_name == "Gamma":
		gamma_ranking.append(user)
	if league_name == "Delta":
		delta_ranking.append(user)

print(f"Alpha: {len(alpha_ranking)} \nBeta: {len(beta_ranking)} \nGamma: {len(gamma_ranking)} \nDelta: {len(delta_ranking)}")

alpha_bottom = alpha_ranking[-int((len(alpha_ranking) / 100) * 20):]
for i in alpha_bottom:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))
conn.commit()

beta_top = beta_ranking[:int((len(beta_ranking) / 100) * 20)]
for i in beta_top:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Alpha", i))
conn.commit()
beta_bottom = beta_ranking[-int((len(beta_ranking) / 100) * 20):]
for i in beta_bottom:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))
conn.commit()

gamma_top = gamma_ranking[:int((len(gamma_ranking) / 100) * 20)]
for i in gamma_top:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Beta", i))
conn.commit()
gamma_bottom = gamma_ranking[-int((len(gamma_ranking) / 100) * 20):]
for i in gamma_bottom:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Delta", i))
conn.commit()

delta_top = delta_ranking[:int((len(delta_ranking) / 100) * 20)]
for i in delta_top:
	c.execute("UPDATE League SET league = (?) WHERE username = (?) ", ("Gamma", i))
conn.commit()

c.execute("UPDATE League SET xp = 0, time_spend = 0, reviews = 0, retention = 0")
conn.commit()