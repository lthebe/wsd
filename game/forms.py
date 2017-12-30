from django.forms import ModelForm, TextInput
from .models import Game

class UploadGameForm(ModelForm):
    
    class Meta:
        model = Game
        fields = ('name', 'url', 'price', 'description', 'gameimage')
        widgets = {
            'name': TextInput,
        }
        labels = {
            'name': 'title',
        }
