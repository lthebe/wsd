import logging

from functools import reduce

from django.test import TestCase, Client
from django.urls import reverse

from game.models import Game

logger = logging.getLogger(__name__)

# Create your tests here.

class BuyViewTest(TestCase):
    
    def setUp(self):
        
        logger.debug('BuyViewTest.setUp')
        
        self.client = Client()
        Game.create(name='name', url='url').save()
    
    def testResponses(self):
        
        game = Game.objects.all()[0]
        pk = game.pk
        
        response = self.client.get(reverse('game:buy', args=[pk]))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('game:buy', args=[pk + 1]))
        self.assertEquals(response.status_code, 404)

class GameSearchTest(TestCase):
    
    def setUp(self):
        
        logger.debug('GameSearchTest.setUp')
        
        for i in range(1, 8):
            name = ''
            name += 'foo ' if i & 1 == 1 else ''
            name += 'bar ' if i & 2 == 2 else ''
            name += 'baz ' if i & 4 == 4 else ''
            Game.create(name, '').save()
        
        Game.create('game1', '', description='some description').save()
        Game.create('game2', '', description='also some description').save()
        Game.create('title', '', description='this game has a title').save()
        Game.create('another game', '', description='this game also has a title').save()
        
    def testNameSearch(self):
        
        qset = Game.search('foo')
        self.assertEquals(len(qset), 4)
        qset = Game.search('bar')
        self.assertEquals(len(qset), 4)
        qset = Game.search('foo bar')
        self.assertEquals(len(qset), 2)
        qset = Game.search('foo bar baz')
        self.assertEquals(len(qset), 1)
        qset = Game.search('baz bar foo')
        self.assertEquals(len(qset), 1)
    
    def testDescriptionSearch(self):
        
        qset = Game.search('some')
        self.assertEquals(len(qset), 2)
        qset = Game.search('title')
        self.assertEquals(len(qset), 2)
        qset = Game.search('game')
        self.assertEquals(len(qset), 4)
        
    def testPageLimits(self):
        
        qset1 = Game.search(None, p=0, pagelen=5)
        qset2 = Game.search(None, p=1, pagelen=5)
        qset3 = Game.search(None, p=2, pagelen=5)
        self.assertEquals(len(qset1), 5)
        self.assertEquals(len(qset2), 5)
        self.assertEquals(len(qset3), 1)
        
        collision = reduce(lambda a, b: a or b,
        map(lambda key: key in (game.pk for game in qset2),
        (game.pk for game in qset1)))
        self.assertFalse(collision)
    