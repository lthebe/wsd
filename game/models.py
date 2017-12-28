from django.db import models

# Create your models here.

class Game(models.Model):
    
    name        = models.TextField()
    url         = models.TextField()
    description = models.TextField()
    gameimage   = models.TextField()
    
    @classmethod
    def create(cls, name, url, description='', gameimage=''):
        game = cls(name=name, url=url, description=description, gameimage=gameimage)
        return game
    
    def __str__(self):
        return 'Game {0}, name: {1}, url: {2}'.format(
            self.pk,
            self.name,
            self.url
        )