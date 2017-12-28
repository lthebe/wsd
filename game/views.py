import logging

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest

from .models import Game

logger = logging.getLogger(__name__)

# Create your views here.

def buy(request, game):
    try:
        g = Game.objects.get(pk=game)
        return HttpResponse(str(g))
    except:
        return HttpResponseNotFound()


def search(request):
    
    if request.method != 'GET':
        logger.debug('games.views.search responded 405')
        return HttpResponseNotAllowed()
    
    q = request.GET.get('q', default=None)
    p = request.GET.get('p', default=0)
    
    return HttpResponse(str(Game.search(q, p)))
