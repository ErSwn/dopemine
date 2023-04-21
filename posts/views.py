from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from .serializers import PublicationSerializer
from .models import Bookmark, Publication
from MediaManager.models import Image
from dopemine import settings

import json
import numpy as np
import random
import string
from datetime import datetime
import uuid

def get_user(request):
	user = request.user
	if settings.DEBUG:
		if user.is_authenticated:
			return user
		return User.objects.get(username = '123')
	return user

@require_POST
def setBookmark(request):
	data = json.loads(request.body.decode('utf-8'))['data']
	user = get_user(request)
	postId = data.get('id')
	print(postId)
	post = Publication.objects.get(id=postId)
	value = data.get('value')

	if not user.is_authenticated:
		return Http404('You need to be authenticated')

	if value:
		bookmark = Bookmark.objects.create(user=user, post=post)
		bookmark.save()
	else:
		bookmark = Bookmark.objects.get(user=user, post=post)
		bookmark.delete()

	return HttpResponse(True)

class HomeView(viewsets.ModelViewSet):
	def get_serializer_class(self):
		return PublicationSerializer
	def get_queryset(self):
		data = self.request.GET
		page = int(data.get('page'))
		page_size = 12

		publications = Publication.objects.all()
		paginator = Paginator(publications.order_by('-id'), page_size)

		if not publications.exists():
			return []

		if page >= paginator.num_pages:
			return []

		return paginator.page(page+1)

def upload_images(user, images):
	keys = []
	N = 7
	for index, im in enumerate(images):
		#creates UUID name
		print(im)
		key = str(uuid.uuid4())
		# sets UUID name to file
		extension 	= im._name.split('.')[-1]
		new_name 	= key+'.' +extension
		im._name 	= new_name

		# store file
		Image.objects.create(identifier=key, image = im)
		keys.append(key)
	return keys

def CreatePublication(request):
	if request.method == 'POST':
		description = request.POST['description']
		user 		= request.user
		keys 		= upload_images(request.user, request.FILES.getlist('file'))
		media 		= {str(i):key for i, key in enumerate(keys)}
		publication = Publication.objects.create( owner = user, content=description, media=media )
	return redirect('home')

@require_POST
def makePublication(request):
	upload_images('edua009', dict(request.FILES).get('images'))
	# print(request.body.decode('utf-8'))

	return HttpResponse(1)

class PublicationView(viewsets.ModelViewSet):
	def get_serializer_class(self):
		return PublicationSerializer
	def get_queryset(self):

		data = self.request.GET
		page = int(data.get('page'))
		username = data.get('user')
		user = get_object_or_404(User, username = username)
		page_size = 12

		publications = Publication.objects.filter(owner = user )
		paginator = Paginator(publications.order_by('-id'), page_size)

		if not publications.exists():
			return []

		if page >= paginator.num_pages:
			return []

		return paginator.page(page+1)

