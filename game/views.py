import logging
import json
from django.db.models import Max
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

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

def game_player_required(function):
    """Decorator to permit only the gameowner to update the game"""
    def wrap(request, *args, **kwargs):
        """Wrapper returns the decorated function if permitted, else returns PermissionDenied"""
        games = request.user.gameplayed_set.all() #games played by the user
        game = Game.objects.get(pk=kwargs['game'])
        if request.user.is_authenticated and game in list(map(lambda x: x.game, games)):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

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
        game = Game.objects.get(pk=game)
        game.increment_viewcount()
        game_owner = False
        if request.user.is_authenticated:
            games = request.user.gameplayed_set.all()
            if game in list(map(lambda x: x.game, games)):
                game_owner = True
        context = {'game': game, 'game_owner': game_owner}
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
@group_required('Developer')
def upload(request):
    """Provides the upload functionality.

    On get it presents a form for uploading a game. On post it processes that form,
    and either redirects with an error or returns a response confirming the upload.

    The following context is provided to the template:
      - form: templates/game/upload.html.
      - errors: a dict containing the errors.

    The form used is a standard ModelForm with nothing special.

    The errors dict used in the templates is copied from Form.errors in case of a
    validation error. The view then redirects to itself with a GET request. The
    errors dict is stored in the current session, in field 'errors'. This field in
    the session is cleared on a GET request.

    :statuscode 200: Success.
    :statuscode 302: Redirection in case of either invalid authorization, or a validation error.

    .. todo:: Upon successful upload it should redirect somewhere, not just give a string response.
    """

    if 'errors' in request.session:
        errors = request.session['errors']
        del request.session['errors']
    else:
        errors = None

    if request.method == 'POST':
        form = UploadGameForm(request.POST, request.FILES)
        if form.is_valid():
            new_game = form.save()
            #adds the developer as a player allowing to play game without buying
            played_game = GamePlayed.objects.create(gameScore=0)
            played_game.game = new_game
            played_game.users.add(request.user)
            played_game.save()
            return HttpResponse('Upload successful!')
        else:
            request.session['errors'] = form.errors
            return HttpResponseRedirect(reverse('game:upload'))
    else:
        form = UploadGameForm()
        return render(request, 'game/upload.html', {'form': form, 'errors': errors})


@require_http_methods(('GET', 'HEAD'))
@login_required
def purchase(request, game):
    try:
        game = Game.objects.get(pk=game)
    except:
        return HttpResponseNotFound()
    games = request.user.gameplayed_set.all()
    if game in list(map(lambda x: x.game, games)):
        messages.add_message(request, messages.INFO, 'You have already purchased the game!')
        return redirect(reverse('game:detail', kwargs={'game':game.id}))
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
        return redirect(reverse('game:detail', kwargs={'game':buy_game.game.id}))
    else:
        return HttpResponse('sorry, you!')

@require_http_methods(('GET', 'HEAD'))
def highscore(request, game):
    if request.is_ajax():
        game = Game.objects.get(pk=game)
        highscore = GamePlayed.objects.filter(game=game).aggregate(Max('gameScore'))
        return HttpResponse(highscore['gameScore__max'])

@require_http_methods(('POST', 'HEAD'))
@csrf_exempt #no csrf for this post
@game_player_required #only the game player
def update_played_game(request, game, user):
    """Fetch the game based on the game id and users from GamePlayed tables, &
    responds based on the messageType received in json data passed with ajax
    request. If the messageType is 'LOAD_REQUEST', it constructs the json data
    and send as response. So, it is with when ERROR messageType is received.
    """
    if request.is_ajax():
        game_played = GamePlayed.objects.get(users__pk=user, game__id=game)
        data = request.POST.get('data')
        data_dict = json.loads(data)
        if data_dict['messageType'] == 'SAVE':
            game_played.gameState = data
            game_played.save()
        if data_dict['messageType'] == 'SCORE':
            game_played.gameScore = data_dict['score']
            game_played.save()
        if data_dict['messageType'] == 'LOAD_REQUEST':
            try:
                data = json.loads(game_played.gameState)
                data['messageType'] = 'LOAD'
                return HttpResponse(json.dumps(data), content_type="application/json")
            except:
                return HttpResponse('error')
        return HttpResponse('Great Job So Far')
    else:
        return HttpResponse('Only ajax')
