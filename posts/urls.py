from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'users', views.PublicationView, 'posts')

urlpatterns = [
    path('posts/bookmark/', views.setBookmark),
    path('posts/', include(router.urls)),
]