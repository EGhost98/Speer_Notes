from rest_framework import routers
from .views import NoteViewSet, ShareViewSet, UnShareViewSet, MakePublicViewSet, MakePrivateViewSet, SearchViewSet
from django.urls import path, include

notes_router = routers.DefaultRouter()
notes_router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(notes_router.urls)),
    path('notes/<pk>/share/', ShareViewSet.as_view({'post': 'share'}), name='share-note'),
    path('notes/<pk>/unshare/', UnShareViewSet.as_view({'post': 'unshare'}), name='unshare-note'),
    path('notes/<pk>/make-public/', MakePublicViewSet.as_view({'post': 'make_public'}), name='make-public-note'),
    path('notes/<pk>/make-private/', MakePrivateViewSet.as_view({'post': 'make_private'}), name='make-private-note'),
    path('search/', SearchViewSet.as_view({'get': 'search'}), name='search-notes'),
]

