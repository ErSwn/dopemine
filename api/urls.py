from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token
router = routers.DefaultRouter()

router.register(r'posts', views.PostApiView, 'posts')
router.register(r'todos', views.PublicationPaginator, 'todo')  
router.register(r'comment', views.CommentView, 'comments')
router.register(r'info', views.user_info, 'usersinfo')
# router.register(r'like', views.handleLike.as_view({'post': 'handleLike'}), 'like')

urlpatterns = [
    path('security/gettoken/', views.token_security),
    path('user/test/900/', obtain_auth_token),
    path('api/', include(router.urls)),
    path('check/test', views.checkToken),
]