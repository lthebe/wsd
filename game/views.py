import logging

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .models import Game

import accounts.urls

logger = logging.getLogger(__name__)

# Create your views here.

@require_http_methods(('GET', 'HEAD'))
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

@require_http_methods(('GET', 'HEAD'))
def search(request):
    """Gives the result page for a search query.
    
    The following context is provided to the template:
    
    - hits: queryset containing all the models for the current page in the query.
    - page: the number of the current page.
    - numpages: the total number of pages found in the query.
    - query: the original query string.
    
    GET Params:
    
    - q: The search query string. If not provided it finds all games.
    - p: The page number.
    
    The number of games in a response is limited by a maximum page size. Page numbers
    start from 1. If not provided it defaults to 1.
    
    :statuscode 200: Success.
    :statuscode 400: Bad request if page number is 0 or lower.
    
    .. todo:: Make the template presentable.
    """
    
    pagelen = 20
    
    q = request.GET.get('q', default=None)
    p = int(request.GET.get('p', default=1))
    
    if p <= 0:
        return HttpResponseBadRequest()
    
    qset = Game.search(q)
    qlen = len(qset)
    numpages = (qlen + pagelen - 1) // pagelen
    qset = qset[(p - 1) * pagelen : p * pagelen]
    
    return render(request,
        template_name='game/search.html',
        context={
            'hits': qset,
            'page': p,
            'numpages': numpages,
            'query': q,
        })

@require_http_methods(('GET', 'HEAD'))
@login_required
def upload(request):
    
    return HttpResponse('upload view.')
