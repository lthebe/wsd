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
        self.assertEquals(len(content), 8)
        print(response.content)

# Create your tests here.
