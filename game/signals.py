import logging

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Game

logger = logging.getLogger(__name__)

@receiver(pre_delete, sender=Game, dispatch_uid='game_delete_receiver')
def gameDeleteHandler(sender, instance, **kwargs):
    """Signal handler for game.models.Game pre_delete signal.
    
    This signal handler removes the gameimage file from the filesystem.
    """
    instance.gameimage.delete(save=False)
