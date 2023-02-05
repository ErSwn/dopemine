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
from django_ratelimit.decorators import ratelimit

from accounts.models import UserData

from posts.models import Publication, PostLike, Comment, CommentLike
from posts.serializers import PublicationSerializer, CommentSerializer

from MediaManager.models import Image

from relations.models import Follow

from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes,permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

import django
import json
import uuid
import random
import string
from random import randint
from tqdm import tqdm
from urllib.parse import urlparse
from datetime import datetime
from dopemine import settings


def get_user(request):
	# Disable login requirement for development enviroment
	# returns 'edua009' user

	if not settings.DEVELOPMENT:
		user = request.user
	else:
		user = User.objects.get(username = '123')
	return user

@ensure_csrf_cookie
@ratelimit(key='ip', rate='60/m')
def ProfileView(request, profile):
	user = None
	try:
		user 			 = User.objects.get(username=profile)
	except:
		return redirect('home')
	user_data = UserData.objects.get(user = user)

	full_name 		 = user_data.fullname
	user_description = user_data.description
	profile_username = user.username

	follow_count = Follow.objects.filter( follow = user ).count()
	publication_count = Publication.objects.filter(owner = user ).count()

	data = {
		"current_profile":	profile,
		"fullname":			full_name,
		"username":			profile_username,
		"user_description": user_description,
		"follow_count":		follow_count,
		"publication_count":publication_count,
	}

	return render(request, 'views/profile.html', data)

def book_marks(request):
	return redirect('home')

@login_required(login_url='accounts/login')
def home_page(request):
	data = {
		"user":request.user
	}

	return render(request, 'views/home.html', data)

@ensure_csrf_cookie
@ratelimit(key='ip', rate='100/m')
def GalleryView(request, username):
	user 			 = User.objects.get(username=username)
	user_data = UserData.objects.get(user = user)

	full_name 		 = user_data.fullname
	user_description = user_data.description
	profile_username = user.username

	follow_count = Follow.objects.filter( follow = user ).count()
	publication_count = Publication.objects.filter(owner = user ).count()

	data = {
		"current_profile":	username,
		"fullname":			full_name,
		"username":			profile_username,
		"user_description": user_description,
		"follow_count":		follow_count,
		"publication_count":publication_count
	}

	return render(request, 'views/gallery.html', data)

@login_required(login_url='accounts/login')
def saved_view(request):
	return render(request, 'views/saved.html', {"user":username, "items": response})


""" web posts """

@require_POST
@csrf_protect
def MakeLike(request):
	data 	= json.loads(request.body.decode("utf-8"))['data']
	# print(request.body.decode("utf-8"))
	post_id = data['id']
	value 	= data['value']
	user 	= get_user(request)

	if not value:
		PostLike.objects.filter(user = user, post_id = post_id).delete()
	else:
		post = Publication.objects.get(id=post_id)
		PostLike.objects.update_or_create(user=user, post_id=post)

	return HttpResponse(True)

@require_POST
@csrf_exempt
def PostComment(request):
	data 	= json.loads(request.body.decode('utf-8'))['data']
	post_id = data['post_id']
	content = data['content']
	user 	= get_user(request)
	post 	= Publication.objects.get(id = post_id)

	Comment.objects.create(author=user, post_id=post, content =  content)

	return HttpResponse(True)


def upload_images(user, images):
	keys = []
	N = 7
	for index, im in enumerate(images):
		#creates UUID name
		res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=N))
		key = str(user) +str(datetime.now()).replace('-', '').replace('.', '').replace(' ', '').replace(':', '')+str(res)+ str(index)
		key = str(uuid.uuid5(uuid.NAMESPACE_OID, key))

		# sets UUID name to file
		extension 	= im._name.split('.')[-1]
		new_name 	= key+'.' +extension
		im._name 	= new_name

		# store file
		Image.objects.create(identifier=key, image = im)
		keys.append(key)
	return keys

@login_required(login_url='accounts/login')
def CreatePublication(request):
	print(request.headers)
	if request.method == 'POST':
		description = request.POST['description']
		user 		= request.user
		keys 		= upload_images(request.user, request.FILES.getlist('file'))
		media 		= {str(i):key for i, key in enumerate(keys)}
		publication = Publication.objects.create( owner = user, content=description, media=media )
	return redirect('home')

@require_POST
@login_required(login_url='accounts/login')
def DeletePublication(request):
	Publication.objects.filter(id=request.POST['id'],  owner = request.user).delete()	
	return redirect('home')

@require_POST
@login_required(login_url='accounts/login')
def post_comment(request):
	comment = Comment.objects.create(
		author 	= request.user,
		content = content )
	comment.save()

class CommentView(viewsets.ModelViewSet):
	def get_serializer_class(self):
		return CommentSerializer
	def get_queryset(self):
		print(self.request)
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

class TodoView(viewsets.ModelViewSet): 
	def get_serializer_class(self):
		return TodoSerializer
	def get_queryset(self):
		page 		= int(self.request.query_params['pagination'])
		page_size 	= 12
		origin 		= self.request.META['HTTP_REFERER']
		user 		= urlparse(origin).path.split('/')[1]

		if user == '':
			query_object = Publication.objects.all()
		else:
			owner 	= User.objects.get(username=user)
			query_object = Publication.objects.filter(owner=owner)
			
		paginator = Paginator(
						query_object.order_by('-id'),
						page_size )

		if page >= paginator.num_pages:
			return []

		response = paginator.page(page+1)
		return response