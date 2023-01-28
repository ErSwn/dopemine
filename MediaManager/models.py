from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Image(models.Model):
	identifier = models.CharField(max_length=40, primary_key=True)
	image = models.FileField(upload_to='uploads/', max_length=255)

class UserMedia(models.Model):
	user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, primary_key=True)
	profile_photo = models.ImageField(upload_to='profile_photos/',
					default='profile_photos/default/default.jpg' )
	banner = models.ImageField( upload_to="banners/",
								default = "banners/default.jpg")
	class Meta:
		indexes = [
			models.Index(fields = ['user'])
		]
