from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.home_page, name = 'home' ),
	path('todo/publish/', views.CreatePublication),
	path('todo/delete', views.DeletePublication, name='delete'),
    path(r'<slug:profile>/', views.ProfileView ),
    path('user/saved/', views.book_marks),
    path('<str:username>/gallery/', views.GalleryView ),
	path('actions/like/', views.MakeLike),
    path('actions/comment/', views.PostComment),
    
]