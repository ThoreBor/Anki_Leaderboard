from django.db import models
from django.contrib.auth.models import User

class Groups(models.Model):
	group_name = models.TextField()
	pwd_hash = models.TextField(null=True)
	admins = models.JSONField(default=list)
	banned = models.JSONField(default=list)
	members = models.IntegerField()

class User_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    auth_token = models.TextField(null=True)
    old_hash = models.TextField(null=True)
    country = models.TextField(null=True)
    groups = models.JSONField(null=True, default=list)
    league = models.TextField()
    history = models.JSONField(null=True, default=dict)
    suspended = models.TextField(null=True)
    bio = models.TextField(null=True)
    version = models.TextField(null=True)
    sync_date = models.TextField()

class User_Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    streak = models.IntegerField()
    cards_today = models.IntegerField()
    cards_month = models.IntegerField(null=True)
    time_today = models.FloatField()
    retention = models.FloatField(null=True)

class User_League(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    xp = models.IntegerField()
    time_spent = models.IntegerField()
    cards = models.IntegerField()
    retention = models.FloatField()
    days_studied = models.FloatField()


