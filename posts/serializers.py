from .models import Publication, PostLike, Comment, Bookmark
from rest_framework  import serializers
from accounts.models import UserData
from django.contrib.auth.models import User
from dopemine import settings

def get_user(request):

    if not settings.DEVELOPMENT:
        user = request.user
    else:
        user = User.objects.get(username = '123')
    return user

class CommentSerializer(serializers.ModelSerializer):
    username    = serializers.CharField(source='author.username')
    full_name   = serializers.SerializerMethodField()

    class Meta:
        model   = Comment
        fields  = ('id', 'username','content', 'date', 'full_name')

    def get_full_name(self, instance):
        return UserData.objects.get(user=instance.author).fullname

class PublicationSerializer(serializers.ModelSerializer):
    username 		= serializers.CharField(source='owner.username')
    full_name 		= serializers.SerializerMethodField()
    like_count 		= serializers.SerializerMethodField()
    liked_by_user 	= serializers.SerializerMethodField()
    comment_count 	= serializers.SerializerMethodField()
    bookmark        = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = ('username', 
                'full_name',
                'id',
                'content',
                'date_of_publication',
                'media',
                'like_count',
                'liked_by_user',
                'comment_count',
                'bookmark')

    def get_full_name(self, instance):
        return UserData.objects.get(user=instance.owner).fullname

    def get_like_count(self, instance):
        return PostLike.objects.filter(post_id = instance.id ).count()

    def get_liked_by_user(self, instance):
        user = get_user(self.context['request'])
        return PostLike.objects.filter(user=user, post_id = instance).exists()
    
    def get_comment_count(self, instance):
        return Comment.objects.filter(post_id = instance.id ).count()

    def get_bookmark(self, instance):
        user = get_user(self.context['request'])
        return Bookmark.objects.filter(user = user, post = instance).exists()