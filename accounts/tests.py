from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from .forms import RegisterForm


class RegistrationFormTest(TestCase):
    """Tests if the registration form is valid or not. The valid registration forms are:
    1. Checks email field
    2. Checks if password is same (and make sure password from the validators in settings is met)
    3. Username doesnot already exists etc.
    """
    def setUp(self):
        """Set up form testing"""
        user = User.objects.create_user(username='testuser1', password='password1')
        player = Group.objects.create(name='Player')
        developer = Group.objects.create(name='Developer')

    def testValidRegistrationForm(self):
        """Tests if the form is valid"""
        data = {'username': 'gamehub', 'is_active':True, 'password1': 'VeryStrong', 'password2': 'VeryStrong', 'group': 1, 'email': 'info@gamehub.com', 'image': None, 'nickname': 'tuser3', 'description':'Awesome'}
        upload_image = open('/home/agapios/Desktop/gameHub/media_cdn/5214014-game-images.png', 'rb')
        image = {'file': SimpleUploadedFile(upload_image.name, upload_image.read())}
        form = RegisterForm(data, image)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def testInvalidRegistrationForm(self):
        """Tests if the form is invalid"""
        data = {'username': 'gamehub', 'password1': 'VeryStrong', 'password2': 'Verystrong', 'group': 1, 'email': 'info@gamehub.com'}
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())

class TemplateTestCase(TestCase):
    """Tests the template using django client"""
    def setUp(self):
        """Set up template test"""
        self.client = Client()
        user = User.objects.create_user(username='testuser2', password='password2')
        player = Group.objects.create(name='Player')
        developer = Group.objects.create(name='Developer')

    def testInvalidUrl(self):
        """Tests if invalid url returns 404"""
        response = self.client.get('/login_invalid_url')
        self.assertEquals(response.status_code, 404, "Requesting a page with an invalid country code.")

    def testValidLogin(self):
        response = self.client.post(reverse('accounts:login'), {'username': 'testuser2', 'password': 'password2'}, follow=True)
        self.assertEquals(response.status_code, 200, "Login with user name password and redirects to home")

    def testRegistration(self):
        """Checks if developer is registered and in particular group"""
        data = {'username': 'testuser3', 'is_active': True, 'password1': 'password3', 'password2': 'password3', 'group': 1, 'email': 'game@gamehub.com'}
        response = self.client.post(reverse('accounts:register'), data)
        group = Group.objects.get(name='Player')
        self.assertTrue(group.user_set.filter(username='testuser3').exists())
    #
    # def testGroupRegistration(self):
    #     res = self.client.post(reverse('accounts:login'), {'username': 'testuser3', 'password': 'password3'}, follow=True)
    #     response = self.client.post('/accounts/choosegroup', {'group': 0})
    #     print (response)
