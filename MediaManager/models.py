from django.db import models
from django.contrib.auth.models import User

from io import BytesIO

from PIL import Image as PILImage
from PIL import ImageOps
from django.core.files import File

class Image(models.Model):
	identifier 	= models.CharField(
						max_length = 40,
						primary_key = True)
	image 		= models.FileField(
						upload_to = 'uploads/',
						max_length = 255)
	# def save(self, *args, **kwargs):
	# 	image = PILImage.open(self.image)
	# 	# Convert Image to RGB color mode
	# 	image = image.convert('RGB')
	# 	# auto_rotate image according to EXIF data
	# 	image = ImageOps.exif_transpose(image)
	# 	# save image to BytesIO object
	# 	im_io = BytesIO() 
	# 	# save image to BytesIO object
	# 	image.save(im_io, 'JPEG', quality=80) 
	# 	# create a django-friendly Files object
	# 	new_image = File(im_io, name=self.identifier)
	# 	# Change to new image
	# 	self.image = new_image
	# 	super().save(*args, **kwargs)

class UserMedia(models.Model):
	user 			= models.OneToOneField(
								User,
								unique = True,
								on_delete = models.CASCADE,
								primary_key = True)

	profile_photo 	= models.ImageField(
								upload_to ='profile_photos/',
								default ='profile_photos/default/default.png' )

	banner  		= models.ImageField( upload_to="banners/",
								default = "banners/default.jpg")
	class Meta:
		indexes = [
			models.Index(fields = ['user'])
		]
