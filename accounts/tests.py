from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate
from tasktopia.settings import *

# Override default DATABASES setting
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
class AccountViewTests(TestCase):
    """
    Functional tests for the account views. These tests simulate user interactions
    with the application and verify that the views behave as expected.
    """

    def setUp(self):
        """
        Set up the test environment. Create a test user and initialize the client.
        """
        self.user = User.objects.create_user(
            username='testuser', password='testpassword', email='test@example.com', first_name='Test', last_name='User'
        )
        self.client = Client()

    def test_index_view(self):
        """
        Test the index view. Verify that it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/index.html')

    def test_login_view(self):
        """
        Test the login view. Verify that it handles GET and POST requests correctly,
        including login success and failure scenarios.
        """
        # Test the login view GET request
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

        # Test the login view POST request with correct credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('task_list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Successfully logged in.' in str(message) for message in messages))

        # Test the login view POST request with incorrect credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertRedirects(response, reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Invalid credentials.' in str(message) for message in messages))

    def test_logout_view(self):
        """
        Test the logout view. Verify that it logs the user out and redirects to the index page.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully logged out' in str(message) for message in messages))

    def test_signup_view(self):
        """
        Test the signup view. Verify that it handles GET and POST requests correctly,
        including signup success and validation errors.
        """
        # Test the signup view GET request
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

        # Test the signup view POST request with valid data
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Successfully signed up.' in str(message) for message in messages))

    def test_profile_view(self):
        """
        Test the profile view. Verify that it is accessible only to logged-in users and uses the correct template.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile.html')

    def test_profile_edit_view(self):
        """
        Test the profile edit view. Verify that it handles GET and POST requests correctly,
        including profile update success and validation errors.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile_edit.html')

        # Test the profile edit view POST request with valid data
        response = self.client.post(reverse('profile_edit'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertRedirects(response, reverse('task_list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Profile successfully updated.' in str(message) for message in messages))

    def test_delete_account_view(self):
        """
        Test the delete account view. Verify that it handles GET and POST requests correctly,
        including account deletion success and password validation errors.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/delete_account.html')

        # Test the delete account view POST request with correct password
        response = self.client.post(reverse('delete_account'), {'password': 'testpassword'})
        self.assertRedirects(response, reverse('index'))
        self.assertFalse(User.objects.filter(username='testuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('account (testuser) has been deleted.' in str(message) for message in messages))

        # Test the delete account view POST request with incorrect password
        self.user = User.objects.create_user(username='testuser2', password='testpassword2', email='test2@example.com')
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(reverse('delete_account'), {'password': 'wrongpassword'})
        self.assertRedirects(response, reverse('delete_account'))
        self.assertTrue(User.objects.filter(username='testuser2').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Incorrect password. Account not deleted.' in str(message) for message in messages))

    def test_password_change_view(self):
        """
        Test the password change view. Verify that it handles GET and POST requests correctly,
        including password change success and validation errors.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

        # Test the password change view POST request with valid data
        response = self.client.post(reverse('password_change'), {
            'old_password': 'testpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        })
        self.assertRedirects(response, reverse('password_change_done'))
        user = authenticate(username='testuser', password='newpassword')
        self.assertIsNotNone(user)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Your password was successfully updated' in str(message) for message in messages))

        # Test the password change view POST request with incorrect old password
        response = self.client.post(reverse('password_change'), {
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword',
            'new_password2': 'newpassword',
        })
        self.assertFormError(response, 'form', 'old_password', 'Your old password was entered incorrectly. Please enter it again.')
