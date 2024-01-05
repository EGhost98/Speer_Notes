from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import UserData
from notes.models import Note

class ShareViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.share_url = reverse('share-note', args=[self.note.id])

    def test_share_note(self):
        other_user = UserData.objects.create_user(name='otheruser', email='otheruser@example.com', password='otherpassword')
        data = {'email': other_user.email}
        response = self.client.post(self.share_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Note shared successfully', str(response.data))

    def test_share_note_invalid_user(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.share_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User with this email does not exist', str(response.data))

    def test_share_note_permission_denied(self):
        unauthorized_user = UserData.objects.create_user(name='unauthorized', email='unauthorized@example.com', password='unauthorizedpassword')
        self.client.force_authenticate(user=unauthorized_user)
        data = {'email': self.user.email}
        response = self.client.post(self.share_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UnShareViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.shared_user = UserData.objects.create_user(name='shareduser', email='shareduser@example.com', password='sharedpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.note.shared_with.add(self.shared_user)
        self.unshare_url = reverse('unshare-note', args=[self.note.id])

    def test_unshare_note(self):
        data = {'email': self.shared_user.email}
        response = self.client.post(self.unshare_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Note unshared successfully', str(response.data))

    def test_unshare_note_invalid_user(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.unshare_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User with this email does not exist', str(response.data))

    def test_unshare_note_permission_denied(self):
        unauthorized_user = UserData.objects.create_user(name='unauthorized', email='unauthorized@example.com', password='unauthorizedpassword')
        self.client.force_authenticate(user=unauthorized_user)
        data = {'email': self.shared_user.email}
        response = self.client.post(self.unshare_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MakePublicViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.make_public_url = reverse('make-public-note', args=[self.note.id])

    def test_make_note_public(self):
        response = self.client.post(self.make_public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Note made public successfully', str(response.data))

    def test_make_note_public_permission_denied(self):
        unauthorized_user = UserData.objects.create_user(name='unauthorized', email='unauthorized@example.com', password='unauthorizedpassword')
        self.client.force_authenticate(user=unauthorized_user)
        response = self.client.post(self.make_public_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MakePrivateViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
            'public': True,
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.make_private_url = reverse('make-private-note', args=[self.note.id])

    def test_make_note_private(self):
        response = self.client.post(self.make_private_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Note made private successfully', str(response.data))

    def test_make_note_private_permission_denied(self):
        unauthorized_user = UserData.objects.create_user(name='unauthorized', email='unauthorized@example.com', password='unauthorizedpassword')
        self.client.force_authenticate(user=unauthorized_user)
        response = self.client.post(self.make_private_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class SearchViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.search_url = reverse('search-notes')

    def test_search_notes(self):
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('List of notes matching the search query', str(response.data))

    def test_search_notes_empty_query(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid search query', str(response.data))
