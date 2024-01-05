from django.db import models
from users.models import UserData
from django.contrib.postgres.search import SearchVectorField, SearchVector

class Note(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    public = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(UserData, related_name='shared_notes', blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Note.objects.filter(pk=self.pk).update(search_vector=(
            SearchVector('title', weight='A') +
            SearchVector('content', weight='B')
        ))