import logging
import re

from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F
from django.utils import timezone

logger = logging.getLogger(__name__)

# Create your models here.

#https://stackoverflow.com/questions/34239877/django-save-user-uploads-in-seperate-folders
def user_directory_path(instance, filename):
    return 'user_{0}/game/{1}'.format(instance.developer.id, filename)

class Game(models.Model):
    """Game model

    referr to README.md for database schema.

    :members: title, url, description, gameimage

    .. todo::
        Relations with user models.
    """

    title         = models.TextField(max_length=300, unique=True)
    developer     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    url           = models.URLField()
    price         = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    description   = models.TextField()
    gameimage     = models.ImageField(null=True, blank=True, upload_to=user_directory_path)
    viewcount     = models.PositiveIntegerField(default=0)
    sellcount     = models.PositiveIntegerField(default=0)
    upload_date   = models.DateTimeField(default=timezone.now)
    
    ratings       = models.IntegerField(default=0)
    total_rating  = models.IntegerField(default=0)
    

    class Meta:
           ordering = ['viewcount', 'sellcount']

    def increment_viewcount(self):
        self.viewcount = F('viewcount') + 1
        self.save()

    def increment_sellcount(self):
        self.sellcount = F('sellcount') + 1
        self.save()
    
    
    def add_rating(self, rating):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.ratings = F('ratings') + 1
        self.total_rating = F('total_rating') + rating
        self.save()
    
    def remove_rating(self, rating):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.ratings = F('ratings') - 1
        self.total_rating = F('total_rating') + rating
        self.save()
    
    def change_rating(self, change):
        """
        .. note:: Use GamePlayed.set_rating rather than calling this function directly.
        """
        self.total_rating = F('total_rating') + change
        self.save()
    
    def get_rating_cleaned(self):
        """Returns the ratings as they should be read by the game/rating.html
        template.
        
        The game/rating template requires the rating to be given times a factor of
        two to permit half stars to be given as an integer. Examples, 10 is 5 stars,
        5 is 2 and a half star.
        """
        if self.ratings > 0:
            return int((self.total_rating / self.ratings) * 2 + 0.5)
        else:
            return 0

    @classmethod
    def create(cls, title, url, developer, price = 0.0, description='', gameimage=None, viewcount=0):
        """Creates an object. Use this function instead of calling the class
        constructor.
        """

        game = cls(
            title=title,
            url=url,
            price=price,
            developer = developer,
            description=description,
            gameimage=gameimage,
            viewcount=viewcount
        )
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
                    Q(title__contains=word) |
                    Q(description__contains=word))

            return cls.objects.all().filter(query)

    def __str__(self):
        return 'Game {0}, title: {1}, url: {2}'.format(
            self.pk,
            self.title,
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

    game      = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    gameScore = models.IntegerField()
    gameState = models.TextField(default="{''}")
    users     = models.ManyToManyField(User, through="PaymentDetail")
    rating    = models.IntegerField(default=0)
    
    def set_rating(self, rating):
        """Gives a rating from a user to a game.
        """
        if self.rating == 0:
            self.game.add_rating(rating)
        else:
            self.game.change_rating(rating - self.rating)
        self.rating = rating
        self.save()

    def __str__(self):
        if (self.game):
            gametitle = self.game.title
        else:
            gametitle = 'Game Deleted'
        return 'Game {0}, GameState: {1}'.format(
            gametitle,
            self.gameState
        )

class PaymentDetail(models.Model):
    """PaymentDetail model - this model is used as a link between gameplayed and
    users many to many relationship. When game is purchased, it is added here.

    :members: game_played, cost, user, selldate
    -Game purchased is stored in game_played as GamePlayed
    -cost is the price of the game
    -user is the buyer of the game
    -selldate is the date of purchase

    """
    game_played = models.ForeignKey(GamePlayed, null=True, on_delete=models.SET_NULL)
    cost = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(Decimal('0.01'))])
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    selldate = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        if (self.user):
            user = self.user.username
        else:
            user = 'Account Deleted'
        if (self.game_played.game):
            game = self.game_played.game.title
        else:
            game = 'Game Deleted'
        return '{0} owns {1}'.format(
            user,
            game
        )
