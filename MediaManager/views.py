from django.shortcuts import render
from accounts.models import UserData
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse

from .models import Image, UserMedia
import os
from dopemine import settings
from base64 import b64decode, b64encode
# Create your views here.
def ProfileMedia(request, username):
	user_key 	= User.objects.get(username=username)
	user_media=  UserMedia.objects.get(user=user_key)

	return FileResponse(user_media.profile_photo)

def BannerMedia(request, username):
	user_key 	= User.objects.get(username=username)
	user_media 		=  UserData.objects.get(user=user_key)

	return FileResponse(user_media.banner)

def Media(request, file):
	img = Image.objects.get(identifier=file)
	return FileResponse(img.image)

from django.contrib.staticfiles.storage import staticfiles_storage
def get_current_user_profile_photo(request):
	user = request.user
	print(user)

	if not user.is_anonymous:
		user_media=  UserMedia.objects.get(user=user)
		return FileResponse(user_media.profile_photo)
	else:
		user_data = UserData.objects.get(user = user )
		profile_photo = user_data.profile_photo
		file = open(os.path.join(settings.BASE_DIR, 'static\\media\\defaultProfilePhoto.jpg'), 'rb')
		return FileResponse(file)
