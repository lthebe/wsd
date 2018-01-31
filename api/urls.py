"""Api URL Configuration"""

from django.urls import path
import api.views as views

app_name = 'api'

#games use game to determine the pk
urlpatterns = [
    #path('games/<int:game>/', views.details, name='detail'),
    #path('games/<int:game>/purchase', views.purchase, name='purchase'),
    #path('games/<int:game>/highscore', views.highscore, name='highscore'),
    #path('games/<int:game>/delete', game_developer_required(views.GameDeleteView.as_view()), name='delete'),
    #path('games/search/', views.search, name='search'),
    #path('games/<int:game>/update', game_developer_required(views.GameUpdateView.as_view()), name='game_update'),
    #path('games/<int:game>/update_playedgame', views.update_played_game, name='update'),
    #path('games/process_purchase', views.process, name='process'),
    #path('games/upload/', views.upload, name='upload'),
    #path('games/<int:game>/rate', views.rate, name='rate'),
]
