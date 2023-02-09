from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from rest_framework import viewsets

from .serializers import PublicationSerializer
from .models import Bookmark, Publication
from dopemine import settings
import json

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
	post = Publication.objects.get(id=postId)
	value = data.get('value')

	if not user.is_authenticated:
		return Http404('You need to be authenticated')

	# if not post.exists():
	# 	return Http404('Post do not exist')
	if value:
		bookmark = Bookmark.objects.create(user=user, post=post)
		bookmark.save()
	else:
		bookmark = Bookmark.objects.get(user=user, post=post)
		bookmark.delete()

	return HttpResponse(True)

def getPostsFromUser(request):
	data = request.GET
	page = int(data.get('page'))
	username = data.get('user')
	user = User.objects.filter(username = username)
	pageSize = 12
	if user.exists():
		return Http404()

	userPublications = Publication.objects.filter(user = user )
	paginator = Paginator(userPublications.order_by('-id'), page_size)

	return Http

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