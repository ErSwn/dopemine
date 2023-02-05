from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseSuccess
from .models import Bookmark, Publication

def setBookmark(request):
	user = request.user
	postId = request.body.get('postId')

	post = Publication.objects.filter(post_id = postId)

	if not user.is_authenticated():
		return Http404('You need to be authenticated')

	if not post.exists():
		return Http404('Post do not exist')

	bokmark = Bookmark.objects.create(user = user, post = post)
	bokmark.save()

	return HttpResponseSuccess(True)

