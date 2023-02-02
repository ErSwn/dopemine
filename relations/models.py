from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
	user 	= models.ForeignKey(User,related_name='user_id', on_delete=models.CASCADE)
	follow 	= models.ForeignKey(User,related_name='follows', on_delete=models.CASCADE)
	date 	= models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['user', 'follow']
		indexes = [
			models.Index(fields = ['user', 'follow'])
		]
