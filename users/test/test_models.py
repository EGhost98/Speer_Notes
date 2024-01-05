from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import UserData

class UserModelTest(TestCase):

    def test_create_user(self):
        """Test creating a new user"""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'Test User'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a new superuser"""
        email = 'admin@example.com'
        password = 'adminpass123'
        name = 'Admin User'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password,
            name=name
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_str_representation(self):
        """Test string representation of the user model"""
        email = 'test@example.com'
        name = 'Test User'
        user = get_user_model().objects.create_user(
            email=email,
            password='testpass123',
            name=name
        )
        self.assertEqual(str(user), email)
