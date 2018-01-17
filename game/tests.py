import pdb
import logging

from functools import reduce

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

from game.models import Game, GamePlayed, PaymentDetail

logger = logging.getLogger(__name__)

# Create your tests here.
def get_user():
    user = User.objects.create()
    user.save()
    return user

class BuyViewTest(TestCase):
    """Tests the buy view responses. This really is just a test of finding the games
    by their private keys.
    """

    def setUp(self):

        logger.debug('BuyViewTest.setUp')

        self.client = Client()
        user = get_user()
        self.client.force_login(user)

        Game.create(title='title', url='url', developer=user).save()

    def testResponses(self):
        """Tests the response codes"""

        game = Game.objects.all()[0]
        pk = game.pk

        response = self.client.get(reverse('game:purchase', args=[pk]))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('game:purchase', args=[pk + 1]))
        self.assertEquals(response.status_code, 404)

class GameSearchTest(TestCase):
    """Tests the search function of the Game model.

    Given that these tests are implemented here, testing for which games a query finds
    on the views is unnessecary.
    """

    def setUp(self):

        logger.debug('GameSearchTest.setUp')
        user = get_user()
        for i in range(1, 8):
            title = ''
            title += 'foo ' if i & 1 == 1 else ''
            title += 'bar ' if i & 2 == 2 else ''
            title += 'baz ' if i & 4 == 4 else ''
            Game.create(title, '', developer=user).save()

        Game.create('game1', '', description='some description', developer=user).save()
        Game.create('game2', '', description='also some description', developer=user).save()
        Game.create('title', '', description='this game has a title', developer=user).save()
        Game.create('another game', '', description='this game also has a title', developer=user).save()

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

class SearchViewTest(TestCase):
    """Tests for the search view.

    Given that the searching functionality is implemented on the Game model, and
    tested by GameSearchTest, this class does not test the specific responses of the
    search function.
    """

    def setUp(self):

        logger.debug('SearchViewTest.setUp')

        self.client = Client()
        user = get_user()

        for i in range(0, 30):
            Game.create('game title {0}'.format(i), '', developer=user).save()

    def testEmptyResult(self):
        """Tests template rendering for an empty queryset."""

        response = self.client.get(reverse('game:search'), {'q': 'foo'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count(
            b'No games matched your search query!'
        ), 1)

    def testPaging(self):
        """Tests the number of reponses shown on a given page."""

        response = self.client.get(reverse('game:search'), {'q': 'game', 'p': '1'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count(b'game title'), 20)

        response = self.client.get(reverse('game:search'), {'q': 'game', 'p': '2'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count(b'game title'), 10)

        response = self.client.get(reverse('game:search'), {'q': 'game', 'p': '3'})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content.count(b'game title'), 0)

    def testFailResponses(self):
        """Tests the fail conditions."""

        response = self.client.get(reverse('game:search'), {'q': 'game', 'p': 0})
        self.assertEquals(response.status_code, 400)

class GameUploadTest(TestCase):
    """Tests for the upload feature.
    """

    def setUp(self):
        logger.debug('GameUploadTest.setUp')
        self.client = Client()

        group, created = Group.objects.get_or_create(name='Developer')
        user = User.objects.create()
        user.save()
        group.user_set.add(user)

        self.client.force_login(user)

    def testUpload(self):
        """Test that uploading works.
        """

        response = self.client.post(reverse('game:upload'), {
            'title': 'somegame',
            'url': 'http://google.com',
            'price': '0.50',
            'description': 'This here is a game',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Upload successful!' in response.content)

        qset = Game.objects.all().filter(title='somegame')
        self.assertTrue(len(qset) == 1)
        game = qset[0]
        self.assertEquals(game.url, 'http://google.com')
        self.assertEquals(str(game.price), '0.5')
        self.assertEquals(game.description, 'This here is a game')

    def testValidation(self):
        """This tests that the validation in the upload view  works.

        Tests only the case that two games with the same title are uploaded.
        """
        response = self.client.post(reverse('game:upload'), {
            'title': 'somegame',
            'url': 'http://google.com',
            'price': '0.50',
            'description': 'This here is a game',
        })

        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Upload successful!' in response.content)

        response = self.client.post(reverse('game:upload'), {
            'title': 'somegame',
            'url': 'http://google.com',
            'price': '0.50',
            'description': 'This game has the same title as the last one',
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['location'], reverse('game:upload'))

        response = self.client.get(response['location'])
        self.assertEquals(response.status_code, 200)
        self.assertTrue(b'Game with this Title already exists.' in response.content)

class GameRatingTest(TestCase):
    
    def setUp(self):
        logger.debug('game.GameRatingTest.setUp')
        self.client = Client()
        
        for i in range(1, 5):
            user = User.objects.create()
            user.username = 'user' + str(i)
            user.save()
        
        for i in range(1, 5):
            Game.create(
                title='game' + str(i),
                url='http://google.com',
                developer=user
            ).save()
        
        for i in range(1, 5):
            user = User.objects.get(username='user' + str(i))
            for j in range(i, 5):
                g = Game.objects.get(title='game' + str(j))
                buy_game = GamePlayed.objects.create(gameScore=0)
                buy_game.game = g
                buy_game.game.increment_sellcount()
                buy_game.save()
                PaymentDetail.objects.create(game_played=buy_game, cost=buy_game.game.price, user=user)
    
    def testResponses(self):
        user = User.objects.get(username='user2')
        self.client.force_login(user)
        
        #test negative responses
        game = Game.objects.get(title='game1')
        response = self.client.post(reverse('game:rate', args=[game.pk]), {
            'rating': 3
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('game:rate', args=[10]), {
            'rating': 3
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        game = Game.objects.get(title='game2')
        response = self.client.post(reverse('game:rate', args=[game.pk]), {
            'rating': 3
        })
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('game:rate', args=[game.pk]), {})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('game:rate', args=[game.pk]), {
            'rating': 'foobar'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        response = self.client.post(reverse('game:rate', args=[game.pk]), {
            'rating': 7
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        
        response = self.client.post(reverse('game:rate', args=[game.pk]), {
            'rating': 3
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'3')
        game.refresh_from_db()
        self.assertEqual(game.ratings, 1)
        self.assertEqual(game.total_rating, 3)
    
    #def testRatings(self):
    #    pass
