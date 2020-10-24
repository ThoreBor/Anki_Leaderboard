import requests
import sqlite3

conn = sqlite3.connect('/home/ankileaderboard/anki_leaderboard_pythonanywhere/Leaderboard.db')
#conn = sqlite3.connect('Leaderboard.db')
c = conn.cursor()

url_base = "https://ankileaderboard.pythonanywhere.com/"
#url = "http://127.0.0.1:8000/"

def sync():
	url = url_base + "sync/"
	data = {'Username': "AdminTest", "Streak": 100, "Cards": 101, "Time": 102, "Sync_Date": "2020-01-01 00:00:00.00000",
	"Month": 3000, "Country": "Germany", "Retention": 99,
	"league_reviews": 103, "league_time": 104, "league_retention": 98,
	"Token_v3": "TestToken", "Version": "v1.6.1"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("Sync server response: Done!")
		data = c.execute("SELECT Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention, Token FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "AdminTest"
		assert data[1] == 100
		assert data[2] == 101
		assert data[3] == 102
		assert data[4] == "2020-01-01 00:00:00.00000"
		assert data[5] == 3000
		assert data[6] == None
		assert data[7] == "Germany"
		assert data[8] == 99
		assert data[9] == "TestToken"

		data = c.execute("SELECT username, xp, time_spend, reviews, retention FROM League WHERE username = 'AdminTest'").fetchone()
		assert data[0] == "AdminTest"
		assert data[1] == int((4 * float(104) + 2 * int(103)) * float(98))
		assert data[2] == 104
		assert data[3] == 103
		assert data[4] == 98

	else:
		print(x.text)

def dont_sync_league():
	url = url_base + "sync/"
	data = {'Username': "AdminTest", "Streak": 101, "Cards": 102, "Time": 103, "Sync_Date": "2020-01-01 00:00:00.00000",
	"Month": 3001, "Country": "Germany", "Retention": 100,
	"league_reviews": 104, "league_time": 105, "league_retention": 99, "Update_League": False,
	"Token_v3": "TestToken", "Version": "v1.6.1"}

	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("Don't sync league server response: Done!")
		data = c.execute("SELECT Username, Streak, Cards , Time_Spend, Sync_Date, Month, Subject, Country, Retention, Token FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "AdminTest"
		assert data[1] == 101
		assert data[2] == 102
		assert data[3] == 103
		assert data[4] == "2020-01-01 00:00:00.00000"
		assert data[5] == 3001
		assert data[6] == None
		assert data[7] == "Germany"
		assert data[8] == 100
		assert data[9] == "TestToken"

		data = c.execute("SELECT username, xp, time_spend, reviews, retention FROM League WHERE username = 'AdminTest'").fetchone()
		assert data[0] == "AdminTest"
		assert data[1] == int((4 * float(104) + 2 * int(103)) * float(98))
		assert data[2] == 104
		assert data[3] == 103
		assert data[4] == 98

	else:
		print(x.text)

def joinGroup():
	url = url_base + "joinGroup/"
	data = {"username": "AdminTest", "group": "Languages", "pwd": None, "token": "TestToken"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("joinGroup server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "Languages"
	else:
		print(x.text)

def createGroup():
	url = url_base + "create_group/"
	data = {'Group_Name': "TestGroup", "User": "AdminTest", "Mail": "test@mail.com", "Pwd": "1234"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("createGroup server response: Done!")
		c.execute("UPDATE Groups SET verified = 1 WHERE Group_Name = 'TestGroup'")
		conn.commit()
		data = c.execute("SELECT Group_Name, verified, pwd, admins, banned FROM Groups WHERE Group_Name = 'TestGroup'").fetchone()
		assert data[0] == "TestGroup"
		assert data[1] == 1
		assert data[2] == "1234"
		assert data[3] == "AdminTest,"
		assert data[4] == None
	else:
		print(x.text)

def joinGroup_pwd():
	url = url_base + "joinGroup/"
	data = {"username": "AdminTest", "group": "TestGroup", "pwd": "1234", "token": "TestToken"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("joinGroup server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "TestGroup"
	else:
		print(x.text)

def joinGroup_pwd_wrong():
	url = url_base + "joinGroup/"
	data = {"username": "AdminTest", "group": "TestGroup", "pwd": "12342", "token": "TestToken"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("joinGroup server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "TestGroup"
	else:
		print(x.text)

def joinGroup_token_wrong():
	url = url_base + "joinGroup/"
	data = {"username": "AdminTest", "group": "TestGroup", "pwd": "1234", "token": "TestToken!"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("joinGroup server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == "TestGroup"
	else:
		print(x.text)

def banUser():
	url = url_base + "banUser/"
	data = {"toBan": "AdminTest", "group": "TestGroup", "pwd": "1234", "token": "TestToken", "user": "AdminTest"}

	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("banUser server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == None
	else:
		print(x.text)

def banUser_notAdmin():
	url = url_base + "banUser/"
	data = {"toBan": "AdminTest", "group": "TestGroup", "pwd": "1234", "token": "TestToken", "user": "notAdmin"}

	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("banUser server response: Done!")
		data = c.execute("SELECT Subject FROM Leaderboard WHERE Username = 'AdminTest'").fetchone()
		assert data[0] == None
	else:
		print(x.text)

def manageGroup():
	url = url_base + "manageGroup/"
	data = {'group': "TestGroup", "user": "AdminTest", "token": "TestToken", "oldPwd": "1234", "newPwd": "abcd", "addAdmin": "NewAdmin"}

	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("manageGroup server response: Done!")
		data = c.execute("SELECT Group_Name, verified, pwd, admins, banned FROM Groups WHERE Group_Name = 'TestGroup'").fetchone()

		assert data[0] == "TestGroup"
		assert data[1] == 1
		assert data[2] == "abcd"
		assert data[3] == "AdminTest, NewAdmin,"
		assert data[4] == "None, AdminTest"
	else:
		print(x.text)

def manageGroup_withoutAdmin():
	url = url_base + "manageGroup/"
	data = {'group': "TestGroup", "user": "AdminTest", "token": "TestToken", "oldPwd": "abcd", "newPwd": "abcd", "addAdmin": ""}

	x = requests.post(url, data = data, timeout=20)
	if x.text == "Done!":
		print("manageGroup server response: Done!")
		data = c.execute("SELECT Group_Name, verified, pwd, admins, banned FROM Groups WHERE Group_Name = 'TestGroup'").fetchone()

		assert data[0] == "TestGroup"
		assert data[1] == 1
		assert data[2] == "abcd"
		assert data[3] == "AdminTest, NewAdmin,"
		assert data[4] == "None, AdminTest"
	else:
		print(x.text)

def delete():
	url = url_base + "delete/"
	data = {'Username': 'AdminTest', 'Token_v3': "TestToken"}
	x = requests.post(url, data = data, timeout=20)
	if x.text == "Deleted":
		print("Delete sever response: Deleted!")
	else:
		print("Delete error")

def deleteGroup():
	c.execute("DELETE FROM Groups WHERE Group_Name = 'TestGroup'")
	print("Deleted Group")
	conn.commit()

sync()
sync()
dont_sync_league()
sync()
joinGroup()
createGroup()
joinGroup_pwd()
joinGroup_pwd_wrong()
joinGroup_token_wrong()
banUser()
joinGroup_pwd()
banUser_notAdmin()
manageGroup()
manageGroup_withoutAdmin()

print("")

deleteGroup()
delete()