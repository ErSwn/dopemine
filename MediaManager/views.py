from django.shortcuts import render
from accounts.models import UserData
from django.contrib.auth.models import User
from django.http import FileResponse

from .models import Image, UserMedia

# Create your views here.
def ProfileMedia(request, username):
	user_key 	= User.objects.get(username=username)
	profileMedia=  UserMedia.objects.get(user=user_key)

	return FileResponse(profileMedia.profile_photo)

def BannerMedia(request, username):
	user_key 	= User.objects.get(username=username)
	data 		=  UserData.objects.get(user=user_key)

	return FileResponse(data.banner)

def Media(request, file):
	img = Image.objects.get(identifier=file)
	
	return FileResponse(img.image)




