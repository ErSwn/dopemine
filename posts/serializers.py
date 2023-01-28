from .models import Publication, PostLike, Comment
from rest_framework  import serializers
from accounts.models import UserData

self_origin = True

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

    class Meta:
        model = Publication
        fields = ('username', 'full_name','id', 'content', 'date_of_publication', 'media', 'like_count', 'liked_by_user', 'comment_count')
    
    def get_full_name(self, instance):
        return UserData.objects.get(user=instance.owner).fullname

    def get_like_count(self, instance):
        return PostLike.objects.filter(post_id = instance.id ).count()

    def get_liked_by_user(self, instance):
        if self_origin:
            user = self.context['request'].user
        else:
            username = 'edua009'
            user = User.objects.get( username = username )

        return PostLike.objects.filter(user=user, post_id = instance).exists()
    def get_comment_count(self, instance):
        return Comment.objects.filter(post_id = instance.id ).count()

