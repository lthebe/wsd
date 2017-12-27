from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Requried a valid email')
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'group', 'password1', 'password2')

class GroupChoiceForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
