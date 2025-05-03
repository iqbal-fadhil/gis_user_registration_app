from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.gis.geos import Point

from .models import UserProfile
from .forms import UserForm, UserProfileForm

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_model_test_user', password='testpassword')

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'user_model_test_user')

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profile_model_test_user', password='testpassword')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            home_address='123 Test Address',
            phone_number='081234567890',
            location=Point(107.6191, -6.9175, srid=4326) # Bandung coordinates
        )

    def test_user_profile_creation(self):
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.home_address, '123 Test Address')
        self.assertEqual(self.user_profile.phone_number, '081234567890')
        self.assertEqual(self.user_profile.location.wkt, 'POINT (107.6191 -6.9175)')

    def test_user_profile_str_method(self):
        self.assertEqual(str(self.user_profile), 'profile_model_test_user')

class UserFormTest(TestCase):
    def test_user_form_valid_data(self):
        form_data = {'first_name': 'Test', 'last_name': 'User', 'email': 'test@example.com'}
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_data(self):
        form_data = {'first_name': '', 'last_name': 'User', 'email': 'invalid-email'}
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('email', form.errors)

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='profile_form_test_user', password='testpassword')

    def test_user_profile_form_valid_data(self):
        form_data = {'home_address': '456 Another Address', 'phone_number': '089876543210', 'location': 'POINT(107.6098 -6.9250)'}
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = self.user
        profile.save()
        self.assertEqual(profile.home_address, '456 Another Address')
        self.assertEqual(profile.phone_number, '089876543210')
        self.assertEqual(profile.location.wkt, 'POINT (107.6098 -6.925)')

    def test_user_profile_form_no_location(self):
        form_data = {'home_address': 'No Location Address', 'phone_number': '081122334455', 'location': ''}
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = self.user
        profile.save()
        self.assertIsNone(profile.location)

    def test_user_profile_form_invalid_location_format(self):
        form_data = {'home_address': 'Invalid Location Address', 'phone_number': '082233445566', 'location': '10,20'}
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='views_test_user', password='testpassword')
        self.client.login(username='views_test_user', password='testpassword')
        self.profile = UserProfile.objects.create(user=self.user, location=Point(107.6, -6.9))

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

        # Test successful registration
        form_data = {'username': 'new_test_user', 'email': 'new@example.com', 'password': 'newpassword123', 'password2': 'newpassword123'}
        response = self.client.post(reverse('register'), form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('profile'))
        self.assertTrue(User.objects.filter(username='new_test_user').exists())

        # Test registration with password mismatch
        form_data = {'username': 'another_test_user', 'email': 'another@example.com', 'password': 'pass1', 'password2': 'pass2'}
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')
        self.assertFalse(User.objects.filter(username='another_test_user').exists())

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Test successful login
        form_data = {'username': 'views_test_user', 'password': 'testpassword'}
        response = self.client.post(reverse('login'), form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('profile'))

        # Test invalid login
        form_data = {'username': 'views_test_user', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_user_locations_map_view(self):
        response = self.client.get(reverse('user_locations_map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_locations_map.html')
        self.assertIn('profiles', response.context)
        self.assertEqual(len(response.context['profiles']), 1)
        self.assertEqual(response.context['profiles'][0]['user'], 'views_test_user')
        self.assertEqual(response.context['profiles'][0]['lat'], -6.9)
        self.assertEqual(response.context['profiles'][0]['lng'], 107.6)

    def test_custom_logout_view(self):
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_profile_view(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['lat'], -6.9)
        self.assertEqual(response.context['lng'], 107.6)

        # Test profile view when location is None
        self.profile.location = None
        self.profile.save()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.context['lat'], None)
        self.assertEqual(response.context['lng'], None)

    def test_edit_profile_view(self):
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')
        self.assertIsInstance(response.context['user_form'], UserForm)
        self.assertIsInstance(response.context['profile_form'], UserProfileForm)
        self.assertEqual(response.context['lat'], -6.9)
        self.assertEqual(response.context['lng'], 107.6)

        # Test successful profile edit
        form_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'home_address': 'Updated Address',
            'phone_number': '081111111111',
            'location': 'POINT(107.5 -7.0)'
        }
        response = self.client.post(reverse('edit_profile'), form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.profile.home_address, 'Updated Address')
        self.assertEqual(self.profile.location.wkt, 'POINT (107.5 -7.0)')

        # Test edit profile with invalid location
        form_data_invalid_location = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'home_address': 'Updated Address',
            'phone_number': '081111111111',
            'location': 'invalid'
        }
        response = self.client.post(reverse('edit_profile'), form_data_invalid_location)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'profile_form', 'location', 'Invalid location format.')

    def test_login_required_views(self):
        self.client.logout()
        login_required_urls = ['profile', 'edit_profile']
        for url_name in login_required_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('login') + '?next=' + reverse(url_name))