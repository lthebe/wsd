import pdb

import logging
import pdb

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .models import Game, GamePlayed
from .utils import get_checksum
from .forms import UploadGameForm

import accounts.urls

logger = logging.getLogger(__name__)

# Create your views here.

def group_required(*groups):
    """Requires user membership in at least one of the groups passed in.
    Source: Django Snippets"""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=groups)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@require_http_methods(('GET', 'HEAD'))
def details(request, game):
    """Presents a game for buying.

    At the moment this view only responds with a string describing the game object.

    Args:
        game (int): The private key of the game.

    :statuscode 200: Success.
    :statuscode 404: Game not found.
    """

    try:
        g = Game.objects.get(pk=game)
        context = {'game': g}
        return render(request, template_name='game/game.html', context=context)
    except:
        return HttpResponseNotFound('The game you requested could not found!')

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

#ONLY Developer can upload the game and of course superuser
@group_required('developer')
def upload(request):
    if request.method == 'POST':
        #pdb.set_trace()
        form = UploadGameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Thxbye!')
        else:
            return HttpResponse('Bad boy!')
    else:
        form = UploadGameForm()
        return render(request, 'game/upload.html', {'form': form})


@require_http_methods(('GET', 'HEAD'))
@login_required
def purchase(request, game):
    try:
        game = Game.objects.get(pk=game)
    except:
        return HttpResponseNotFound()
    games = request.user.gameplayed_set.all()
    if len(list(filter(lambda x: x.game.id == game.id, games))) > 0:
        messages.add_message(request, messages.INFO, 'You have already purchased the game!')
        return redirect(reverse('game:detail', kwargs={'game':game.id}))
    #if game in games, don't allow to buy as the user has already the game - todo
    message = "pid={}&sid={}&amount={}&token={}".format(game.id, settings.SELLER_ID, game.price, settings.PAYMENT_KEY)
    checksum = get_checksum(message)
    context =  {'game': game.id, 'checksum': checksum, 'pid': game.id, 'sid': settings.SELLER_ID, 'amount': game.price }
    return render(request, "game/buy.html", context=context)

@require_http_methods(('GET', 'HEAD'))
def process_purchase(request):
    pid = request.GET.get('pid')
    ref = request.GET.get('ref')
    result = request.GET.get('result')
    checksum = request.GET.get('checksum')
    message = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, settings.PAYMENT_KEY)
    if get_checksum(message) == checksum:
        buy_game = GamePlayed.objects.create(gameScore=0)
        buy_game.game = Game.objects.get(pk=pid)
        buy_game.users.add(request.user)
        buy_game.save()
        return HttpResponse('Thank you for the purchase')
    else:
        return HttpResponse('sorry, you!')
