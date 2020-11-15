"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from . import website
from . import api
from django.urls import path

app_name = "main"
#path('upload/', website.upload, name="upload"),
urlpatterns = [
	path("", website.reviews, name="reviews"),
    path("time/", website.time, name="time"),
    path("streak/", website.streak, name="streak"),
    path("retention/", website.retention, name="retention"),
    path(r'user/<username>/', website.user, name="user"),
	path('alpha/', website.alpha, name="alpha"),
	path('beta/', website.beta, name="beta"),
	path('gamma/', website.gamma, name="gamma"),
	path('delta/', website.delta, name="delta"),
	path('users/', views.users, name="users"),
	path('getstreaks/', views.getstreaks, name="getstreaks"),
	path('getreviews/', views.getreviews, name="getreviews"),
	path('gettime/', views.gettime, name="gettime"),
	path('sync/', api.sync, name="sync"),
	path('delete/', api.delete, name="delete"),
	path('allusers/', api.all_users, name="allusers"),
	path('getdata/', api.get_data, name="get_data"),
	path('groups/', api.groups, name="groups"),
	path('create_group/', api.create_group, name="create_group"),
	path('league/', api.league_data, name="league_data"),
	path('season/', api.season, name="season"),
	path('setStatus/', api.setStatus, name="setStatus"),
	path('getStatus/', api.getStatus, name="getStatus"),
	path('getUserinfo/', api.getUserinfo, name="Userinfo"),
	path('joinGroup/', api.joinGroup, name="joinGroup"),
	path('manageGroup/', api.manageGroup, name="manageGroup"),
	path('banUser/', api.banUser, name="banUser"),
]
