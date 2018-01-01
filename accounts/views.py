from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.core import signing
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.views import View


from .forms import RegisterForm, GroupChoiceForm
from game.models import Game
# Create your views here.

class RegisterView(CreateView):
    """Registration of the user - custom form to include the group selection"""
    model = User
    form_class = RegisterForm
    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.image = form.cleaned_data.get('image')
            user.profile.description = form.cleaned_data.get('description')
            user.profile.nickname = form.cleaned_data.get('nickname')
            group = Group.objects.get(name=form.cleaned_data.get('group'))
            group.user_set.add(user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account in GameHub'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': signing.dumps({'id': user.id}),
                'expiry': settings.ACTIVATION_TIME
            })
            user.email_user(subject, message)
            messages.add_message(request, messages.INFO, 'Please activate your account and login!')
            return redirect('accounts:login')
        else:
            return render(request, template_name='accounts/register.html', context={'form': form })
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            form = RegisterForm()
            return render(request, template_name='accounts/register.html', context={'form': form})

class ActivationView(View):
    def get(self, request, token):
        try:
            id_dict = signing.loads(token, max_age=settings.ACTIVATION_TIME)
            id = id_dict['id']
            user = User.objects.get(pk=id)
        except:
            user = None
        if user is not None:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:home')
        else:
            return render(request, 'accounts/activation_error.html')

def home_view(request):
    """Returns the home page of the site"""
    games = Game.objects.all()[:3] #you can make it render the top games in home page for example
    return render(request, template_name='gamehub/home.html', context={'games': games})

def pick_group(request):
    """Pick the group for the user - either developer or player.
    A user will have only one group"""
    if request.method == 'POST':
        form = GroupChoiceForm(request.POST)
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            if len(request.user.groups.all()) >= 1:
                messages.add_message(request, messages.INFO, 'You already belong to a group!')
                return redirect('accounts:home')
            request.session['user_group'] = str(form.cleaned_data['group'])
            # once we have the password stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            return redirect(reverse('social:complete', args=["google-oauth2"]))
    else:
        form = GroupChoiceForm()
    return render(request, "accounts/pick_group.html", context={'form': form})
