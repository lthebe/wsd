from django.contrib.auth.models import User
from game.models import Game

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class GameSerializer(serializers.ModelSerializer):
    
    developer = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
    
    class Meta:
        model = Game
        fields = ('title', 'developer', 'url', 'price')
        depth = 1
