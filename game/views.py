from django.shortcuts import render

from django.http import HttpResponse, HttpResponseNotFound

from .models import Game

# Create your views here.

def buy(request, game):
    try:
        g = Game.objects.get(pk=game)
        return HttpResponse(str(g))
    except:
        return HttpResponseNotFound()
