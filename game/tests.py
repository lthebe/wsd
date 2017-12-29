import logging

from functools import reduce

from django.test import TestCase, Client
from django.urls import reverse

from game.models import Game

logger = logging.getLogger(__name__)

# Create your tests here.

class BuyViewTest(TestCase):
    """Tests the buy view responses. This really is just a test of finding the games
    by their private keys.
    """
    
    def setUp(self):
        
        logger.debug('BuyViewTest.setUp')
        
        self.client = Client()
        Game.create(name='name', url='url').save()
    
    def testResponses(self):
        """Tests the response codes"""
        
        game = Game.objects.all()[0]
        pk = game.pk
        
        response = self.client.get(reverse('game:buy', args=[pk]))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('game:buy', args=[pk + 1]))
        self.assertEquals(response.status_code, 404)

class GameSearchTest(TestCase):
    """Tests the search function of the Game model.
    
    Given that these tests are implemented here, testing for which games a query finds
    on the views is unnessecary.
    """
    
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
        
    def testEmptyQuery(self):
        """Tests if an empty query returns all games in the database"""
        
        qset = Game.search(None)
        self.assertEquals(len(qset), len(Game.objects.all()))
    
    def testNameSearch(self):
        """Tests if games are found by their names"""
        
        qset = Game.search('foo')
        self.assertEquals(len(qset), 4)
        qset = Game.search('bar')
        self.assertEquals(len(qset), 4)
        qset = Game.search('foo bar')
        self.assertEquals(len(qset), 2)
        qset = Game.search('foo baz')
        qset = Game.search('foo bar baz')
        self.assertEquals(len(qset), 1)
        qset = Game.search('baz bar foo')
        self.assertEquals(len(qset), 1)
    
    def testStringSearch(self):
        """Tests if string searches work correctly.
        
        This verifies that a query like '"foo bar"' finds different results than
        'foo bar'.
        """
    
        qset = Game.search('"foo bar"')
        self.assertEquals(len(qset), 2)
        qset = Game.search('"foo baz"')
        self.assertEquals(len(qset), 1)
        qset = Game.search('"foo bar" baz')
        self.assertEquals(len(qset), 1)
    
    def testDescriptionSearch(self):
        """Tests that games can be found by their description."""
        
        qset = Game.search('some')
        self.assertEquals(len(qset), 2)
        qset = Game.search('title')
        self.assertEquals(len(qset), 2)
        qset = Game.search('game')
        self.assertEquals(len(qset), 4)
    