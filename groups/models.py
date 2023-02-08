from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
	name 	= models.CharField(max_length=100)
	owner 	= models.ForeignKey(User, related_name='group_owner', null=True, on_delete=models.SET_NULL)
	members = models.ManyToManyField(
		User,
		through='Member',
		through_fields = ('group', 'user')
	)

	def __str__(self):
		return f'{self.name}'

class Member(models.Model):
	ADMIN = 1
	MODER = 2
	MEMBER = 3

	ROLE_CHOICES = (
		(ADMIN, 'Administrator'),
		(MODER, 'Moderator'),
		(MEMBER, 'Member'),
	)

	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	user  = models.ForeignKey(User, on_delete=models.CASCADE)
	role  = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

	class Meta:
		unique_together = ('group', 'user')
		indexes = [models.Index(fields = ['group', 'user'])]

	def __str__(self):
		return f'{self.group.name} - {self.user.username} ({ROLE_CHOICES[self.role][1]})'
