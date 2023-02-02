from .models import Follow
from rest_framework  import serializers
from accounts.models import UserData

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Follow
        fields  = '__all__'
