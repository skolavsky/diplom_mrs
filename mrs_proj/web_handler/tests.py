from django.test import TestCase, Client
from django.contrib.auth.models import User


class WebHandlerViewsTest(TestCase):

    def setUp(self):
        # Тестовый юзер
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test client
        self.client = Client()

    def test_login_view(self):
        # Test the GET request to the login view
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

        # Test the POST request to the login view with valid credentials
        response = self.client.post('/login/',
                                    {'action': 'login', 'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)  # Expect a redirect status code

        # Test the POST request to the login view with invalid credentials
        response = self.client.post('/login/',
                                    {'action': 'login', 'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid login credentials')

    def test_contacts_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test the GET request to the contacts view
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')

    def test_home_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test the GET request to the home view
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_dashboard_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test the GET request to the dashboard view
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
