from django.urls import path, include   
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('image/<str:file>', views.Media),
    path('profile/media/<str:username>', views.ProfileMedia),
    path('banners/<slug:username>/', views.BannerMedia),
]