from django.contrib.auth.models import User

from game.models import Game
from accounts.models import Profile

from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'description', 'image')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'profile')
    
    profile = ProfileSerializer(many=False, read_only=True)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = (
            'title',
            'developer',
            'url',
            'price',
            'description',
            'viewcount',
            'sellcount',
            'upload_date',
            'average_rating',
            'popularity',
        )
    
    developer = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
    average_rating = serializers.FloatField(source='get_rating', read_only=True)
