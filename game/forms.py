from django.form import ModelForm
from .models import Game

class UploadGameForm(ModelForm):
    
    class Meta:
        
        model = Game
        fields = ('name', 'url', 'price', 'description', 'gameimage')
