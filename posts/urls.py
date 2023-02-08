from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('posts/bookmark/', views.setBookmark),
]