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
    average_rating = serializers.FloatField(source='get_rating', read_only=True)
    
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
