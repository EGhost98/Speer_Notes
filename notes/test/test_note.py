from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import UserData
from notes.models import Note

class NoteViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserData.objects.create_user(name='testuser', email='testuser@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.note_data = {
            'title': 'Test Note',
            'content': 'This is a test note.',
        }
        self.note = Note.objects.create(user=self.user, **self.note_data)
        self.note_url = reverse('note-detail', args=[self.note.id])

    def test_list_notes(self):
        response = self.client.get(reverse('note-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Notes Fetched Successfully', response.data['detail'])

    def test_create_note(self):
        response = self.client.post(reverse('note-list'), data=self.note_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Note Created Successfully', response.data['detail'])

    def test_retrieve_note(self):
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Note retrieved successfully', response.data['detail'])

    def test_update_note(self):
        updated_data = {
            'title': 'Updated Test Note',
            'content': 'Updated content.',
        }
        response = self.client.put(self.note_url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Note Updated Successfully', response.data['detail'])

    def test_delete_note(self):
        response = self.client.delete(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('Note Deleted Successfully.', response.data['detail'])

    def test_permission_denied_update(self):
        other_user = UserData.objects.create_user(name='otheruser', email='otheruser@example.com', password='otherpassword')
        self.client.force_authenticate(user=other_user)
        updated_data = {
            'title': 'Updated Test Note',
            'content': 'Updated content.',
        }
        response = self.client.put(self.note_url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_denied_delete(self):
        other_user = UserData.objects.create_user(name='otheruser', email='otheruser@example.com', password='otherpassword')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_note_not_found(self):
        invalid_note_url = reverse('note-detail', args=[999])
        response = self.client.get(invalid_note_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
