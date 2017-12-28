from django.db import models

# Create your models here.

class Game(models.Model):
    
    name        = models.TextField()
    url         = models.TextField()
    description = models.TextField()
    gameimage   = models.TextField()
