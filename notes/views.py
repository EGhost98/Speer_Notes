from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from .models import UserData
from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db.models import F

class NoteViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(queryset, many=True)
        return Response({'detail' : 'Notes Fetched Succesfully', 'Notes' : serializer.data }, status=status.HTTP_200_OK)

    def create(self, request):
        user =  request.user
        data = {
            'user': user.id,
            'title': request.data.get('title'),
            'content': request.data.get('content'),
        }
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail' : 'Note Created Succesfully', 'Note' : serializer.data }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user or instance.public == True or request.user in instance.shared_with.all():
                serializer = NoteSerializer(instance)
                return Response({'detail': 'Note fetched successfully', 'note': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You do not have permission to access this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        user = request.user
        try:
            instance = Note.objects.get(pk=pk)
            data = {
                'user': user.id,
                'title': request.data.get('title'),
                'content': request.data.get('content'),
            }
            if instance.user == request.user:
                serializer = NoteSerializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'detail' : 'Note Updated Succesfully', 'Note' : serializer.data }, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "You do not have permission to update this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        user = request.user
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user:
                instance.delete()
                return Response({"detail": "Note Deleted Succesully."}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "You do not have permission to delete this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

class ShareViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def share(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user:
                email = request.data.get('email')
                try:
                    user = UserData.objects.get(email=email)
                    instance.shared_with.add(user)
                    return Response({"detail": "Note shared successfully."}, status=status.HTTP_200_OK)
                except UserData.DoesNotExist:
                    return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "You do not have permission to share this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

class UnShareViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def unshare(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user:
                email = request.data.get('email')
                try:
                    user = UserData.objects.get(email=email)
                    instance.shared_with.remove(user)
                    return Response({"detail": "Note unshared successfully."}, status=status.HTTP_200_OK)
                except UserData.DoesNotExist:
                    return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "You do not have permission to unshare this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
        
class MakePublicViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def make_public(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user:
                instance.public = True
                instance.save()
                return Response({"detail": "Note made public successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You do not have permission to make this note public."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
        
class MakePrivateViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def make_private(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user:
                instance.public = False
                instance.save()
                return Response({"detail": "Note made private successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You do not have permission to make this note private."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

class SearchViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def search(self, request):
        search_query = request.query_params.get('q', '')
        queryset = Note.objects.filter(
            user=request.user,
            search_vector=SearchQuery(search_query)
        ).annotate(
            rank=SearchRank(F('search_vector'), SearchQuery(search_query))
        ).order_by('-rank')

        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)