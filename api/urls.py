"""Api URL Configuration"""

from django.urls import path
import api.views as views

from rest_framework import routers

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet, base_name='user')
router.register(r'developers', views.DeveloperViewSet, base_name='developer')
router.register(r'games', views.GameViewSet, base_name='game')

urlpatterns = router.urls
