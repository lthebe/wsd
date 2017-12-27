from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from .forms import RegisterForm, GroupChoiceForm

# Create your views here.

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            group.user_set.add(user)
            login(request, user)
            return redirect('accounts:home')
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            form = RegisterForm()
            return render(request, template_name='accounts/register.html', context={'form': form})

def home_view(request):
    return render(request, template_name='gamehub/home.html')

def pick_group(request):
    if request.method == 'POST':
        form = GroupChoiceForm(request.POST)
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            if len(request.user.groups.all())<=1:
                #add message that you are allowed only a group
                return redirect('accounts:home')
            request.session['user_group'] = str(form.cleaned_data['group'])
            # once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            return redirect(reverse('social:complete', args=["google-oauth2"]))
    else:
        form = GroupChoiceForm()
    return render(request, "accounts/pick_group.html", context={'form': form})
