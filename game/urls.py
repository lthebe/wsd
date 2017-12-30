"""Game URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')

    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

    Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
import game.views as views

app_name = 'game'

urlpatterns = [
    path('games/<int:game>/', views.details, name='detail'),
    path('games/<int:game>/purchase', views.purchase, name='purchase'),
    path('games/search/', views.search, name='search'),
    path('games/process_purchase', views.process_purchase, name='process'),
    path('games/upload/', views.upload, name='upload'),
]
