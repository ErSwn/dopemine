from django.db import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import User

class UserData(models.Model): 
	user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, primary_key=True)
	fullname = models.CharField(max_length=100)
	profile_photo = models.ImageField(upload_to='profile_photos/',
					default='profile_photos/default/default.jpg' )
	banner = models.ImageField( upload_to="banners/",
								default = "banners/default.jpg")
	description = models.CharField(max_length=499,
		default='''No profile description''')
	class Meta:
		indexes = [
			models.Index(fields = ['user'])
		]
