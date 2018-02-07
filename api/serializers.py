from django.contrib.auth.models import User

from game.models import Game, GamePlayed, PaymentDetail
from accounts.models import Profile

from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    """Serializes profiles
    """
    class Meta:
        model = Profile
        fields = ('nickname', 'description', 'image')

class UserSerializer(serializers.ModelSerializer):
    """Serializes users.
    
    This serializer includes a profile field for the user, serialized with
    ProfileSerializer-
    """
    class Meta:
        model = User
        fields = ('username', 'profile')
    
    profile = ProfileSerializer(many=False, read_only=True)

class GameSerializer(serializers.ModelSerializer):
    """Serializes game instances. Used by the games view of the rest api.
    
    Includes pretty much all information about a game, including statistics.
    """
    
    class Meta:
        model = Game
        fields = (
            'title',
            'developer',
            'url',
            'price',
            'description',
            'gameimage',
            'gamethumb',
            'viewcount',
            'sellcount',
            'upload_date',
            'popularity',
            'average_rating',
            'revenue',
        )
        ordering_fields=(
            'title',
            'developer',
            'price',
            'description',
            'viewcount',
            'sellcount',
            'upload_date',
            'popularity',
            'average_rating',
            'revenue'
        )
    
    developer = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
    average_rating = serializers.FloatField(source='get_rating', read_only=True)

class GamePlayedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GamePlayed
        fields = ('game', 'gameScore', 'rating')
        ordering_fields = ('game', 'gameScore', 'rating')
    
    game = serializers.SlugRelatedField(
        slug_field='title',
        many=False,
        read_only=True
    )

class UserGamePlayedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GamePlayed
        fields = ('user', 'gameScore', 'rating')
        ordering_fields = ('user', 'gameScore', 'rating')
    
    user = serializers.SlugRelatedField(
        slug_field='username',
        many=False,
        read_only=True
    )
