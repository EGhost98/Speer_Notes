from django.test import TestCase
from users.models import UserData
from notes.models import Note
from django.contrib.postgres.search import SearchVectorField, SearchVector

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = UserData.objects.create(name='testuser', email='testuser@example.com', password='testpassword')
        self.note_data = {
            'user': self.user,
            'title': 'Test Note',
            'content': 'This is a test note.',
            'public': False,
        }

    def test_note_creation(self):
        note = Note.objects.create(**self.note_data)
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note.')
        self.assertFalse(note.public)
        self.assertEqual(note.user, self.user)
        self.assertEqual(note.search_vector, None)

    def test_note_str_representation(self):
        note = Note.objects.create(**self.note_data)
        self.assertEqual(str(note), 'Test Note')

    def test_shared_notes(self):
        shared_user = UserData.objects.create(name='shareduser', email='shareduser@example.com', password='sharedpassword')
        note = Note.objects.create(**self.note_data)
        note.shared_with.add(shared_user)
        self.assertIn(note, shared_user.shared_notes.all())