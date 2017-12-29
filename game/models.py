from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    """Game model

    referr to README.md for database schema.

    :members: name, url, description, gameimage

    .. todo::
        Relations with user models.
    """

    name        = models.TextField(max_length=300)
    url         = models.URLField()
    description = models.TextField()
    gameimage   = models.ImageField()

    @classmethod
    def create(cls, name, url, description='', gameimage=''):
        """Creates an object. Use this function instead of calling the class
        constructor.
        """

        game = cls(name=name, url=url, description=description, gameimage=gameimage)
        return game

    def __str__(self):
        return 'Game {0}, name: {1}, url: {2}'.format(
            self.pk,
            self.name,
            self.url
        )

class GamePlayed(models.Model):
    """GamePlayed model - when a user buys a game, the game is added to the
    GamePlayed database with gameState field empty, but users field with the
    user who bought the game.
    After the subsequent games, only the gameState for the user is updated.

    For storing extra information -how much a user paid for game (if needed),
    a middle model could be used in many to many relationship
    as referred to README.md for database schema.

    :members: game, gameScore, gameState, users

    """

    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    gameScore = models.IntegerField()
    gameState = models.TextField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return 'Game {0}, GameState: {1}'.format(
            self.game.name,
            self.gameState
        )
