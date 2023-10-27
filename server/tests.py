from django.test import TestCase
from django.contrib.auth.models import User
import json
from .models import Groups, User_Profile, User_Leaderboard, User_League

base_url = "http://127.0.0.1:8000"
class API_V3_TestCase(TestCase):

	def setUp(self):
		# Sample user after db migration
		user = User.objects.create_user(username="Migrated_User",email="migrate@gmail.com")
		user.set_unusable_password()
		user.save()

		user_profile = User_Profile.objects.create(
			user=user,
			auth_token="4a6f89bb34d90c45eb...",
			old_hash="$argon2id$v=19$m=65536,t=3,p=4$fqNsbNo5pWlurs2+Y/2lTQ$CQOUWIgwYVxHiuk2jKpFRiz1nwqY622TzpBWDJ9zKUI",
			country="Germany",
			groups=["Test Group", "not_a_group"],
			suspended=None,
			bio="Test bio",
			version="v4.0.0",
			sync_date="2023-06-01 11:22:45.827167",
			league="Gamma",
			history={}
		)
		
		user_leaderboard = User_Leaderboard.objects.create(
			user=user,
			streak=1900,
			cards_today=78,
			cards_month=3000,
			time_today=30.5,
			retention=87.6,
		)
		
		user_league = User_League.objects.create(
			user=user,
			xp=103456,
			time_spent=200,
			cards=1500,
			retention=98,
			days_studied=100,
		)
		
		user_profile.save()
		user_leaderboard.save()
		user_league.save()

		# New user, or user that logged in after db migration
		user = User.objects.create_user(username="New_User",email="foxahap315@ratedane.com", password="secretweaktestpassword")
		user.save()

		user_profile = User_Profile.objects.create(
			user=user,
			auth_token="4a6f89bb34d90c45eb...",
			old_hash=None,
			country="Germany",
			groups=["Test Group"],
			suspended=None,
			bio="Test bio",
			version="v4.0.0",
			sync_date="2023-06-01 11:22:45.827167",
			league="Gamma",
			history={}
		)

		user_profile.save()

		# Groups
		group = Groups.objects.create(
			group_name="Test Group",
			pwd_hash="grouphash",
			admins=["New_User"],
			banned=[],
			members=4
		)
		group.save()

		group = Groups.objects.create(
			group_name="Test Group2",
			pwd_hash="grouphash",
			admins=[],
			banned=[],
			members=4
		)
		group.save()

	def test_signUp_201(self):
		data = {
			"email": "test@gmail.com",
			"username": "TESTUSER",
			"pwd": "secretweaktestpassword",
			"syncDate": "2021-05-22 11:22:45.827167",
			"version": "v4.0.0"
		}

		response = self.client.post(f"{base_url}/api/v3/signUp/", data)
		self.assertEqual(response.status_code, 201)
		user = User.objects.get(username="TESTUSER")
		self.assertEqual(user.email, "test@gmail.com")
		profile = User_Profile.objects.get(user=user)
		self.assertEqual(profile.sync_date, "2021-05-22 11:22:45.827167")
		self.assertEqual(profile.version, "v4.0.0")
		leaderboard = User_Leaderboard.objects.get(user=user)
		self.assertEqual(leaderboard.streak, 0)
		league = User_League.objects.get(user=user)
		self.assertEqual(league.xp, 0)

	def test_signUp_400_email(self):
		data = {
			"email": "test.gmail.com",
			"username": "TESTUSER",
			"pwd": "secretweaktestpassword",
			"syncDate": "2021-05-22 11:22:45.827167",
			"version": "v4.0.0"
		}

		response = self.client.post(f"{base_url}/api/v3/signUp/", data)
		self.assertEqual(response.status_code, 400)

	def test_signUp_400_date(self):
		data = {
			"email": "test.gmail.com",
			"username": "TESTUSER",
			"pwd": "secretweaktestpassword",
			"syncDate": "2021-13-22 11:22:45.827167",
			"version": "v4.0.0"
		}

		response = self.client.post(f"{base_url}/api/v3/signUp/", data)
		self.assertEqual(response.status_code, 400)

	def test_signUp_400_name_dup(self):
		data = {
			"email": "test@gmail.com",
			"username": "Migrated_User",
			"pwd": "secretweaktestpassword",
			"syncDate": "2021-13-22 11:22:45.827167",
			"version": "v4.0.0"
		}

		response = self.client.post(f"{base_url}/api/v3/signUp/", data)
		self.assertEqual(response.status_code, 400)

	def test_signUp_400_name_char(self):
		data = {
			"email": "test@gmail.com",
			"username": "Migrated_User🥇",
			"pwd": "secretweaktestpassword",
			"syncDate": "2021-13-22 11:22:45.827167",
			"version": "v4.0.0"
		}

		response = self.client.post(f"{base_url}/api/v3/signUp/", data)
		self.assertEqual(response.status_code, 400)

	def test_logIn_migrated_200(self):
		data = {
			"username": "Migrated_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/logIn/", data)
		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username="Migrated_User")
		self.assertEqual(user.has_usable_password(), True)

	def test_logIn_new_200(self):
		data = {
			"username": "New_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/logIn/", data)
		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username="New_User")
		self.assertEqual(user.has_usable_password(), True)

	def test_logIn_migrated_401(self):
		data = {
			"username": "Migrated_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/logIn/", data)
		self.assertEqual(response.status_code, 401)

	def test_logIn_new_401(self):
		data = {
			"username": "New_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/logIn/", data)
		self.assertEqual(response.status_code, 401)

	def test_logIn_404(self):
		data = {
			"username": "wronguser",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/logIn/", data)
		self.assertEqual(response.status_code, 404)

	def test_delete_migrated_204(self):
		data = {
			"username": "Migrated_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/deleteAccount/", data)
		self.assertEqual(response.status_code, 204)
		group = Groups.objects.get(group_name="Test Group")
		self.assertEqual(group.members, 3)
		self.assertEqual(User.objects.filter(username="Migrated_User").exists(), False)

	def test_delete_new_204(self):
		data = {
			"username": "New_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/deleteAccount/", data)
		self.assertEqual(response.status_code, 204)
		group = Groups.objects.get(group_name="Test Group")
		self.assertEqual(group.members, 3)
		self.assertEqual(User.objects.filter(username="New_User").exists(), False)

	def test_delete_new_401(self):
		data = {
			"username": "New_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/deleteAccount/", data)
		self.assertEqual(response.status_code, 401)

	def test_delete_migrated_401(self):
		data = {
			"username": "Migrated_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/deleteAccount/", data)
		self.assertEqual(response.status_code, 401)

	def test_delete_migrated_404(self):
		data = {
			"username": "wronguser",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/deleteAccount/", data)
		self.assertEqual(response.status_code, 404)

	def test_changeUsername_migrated_200(self):
		data = {
			"username": "Migrated_User",
			"newUsername": "New_M_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/changeUsername/", data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.filter(username="Migrated_User").exists(), False)
		self.assertEqual(User.objects.filter(username="New_M_User").exists(), True)

	def test_changeUsername_new_200(self):
		data = {
			"username": "New_User",
			"newUsername": "New_New_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/changeUsername/", data)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.filter(username="New_User").exists(), False)
		self.assertEqual(User.objects.filter(username="New_New_User").exists(), True)

	def test_changeUsername_name_401(self):
		data = {
			"username": "New_User",
			"newUsername": "Migrated_User",
			"pwd": "secretweaktestpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/changeUsername/", data)
		self.assertEqual(response.status_code, 401)

	def test_changeUsername_new_401(self):
		data = {
			"username": "New_User",
			"newUsername": "Migrated_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/changeUsername/", data)
		self.assertEqual(response.status_code, 401)

	def test_changeUsername_migrated_401(self):
		data = {
			"username": "Migrated_User",
			"newUsername": "Migrated_User",
			"pwd": "wrongpassword",
		}

		response = self.client.post(f"{base_url}/api/v3/changeUsername/", data)
		self.assertEqual(response.status_code, 401)

	def test_groups(self):
		response = self.client.get(f"{base_url}/api/v3/groups/")
		self.assertEqual(response.status_code, 200)
		item_to_check = "Test Group"
		self.assertIn(item_to_check, response.content.decode())

	def test_joinGroup_200(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"pwd": "grouphash",
			"group": "Test Group2"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 200)
		group = Groups.objects.get(group_name="Test Group2")
		self.assertEqual(group.members, 5)
		user = User.objects.get(username="New_User")
		profile = User_Profile.objects.get(user=user)
		item_to_check = "Test Group2"
		self.assertIn(item_to_check, profile.groups)

	def test_joinGroup_user_404(self):
		data = {
			"username": "wonguser",
			"authToken": "4a6f89bb34d90c45eb...",
			"pwd": "grouphash",
			"group": "Test Group2"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 404)

	def test_joinGroup_user_401(self):
		data = {
			"username": "New_User",
			"authToken": "wrongtoken",
			"pwd": "grouphash",
			"group": "Test Group2"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 401)

	def test_joinGroup_group_404(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"pwd": "grouphash",
			"group": "wronggroup"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 404)

	def test_joinGroup_group_401(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"pwd": "wronghash",
			"group": "Test Group2"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 401)

	def test_joinGroup_group_403(self):
		group = Groups.objects.get(group_name="Test Group2")
		group.banned.append("New_User")
		group.save()
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"pwd": "grouphash",
			"group": "Test Group2"
		}

		response = self.client.post(f"{base_url}/api/v3/joinGroup/", data)
		self.assertEqual(response.status_code, 403)

	def test_createGroup_200(self):
		data = {
			"username": "New_User",
			"pwd": "grouphash",
			"groupName": "New Group"
		}

		response = self.client.post(f"{base_url}/api/v3/createGroup/", data)
		self.assertEqual(response.status_code, 200)
		group = Groups.objects.get(group_name="New Group")
		self.assertEqual(group.members, 1)
		self.assertEqual(group.pwd_hash, "grouphash")
		self.assertEqual(group.banned, [])
		self.assertEqual(group.admins, ["New_User"])

	def test_createGroup_400(self):
		data = {
			"username": "New_User",
			"pwd": "grouphash",
			"groupName": "Test Group"
		}

		response = self.client.post(f"{base_url}/api/v3/createGroup/", data)
		self.assertEqual(response.status_code, 400)


	def test_leaveGroup_200(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group"
		}

		response = self.client.post(f"{base_url}/api/v3/leaveGroup/", data)
		self.assertEqual(response.status_code, 200)
		group = Groups.objects.get(group_name="Test Group")
		self.assertEqual(group.members, 3)
		user = User.objects.get(username="New_User")
		profile = User_Profile.objects.get(user=user)
		self.assertEqual(profile.groups, [])

	def test_leaveGroup_404(self):
		data = {
			"username": "wronguser",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group"
		}

		response = self.client.post(f"{base_url}/api/v3/leaveGroup/", data)
		self.assertEqual(response.status_code, 404)

	def test_leaveGroup_401(self):
		data = {
			"username": "New_User",
			"authToken": "wrongtoken",
			"group": "Test Group"
		}

		response = self.client.post(f"{base_url}/api/v3/leaveGroup/", data)
		self.assertEqual(response.status_code, 401)

	def test_manageGroup_200(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 200)
		group = Groups.objects.get(group_name="Test Group")
		self.assertEqual(group.pwd_hash, "newhash")
		item_to_check = "NewAdmin"
		self.assertIn(item_to_check, group.admins)

	def test_manageGroup_user_401(self):
		data = {
			"username": "New_User",
			"authToken": "wrongtoken...",
			"group": "Test Group",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 401)

	def test_manageGroup_user_404(self):
		data = {
			"username": "wronguser",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 404)

	def test_manageGroup_group_401(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"oldPwd": "wronghash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 401)

	def test_manageGroup_group_403(self):
		group = Groups.objects.get(group_name="Test Group")
		group.banned.append("New_User")
		group.save()
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 403)

	def test_manageGroup_group_404(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "wronggroup",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 404)

	def test_manageGroup_admin_403(self):
		data = {
			"username": "Migrated_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"oldPwd": "grouphash",
			"newPwd": "newhash",
			"addAdmin": "NewAdmin"
		}

		response = self.client.post(f"{base_url}/api/v3/manageGroup/", data)
		self.assertEqual(response.status_code, 403)

	def test_banUser_200(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 200)
		group = Groups.objects.get(group_name="Test Group")
		self.assertEqual(group.members, 3)
		item_to_check = "Migrated_User"
		self.assertIn(item_to_check, group.banned)
		user = User.objects.get(username="Migrated_User")
		profile = User_Profile.objects.get(user=user)
		item_to_check = "Test Group"
		self.assertNotIn(item_to_check, profile.groups)

	def test_banUser_user_404(self):
		data = {
			"username": "wronguser",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 404)

	def test_banUser_user_401(self):
		data = {
			"username": "New_User",
			"authToken": "wrongtoken...",
			"group": "Test Group",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 401)

	def test_banUser_group_401(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"pwd": "wronghash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 401)

	def test_banUser_group_403(self):
		group = Groups.objects.get(group_name="Test Group")
		group.banned.append("New_User")
		group.save()
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 403)

	def test_banUser_group_404(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "wronggroup",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 404)

	def test_banUser_admin_403(self):
		data = {
			"username": "Migrated_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"group": "Test Group",
			"pwd": "grouphash",
			"toBan": "Migrated_User",
		}

		response = self.client.post(f"{base_url}/api/v3/banUser/", data)
		self.assertEqual(response.status_code, 403)

	# def test_reportUser_200(self):
	# 	data = {
	# 		"username": "New_User",
	# 		"reportUser": "reportuser",
	# 		"message": "test"
	# 	}

	# 	response = self.client.post(f"{base_url}/api/v3/reportUser/", data)
	# 	self.assertEqual(response.status_code, 200)

	def test_setBio_200(self):
		data = {
			"username": "New_User",
			"authToken": "4a6f89bb34d90c45eb...",
			"status": "test"
		}

		response = self.client.post(f"{base_url}/api/v3/setBio/", data)
		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username="New_User")
		profile = User_Profile.objects.get(user=user)
		self.assertEqual(profile.bio, "test")

	def test_setBio_401(self):
		data = {
			"username": "New_User",
			"authToken": "wrongtoken...",
			"status": "test"
		}

		response = self.client.post(f"{base_url}/api/v3/setBio/", data)
		self.assertEqual(response.status_code, 401)

	def test_setBio_404(self):
		data = {
			"username": "wronguser",
			"authToken": "4a6f89bb34d90c45eb...",
			"status": "test"
		}

		response = self.client.post(f"{base_url}/api/v3/setBio/", data)
		self.assertEqual(response.status_code, 404)

	def test_getBio_200(self):
		data = {
			"username": "New_User",
		}

		response = self.client.post(f"{base_url}/api/v3/getBio/", data)
		self.assertEqual(response.status_code, 200)
		item_to_check = "Test bio"
		self.assertIn(item_to_check, response.content.decode())

	def test_getBio_404(self):
		data = {
			"username": "wronguser",
		}

		response = self.client.post(f"{base_url}/api/v3/getBio/", data)
		self.assertEqual(response.status_code, 404)

	def test_getUserInfo_200(self):
		data = {
			"username": "New_User",
		}

		response = self.client.post(f"{base_url}/api/v3/getUserinfo/", data)
		self.assertEqual(response.status_code, 200)

	def test_getUserInfo_404(self):
		data = {
			"username": "wronguser",
		}

		response = self.client.post(f"{base_url}/api/v3/getUserinfo/", data)
		self.assertEqual(response.status_code, 404)

	def test_users_200(self):
		response = self.client.get(f"{base_url}/api/v3/users/")
		self.assertEqual(response.status_code, 200)
		item_to_check = "New_User"
		self.assertIn(item_to_check, response.content.decode())

	def test_season_200(self):
		response = self.client.get(f"{base_url}/api/v3/season/")
		self.assertEqual(response.status_code, 200)

	def test_sync_migrated_200(self):
		data = {
			"username": "Migrated_User",
			"streak": 1000,
			"cards": 1,
			"time": 1.1,
			"syncDate": "2023-06-21 12:19:12.477579",
			"month": 1000,
			"country": "Denmark",
			"retention": 12.3,
			"leagueReviews": 1111,
			"leagueTime": 123,
			"leagueRetention": 78.9,
			"leagueDaysPercent": 100,
			"updateLeague": True,
			"authToken": "4a6f89bb34d90c45eb...",
			"version": "v4.0",
			"sortby": "streak",
		}

		response = self.client.post(f"{base_url}/api/v3/sync/", data)
		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username="Migrated_User")
		profile = User_Profile.objects.get(user=user)
		leaderboard = User_Leaderboard.objects.get(user=user)
		league = User_League.objects.get(user=user)
		self.assertEqual(leaderboard.streak, 1000)
		self.assertEqual(leaderboard.cards_today, 1)
		self.assertEqual(leaderboard.time_today, 1.1)
		self.assertEqual(profile.sync_date, "2023-06-21 12:19:12.477579")
		self.assertEqual(leaderboard.cards_month, 1000)
		self.assertEqual(profile.country, "Denmark")
		self.assertEqual(leaderboard.retention, 12.3)
		self.assertEqual(league.cards, 1111)
		self.assertEqual(league.time_spent, 123)
		self.assertEqual(league.retention, 78.9)
		self.assertEqual(league.days_studied, 100)
		self.assertEqual(profile.version, "v4.0")

	def test_sync_migrated_404(self):
		data = {
			"username": "wronguser",
			"streak": 1000,
			"cards": 1,
			"time": 1.1,
			"syncDate": "2023-06-21 12:19:12.477579",
			"month": 1000,
			"country": "Denmark",
			"retention": 12.3,
			"leagueReviews": 1111,
			"leagueTime": 123,
			"leagueRetention": 78.9,
			"leagueDaysPercent": 100,
			"updateLeague": True,
			"authToken": "4a6f89bb34d90c45eb...",
			"version": "v4.0",
			"sortby": "streak",
		}

		response = self.client.post(f"{base_url}/api/v3/sync/", data)
		self.assertEqual(response.status_code, 404)

	def test_sync_migrated_401(self):
		data = {
			"username": "Migrated_User",
			"streak": 1000,
			"cards": 1,
			"time": 1.1,
			"syncDate": "2023-06-21 12:19:12.477579",
			"month": 1000,
			"country": "Denmark",
			"retention": 12.3,
			"leagueReviews": 1111,
			"leagueTime": 123,
			"leagueRetention": 78.9,
			"leagueDaysPercent": 100,
			"updateLeague": True,
			"authToken": "wrongtoken...",
			"version": "v4.0",
			"sortby": "streak",
		}

		response = self.client.post(f"{base_url}/api/v3/sync/", data)
		self.assertEqual(response.status_code, 401)

	def test_sync_migrated_no_league_200(self):
		data = {
			"username": "Migrated_User",
			"streak": 1000,
			"cards": 1,
			"time": 1.1,
			"syncDate": "2023-06-21 12:19:12.477579",
			"month": 1000,
			"country": "Denmark",
			"retention": 12.3,
			"leagueReviews": 1111,
			"leagueTime": 123,
			"leagueRetention": 78.9,
			"leagueDaysPercent": 99,
			"updateLeague": False,
			"authToken": "4a6f89bb34d90c45eb...",
			"version": "v4.0",
			"sortby": "streak",
		}

		response = self.client.post(f"{base_url}/api/v3/sync/", data)
		self.assertEqual(response.status_code, 200)
		user = User.objects.get(username="Migrated_User")
		profile = User_Profile.objects.get(user=user)
		leaderboard = User_Leaderboard.objects.get(user=user)
		league = User_League.objects.get(user=user)
		self.assertEqual(leaderboard.streak, 1000)
		self.assertEqual(leaderboard.cards_today, 1)
		self.assertEqual(leaderboard.time_today, 1.1)
		self.assertEqual(profile.sync_date, "2023-06-21 12:19:12.477579")
		self.assertEqual(leaderboard.cards_month, 1000)
		self.assertEqual(profile.country, "Denmark")
		self.assertEqual(leaderboard.retention, 12.3)
		self.assertNotEqual(league.cards, 1111)
		self.assertNotEqual(league.time_spent, 123)
		self.assertNotEqual(league.retention, 78.9)
		self.assertNotEqual(league.days_studied, 99)
		self.assertEqual(profile.version, "v4.0")




