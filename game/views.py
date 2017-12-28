import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from .models import Game

logger = logging.getLogger(__name__)

# Create your views here.

def buy(request, game):
    """Presents a game for buying.
    
    At the moment this view only responds with a string describing the game object.
    
    Args:
        game (int): The private key of the game.
    
    :statuscode 200: Success.
    :statuscode 404: Game not found.
    """
    
    try:
        g = Game.objects.get(pk=game)
        return HttpResponse(str(g))
    except:
        return HttpResponseNotFound()


def search(request):
    """Gives the result page for a search query.
    
    At the moment this view only responds with a string describing the result of the
    search query.
    
    GET Params:
        q:  The search query string. If not provided it finds all games.
        p:  The page number. The number of games in a response is limited by a maximum
            page size. Page numbers start from 0.
    
    :statuscode 200: Success
    """
    
    if request.method != 'GET':
        logger.debug('games.views.search responded 405')
        return HttpResponseNotAllowed()
    
    q = request.GET.get('q', default=None)
    p = request.GET.get('p', default=0)
    
    return HttpResponse(str(Game.search(q, p)))
