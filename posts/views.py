from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseSuccess
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET, require_POST

from .models import Bookmark, Publication
from dopemine import settings

def get_user(request):
	user = request.user
	if settings.DEBUG:
		if user.is_authenticated():
			return user
		return User.objects.get(username = '123')
	return user

@require_POST
def deleteBookmark(request):
	user = get_user(request)
	postId = request.body.get('postId')
	post = Publication.objects.filter(post_id = postId)

	if not user.is_authenticated():
		return Response('', status = status.HTTP_200_OK)

	if not post.exists():
		return Http404('Post Do Not Exists')

	bookmark = Bookmark.objects.filter(user = user, post = post)
	bookmark.delete()
	return Response('', status = status.HTTP_200_OK)

@require_POST
def setBookmark(request):
	user = request.user
	postId = request.body.get('postId')
	post = Publication.objects.filter(post_id=postId)

	if not user.is_authenticated():
		return Http404('You need to be authenticated')

	if not post.exists():
		return Http404('Post do not exist')

	bokmark = Bookmark.objects.create(user=user, post=post)
	bokmark.save()

	return HttpResponseSuccess(True)

