import logging

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.utils.six import BytesIO

from rest_framework.test import APIClient
from rest_framework.parsers import JSONParser

from game.models import Game

logger = logging.getLogger(__name__)

class UsersTest(TestCase):
    
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
