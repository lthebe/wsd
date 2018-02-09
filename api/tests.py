import logging

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.six import BytesIO

from rest_framework.test import APIClient
from rest_framework.parsers import JSONParser

from game.models import Game, GamePlayed, PaymentDetail
from game.models_helper import buy_game_for_user

logger = logging.getLogger(__name__)

class UsersTest(TestCase):
    """Test querying of users and developers
    """
    
    def setUp(self):
        
        logger.debug('UsersTest.setUp')
        
        self.parser = JSONParser()
        self.client = APIClient()
        
        dev_group = Group.objects.get(name='Developer')
        ply_group = Group.objects.get(name='Player')
        
        for i in range(3):
            user = User.objects.create(username='dev{}'.format(i))
            user.save()
            dev_group.user_set.add(user)
        
        for i in range(5):
            user = User.objects.create(username='ply{}'.format(i))
            user.save()
            ply_group.user_set.add(user)
    
    def testUserList(self):
        
        response = self.client.get(reverse('api:user-list'), None, format='json')
        self.assertEquals(response.status_code, 200)
        
        content = self.parser.parse(BytesIO(response.content))
        
        got_users = {user['username'] for user in content}
        has_users = {user.username for user in User.objects.all()}
        self.assertTrue(got_users == has_users)
        
    def testDeveloperList(self):
        
        response = self.client.get(reverse('api:developer-list'), None, format='json')
        self.assertEquals(response.status_code, 200)
        
        content = self.parser.parse(BytesIO(response.content))
        
        got_users = {user['username'] for user in content}
        has_users = {user.username for user in
            Group.objects.get(name='Developer').user_set.all()
        }
        self.assertTrue(got_users == has_users)
        
        #self.assertEquals(len(content), 3)
        #
        #developer_list = list(map(
        #    lambda user: user.username,
        #    Group.objects.get(name='Developer').user_set.all()
        #))
        #for user in content:
        #    self.assertTrue(user['username'] in developer_list)

class DevelopedGamesTest(TestCase):
    """Tests the querying of games, and information from the developers.
    """
    
    def setUp(self):
        
        logger.debug('DeveloperGamesTest.setUp')
        
        self.parser = JSONParser()
        self.client = APIClient()
        
        dev_group = Group.objects.get(name='Developer')
        
        for i in range(4):
            user = User.objects.create(username='dev{}'.format(i))
            user.save()
            dev_group.user_set.add(user)
        
        for i in range(4):
            developer = User.objects.get(username='dev{}'.format(i))
            for j in range(i):
                Game.create(
                    title='game{}x{}'.format(i, j),
                    url='http://foobar.fi',
                    developer=developer
                ).save()
    
    def testGamesList(self):
        
        response = self.client.get(reverse('api:game-list'), None, format='json')
        self.assertEquals(response.status_code, 200)
        
        content = self.parser.parse(BytesIO(response.content))
        
        got_games = {(game['title'], game['developer']) for game in content}
        has_games = {
            (game.title, game.developer.username)
            for game in Game.objects.all()
        }
        self.assertTrue(got_games == has_games)
    
    def testDevelopedGamesList(self):
        
        for developer in Group.objects.get(name='Developer').user_set.all():
            response = self.client.get(
                reverse('api:developer-games', args=[developer.username]),
                None, format='json'
            )
            self.assertEquals(response.status_code, 200)
            
            content = self.parser.parse(BytesIO(response.content))
            
            got_games = {game['title'] for game in content}
            has_games = {
                game.title for game in Game.objects.all().filter(developer=developer)
            }
            
            self.assertTrue(got_games == has_games)

class BoughtGamesTest(TestCase):
    """Tests the querying of games bought by users and the lists of buyers by game.
    """
    
    def setUp(self):
        
        logger.debug('BoughtGamesTest.setUp')
        
        self.parser = JSONParser()
        self.client = APIClient()
        
        dev_group = Group.objects.get(name='Developer')
        ply_group = Group.objects.get(name='Player')
        
        developer = User.objects.create(username='dev')
        developer.save()
        dev_group.user_set.add(developer)
        
        for i in range(3):
            user = User.objects.create(username='ply{}'.format(i))
            user.save()
            ply_group.user_set.add(user)
        
        for i in range(4):
            game = Game.create(
                title='game{}'.format(i),
                url='http://foobar.fi',
                developer=developer
            )
            game.save()
            
            for j in range(i):
                user = User.objects.get(username='ply{}'.format(j))
                buy_game_for_user(user, game)
    
    def testUserGameList(self):
        
        for user in Group.objects.get(name='Player').user_set.all():
            response = self.client.get(
                reverse('api:user-games', args=[user.username]),
                None, format='json'
            )
            self.assertEquals(response.status_code, 200)
            
            content = self.parser.parse(BytesIO(response.content))
            
            got_games = {game['game'] for game in content}
            has_games = {
                gameplayed.game.title for gameplayed in user.gameplayed_set.all()
            }
            
            self.assertTrue(got_games == has_games)
    
    def testGameBuyersList(self):
        
        for game in Game.objects.all():
            response = self.client.get(
                reverse('api:game-buyers', args=[game.title]),
                None, format='json'
            )
            self.assertEquals(response.status_code, 200)
            
            content = self.parser.parse(BytesIO(response.content))
            
            got_buyers = {user['user'] for user in content}
            has_buyers = {
                gameplayed.user.username
                for gameplayed in game.gameplayed_set.all()
            }
            
            self.assertTrue(got_buyers == has_buyers)


class SortByTest(TestCase):
    """Tests the sorting feature of the api views. Only a few views and sorting
    options are tested.
    
    The two tests currently are selected since the implementation of these sorting
    methods are significantly different. The implementation of sorting for other
    views are fairly similar to these two methods.
    """
    
    def setUp(self):
        
        logger.debug('SortByTest.setUp')
        
        self.client = APIClient()
        self.parser = JSONParser()
        
        dev_group = Group.objects.get(name='Developer')
        ply_group = Group.objects.get(name='Player')
        
        developer = User.objects.create(username='dev')
        developer.save()
        dev_group.user_set.add(developer)
        
        for i in range(4):
            user = User.objects.create(username='ply{}'.format(i))
            user.save()
            ply_group.user_set.add(user)
        
        for i in range(4):
            game = Game.create(
                title='game{}'.format(i),
                url='http://foobar.fi',
                developer=developer,
                price=0.5*i
            )
            game.save()
            
            for user in ply_group.user_set.all():
                buy_game_for_user(user, game)
    
    def testGameRevenue(self):
        """Tests sorting by revenue.
        """
        
        response = self.client.get(
            reverse('api:game-list'),
            {'order_by': 'revenue'},
            format='json'
        )
        self.assertEquals(response.status_code, 200)
        content = self.parser.parse(BytesIO(response.content))
        for i in range(4):
            self.assertEquals(content[i]['title'], 'game{}'.format(i))
        
        response = self.client.get(
            reverse('api:game-list'),
            {'order_by': '-revenue'},
            format='json'
        )
        self.assertEquals(response.status_code, 200)
        content = self.parser.parse(BytesIO(response.content))
        for i in range(4):
            self.assertEquals(content[i]['title'], 'game{}'.format(3 - i))
    
    def testHighscore(self):
        """Test sorting by game score.
        """
        
        game = Game.objects.get(title='game0')
        gameplayeds = game.gameplayed_set
        ply_group = Group.objects.get(name='Player')
        for i in range(4):
            user = ply_group.user_set.get(username='ply{}'.format(i))
            gameplayed = gameplayeds.get(user=user)
            gameplayed.gameScore = i
            gameplayed.save()
        
        response = self.client.get(
            reverse('api:game-buyers', args=['game0']),
            {'order_by': 'gameScore'},
            format='json'
        )
        self.assertEquals(response.status_code, 200)
        content = self.parser.parse(BytesIO(response.content))
        for i in range(4):
            self.assertEquals(content[i]['user'], 'ply{}'.format(i))
        
        response = self.client.get(
            reverse('api:game-buyers', args=['game0']),
            {'order_by': '-gameScore'},
            format='json'
        )
        self.assertEquals(response.status_code, 200)
        content = self.parser.parse(BytesIO(response.content))
        for i in range(4):
            self.assertEquals(content[i]['user'], 'ply{}'.format(3 - i))
