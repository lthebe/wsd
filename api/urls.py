"""Api URL Configuration"""

from django.urls import path
import api.views as views

from rest_framework import routers

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'games', views.GameViewSet)

urlpatterns = router.urls
