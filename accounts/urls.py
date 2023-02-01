from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('login', views.login_user, name = 'login' ),
	path('register', views.register_user, name = 'register'),
	path("logout", views.logout_request, name= "logout"),
	path('checkusername', views.checkUsername)
	# path('profile/config/', views.configProfile, name = 'configProfile'),
]
