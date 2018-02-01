from django.contrib.auth.models import User

from game.models import Game, GamePlayed, PaymentDetail
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
    revenue = serializers.DecimalField(
        source='get_revenue',
        read_only=True,
        decimal_places=2,
        max_digits=10
    )

class GamePlayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamePlayed
        fields = ('game', 'gameScore', 'rating')
    
    game = serializers.SlugRelatedField(
        slug_field='title',
        many=False,
        read_only=True
    )
