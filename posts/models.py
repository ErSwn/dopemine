from django.db import models
from django.contrib.auth.models import User
def default_media():
  return {'none':"none"}


class Publication(models.Model):
  id      = models.AutoField(primary_key=True)
  owner   = models.ForeignKey(
                  User,
                  on_delete=models.CASCADE,
                  db_index=True)

  content = models.CharField(max_length=4_000)
  media   = models.JSONField(default=default_media)
  date_of_publication = models.DateTimeField(auto_now_add=True)

  class Meta:
    indexes = [models.Index(fields = ['owner', 'id'])]
  
  def __str__(self):
    return f'{self.owner} - {self.date_of_publication} - {id}'


class PostLike(models.Model):
  user    = models.ForeignKey(User, on_delete=models.CASCADE)
  post_id = models.ForeignKey(Publication, on_delete=models.CASCADE)

  class Meta:
    unique_together = (('user', 'post_id'))
    indexes = [models.Index(fields = ['user', 'post_id'])]

  def __str__(self):
    return f'{self.user} - {self.post_id}'

class Comment(models.Model):
  id     = models.AutoField( primary_key=True )
  post_id = models.ForeignKey( Publication, on_delete=models.CASCADE )
  author   = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.CharField( max_length=3000 )
  date   = models.DateTimeField( auto_now_add=True)

  class Meta:
    indexes = [models.Index(fields=['post_id', 'author', 'id'])]

  def __str__(self):
    return f'{self.author} - {self.date} - {self.post_id}'

class CommentLike(models.Model):
  user   = models.ForeignKey(User, on_delete=models.CASCADE)
  post_id = models.ForeignKey(Publication, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

  class Meta:
    unique_together = (('user', 'post_id'))
    indexes = [models.Index(fields = ['user', 'post_id'])]
  
  def __str__(self):
    return f'{self.user} - {self.post_id}'

class Bookmark(models.Model):
  user = models.ForeignKey(User ,on_delete=models.CASCADE)
  post = models.ForeignKey(Publication, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.user} - {self.post}'

  class Meta:
    unique_together = (('user', 'post'))
    indexes = [models.Index(fields = ['user', 'post'])]