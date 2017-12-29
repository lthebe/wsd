import logging
import re

from django.db import models
from django.db.models import Q

logger = logging.getLogger(__name__)

# Create your models here.

class Game(models.Model):
    """Game model
    
    referr to README.md for database schema.
    
    :members: name, url, description, gameimage
    
    .. todo::
        Relations with user models.
    """
    
    name        = models.TextField(unique=True)
    url         = models.TextField()
    description = models.TextField()
    gameimage   = models.TextField()
    
    @classmethod
    def create(cls, name, url, description='', gameimage=''):
        """Creates an object. Use this function instead of calling the class
        constructor.
        """
        
        game = cls(name=name, url=url, description=description, gameimage=gameimage)
        return game
    
    @classmethod
    def search(cls, q):
        """Searches for games in the database.
        
        Args:
            q (str):
                The search query string. If None then it fetches all games from database
        
        Return:
            A queryset containing all the found games.
        """
        
        if q is None:
            return cls.objects.all()
        else:
            qwords = map(lambda m: m[0] if len(m[0]) > 0 else m[1],
                re.findall(r'"(.+)"|(\S+)', q))
            query = Q()
            for word in qwords:
                query = query & (
                    Q(name__contains=word) |
                    Q(description__contains=word))
            
            return cls.objects.all().filter(query)
    
    def __str__(self):
        return 'Game {0}, name: {1}, url: {2}'.format(
            self.pk,
            self.name,
            self.url
        )