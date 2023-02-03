from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, FileResponse
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.views.decorators.http import require_POST

from accounts.models import UserData
from posts.models import Publication, PostLike, Comment
from posts.serializers import PublicationSerializer, CommentSerializer

from relations.models import Follow
from relations.serializers import FollowSerializer


from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes,permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

import json
import uuid
import random
import string
from random import randint
from tqdm import tqdm
from urllib.parse import urlparse
from datetime import datetime


def get_user(request):
	# Disable login requirement for development enviroment
	# returns 'edua009' user
	self_origin = True

	if self_origin:
		user = request.user
	else:
		user = User.objects.get(username = '123')
	print(user)
	return user



""" API posts """
class PublicationPaginator(viewsets.ModelViewSet): 
	def get_serializer_class(self):
		return PublicationSerializer
	def get_queryset(self):
		page 		= int(self.request.query_params['pagination'])
		page_size 	= 12
		user = self.request.query_params.get('user')
		origin 		= self.request.META['HTTP_REFERER']
		user 		= urlparse(origin).path.split('/')[1]
		
		if user == '':
			query_object = Publication.objects.all()
		else:
			owner = User.objects.get(username=user)
			query_object = Publication.objects.filter(owner = owner)
		
		paginator = Paginator(
						query_object.order_by('-id'),
						page_size )

		if page >= paginator.num_pages:
			return []

		response = paginator.page(page+1)
		return response
		return None


@api_view(['POST'])
@action(detail=False, methods=['post'])
def handleLike(request):
	data 	= request.data
	post_id = data['postId']
	value 	= data['value']
	user 	= get_user(request)

	if value == False:
		PostLike.objects.filter(user = user, post_id = post_id).delete()
	else:
		post = Publication.objects.get(id=post_id)
		PostLike.objects.update_or_create(user=user, post_id=post)
	return HttpResponse(True)

""" API gets """
class CommentView(viewsets.ModelViewSet):
	def get_serializer_class(self):
		return CommentSerializer
	def get_queryset(self):
		page_size 	= 3
		post_id 	= int(self.request.query_params['post_id'])
		page 		= int(self.request.query_params['pagination'])
		comments 	= Comment.objects.filter(post_id=post_id)

		if not comments.exists():
			return []

		pagination = Paginator(comments.order_by('-id'), page_size)
		
		if page >= pagination.num_pages:
			return []

		return pagination.page(page+1)

class user_info(viewsets.ModelViewSet):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_serializer_class(self):
		return UserInfoSerializer
	def get_queryset(self):
		username = self.request.query_params['username']
		user 	 = User.objects.get(username=username)
		info 	 = UserData.objects.filter(user=user)
		return info

class PostApiView(viewsets.ModelViewSet):
	authentication_classes = [TokenAuthentication]
	permission_classes = [AllowAny]

	def get_serializer_class(self):
		return PublicationSerializer
	def get_queryset(self):
		page_size 	= 12
		page 		= int(self.request.query_params['page'])
		if self.request.query_params['where'] == 'profile' :
			user 	= self.request.query_params['user']
			owner 	= User.objects.get(username=user)
			
			if owner:
				query_object = Publication.objects.filter(owner=owner)
			else:
				return []
		else:
			query_object = Publication.objects.all()

		paginator = Paginator(
						query_object.order_by('-id'),
						page_size )
	
		if page >= paginator.num_pages:
			return []

		response = paginator.page(page+1)
		return response
 
""" API security """

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def checkToken(request):
	return JsonResponse({'success':True})

@csrf_exempt
def token_security(request):
	return JsonResponse({'csrfToken': get_token(request)})

@csrf_protect
def checkcsrf(request):
	return JsonResponse({'success':True})

