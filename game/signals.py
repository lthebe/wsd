import logging

from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .models import Game, PaymentDetail

logger = logging.getLogger(__name__)

@receiver(pre_delete, sender=Game, dispatch_uid='game_delete_receiver')
def gameDeleteHandler(sender, instance, **kwargs):
    """Signal handler for game.models.Game pre_delete signal.
    
    This signal handler removes the gameimage file from the filesystem.
    """
    instance.gameimage.delete(save=False)

@receiver(post_save, sender=PaymentDetail, dispatch_uid='payment_deatil_save_receiver')
def paymentDetailSaveHandler(sender, instance, created, **kwargs):
    if created:
        instance.game_played.game.increment_sellcount(price=instance.cost)