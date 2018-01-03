from django.forms import ModelForm, TextInput
from .models import Game

class UploadGameForm(ModelForm):

    class Meta:
        model = Game
        fields = ('title', 'url', 'price', 'description', 'gameimage')
        widgets = {
            'title': TextInput,
        }
