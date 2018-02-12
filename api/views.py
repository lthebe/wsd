import logging

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group

from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from game.models import Game, GamePlayed

from .serializers import  UserSerializer, GameSerializer, GamePlayedSerializer, UserGamePlayedSerializer

logger = logging.getLogger(__name__)

def order_by_filter(request, qset, serializer_class):
    """Orders a queryset based on the url param 'order_by'. Supports both regular
    sorting and reverse sorting with a '-' sign before the name to order by.
    
    Fields that can be ordered by must be declared in Meta.ordering_fields in the
    serializer class.
    """
    order_by = request.query_params.get('order_by', None)
    if order_by is not None:
        if (order_by in serializer_class.Meta.ordering_fields
        or (order_by[0] == '-'
        and order_by[1:] in serializer_class.Meta.ordering_fields)):
            qset = qset.order_by(order_by)
    return qset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows for querying users. Based on UserSerializer.
    
    This viewset has a games view which gives the bought games for a player.
    
    serializer:
        GameSerializer
    queryset:
        All users
    """
    
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    def get_queryset(self):
        return order_by_filter(
            self.request,
            User.objects.all(),
            self.serializer_class
        )
    
    @detail_route(methods=['get'])
    def games(self, request, username=None):
        """Detail view for querying the games bought by a player. Serialized with
        GamePlayedSerializer
        """
        user = self.get_object()
        qset = order_by_filter(request, user.gameplayed_set, GamePlayedSerializer)
        serializer = GamePlayedSerializer(qset, many=True)
        return Response(serializer.data)

class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    """Same as UserViewSet, with a few notable differences.
    
    This viewset uses a queryset of only developers, as opposed to UserViewSet which
    includes all user accounts.
    
    The games method of this viewset queries the games developed by a developer. To
    get the games the developer account has bought, use games view for users.
    
    serializer:
        GameSerializer
    queryset:
        All users belonging to the 'Developer' group
    """
    
    serializer_class = UserSerializer
    lookup_field = 'username'
    
    def get_queryset(self):
        return order_by_filter(
            self.request,
            Group.objects.get(name='Developer').user_set.all(),
            self.serializer_class
        )
    
    @detail_route(methods=['get'])
    def games(self, request, username=None):
        """Detail view for querying the games developed by a developer, serializer
        with GameSerializer
        """
        user = self.get_object()
        qset = order_by_filter(request, user.game_set, GameSerializer)
        serializer = GameSerializer(qset, many=True)
        return Response(serializer.data)

class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows for querying the games, with all statistics included.
    
    serializer:
        GameSerializer
    queryset:
        All games.
    """
    
    serializer_class = GameSerializer
    lookup_field = 'title'
    
    def get_queryset(self):
        return order_by_filter(
            self.request,
            Game.objects.all(),
            self.serializer_class
        )
    
    @detail_route(methods=['get'])
    def buyers(self, request, title=None):
        """Detail view for querying the users who have bought a game, serialized with
        UserSerializer.
        """
        game = self.get_object()
        qset = order_by_filter(
            request,
            GamePlayed.objects.all().filter(game=game),
            UserGamePlayedSerializer
        )
        serializer = UserGamePlayedSerializer(qset, many=True)
        return Response(serializer.data)