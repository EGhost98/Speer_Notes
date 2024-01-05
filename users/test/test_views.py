from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserData as User

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('sign-up')
        self.login_url = reverse('token-obtain-pair')
        self.refresh_url = reverse('token-refresh')
        self.logout_url = reverse('logout')

        self.user_data = {
            'name': 'testuser',
            'email': 'testuser@gmail.com',
            'password': 'testpassword',
        }

    def test_registration(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_registration(self):
        invalid_data = {
            'name': '',
            'email': 'invalid_email',
            'password': 'short',
        }
        response = self.client.post(self.register_url, data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        self.client.post(self.register_url, data=self.user_data)
        response = self.client.post(self.login_url, data={'email': self.user_data['email'], 'password': self.user_data['password']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_login(self):
        self.client.post(self.register_url, data=self.user_data)
        invalid_credentials = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data=invalid_credentials)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        self.client.post(self.register_url, data=self.user_data)
        response = self.client.post(self.login_url, data={'email': self.user_data['email'], 'password': self.user_data['password']})
        refresh_token = response.data['refresh']
        response = self.client.post(self.refresh_url, data={'refresh': str(refresh_token)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)