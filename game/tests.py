from django.test import TestCase, Client
from django.urls import reverse

from game.models import Game

# Create your tests here.

class BuyViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        Game.create(name='name', url='url').save()
    
    def testResponses(self):
        
        game = Game.objects.all()[0]
        pk = game.pk
        
        response = self.client.get(reverse('game:buy', args=[pk]))
        self.assertEquals(response.status_code, 200)
        response = self.client.get(reverse('game:buy', args=[pk + 1]))
        self.assertEquals(response.status_code, 404)
