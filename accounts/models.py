from django.db import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import User

class UserData(models.Model): 
	user 		= models.OneToOneField(User,  unique=True, on_delete=models.CASCADE, primary_key=True)
	fullname 	= models.CharField(max_length=100)
	banner 		= models.ImageField( upload_to="banners/",
								default = "banners/default.jpg")
	description = models.CharField(max_length=499,
						default='''No profile description''')

class Profile(models.Model):
	user 		= models.OneToOneField(User, db_index=True,  unique = True, on_delete=models.CASCADE)
	fullname 	= models.CharField(max_length=100)
	description = models.CharField(max_length=500, default = 'Not profile description')
	email 		= models.EmailField(max_length = 254)
	active 		= models.BooleanField(default=True)

	def __str__(self):
		return f'{self.user.username} - {self.email}'

	


