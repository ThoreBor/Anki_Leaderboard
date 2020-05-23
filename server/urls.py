from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
	path("", views.reviews, name="reviews"),
    path("time/", views.time, name="time"),
    path("streak/", views.streak, name="streak"),
    path("retention/", views.retention, name="retention"),
	path('sync/', views.sync, name="sync"),
	path('users/', views.users, name="users"),
	path('getstreaks/', views.getstreaks, name="getstreaks"),
	path('getreviews/', views.getreviews, name="getreviews"),
	path('gettime/', views.gettime, name="gettime"),
	path('delete/', views.delete, name="delete"),
	path('allusers/', views.all_users, name="allusers"),
	path('getdata/', views.get_data, name="get_data"),

]
