from django.db import models
from django.contrib.auth.models import User
from posts.models import Publication

# Create your models here.
class Bookmark(models.Model):
	user = models.ForeignKey(
					User,
					primary_key = True,
					on_delete=models.CASCADE)

	publication = models.ForeignKey(
					Publication,
					on_delete=models.CASCADE)
