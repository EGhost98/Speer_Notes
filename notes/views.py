from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from .models import UserData
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class NoteViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        operation_summary="List all notes of the user.",
        responses={
            status.HTTP_200_OK: "List of all notes of the user.",
        }
    )
    def list(self, request):
        queryset = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(queryset, many=True)
        return Response({'detail' : 'Notes Fetched Succesfully', 'Notes' : serializer.data }, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the note'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the note'),
            },
        ),
        operation_summary="Create a note.",
        responses={
            status.HTTP_201_CREATED: "Note created successfully.",
            status.HTTP_400_BAD_REQUEST: "Invalid data.",
        }
    )
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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        operation_summary="Retrieve a note.",
        responses={
            status.HTTP_200_OK : "Note retrieved successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to access this note.",
            status.HTTP_404_NOT_FOUND: "Note not found.",
        }
    )
    def retrieve(self, request, pk=None):
        try:
            instance = Note.objects.get(pk=pk)
            if instance.user == request.user or instance.public == True or request.user in instance.shared_with.all():
                serializer = NoteSerializer(instance)
                return Response({'detail': 'Note retrieved successfully', 'note': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You do not have permission to access this note."}, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Title of the note'),
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='Content of the note'),
            },
        ),
        operation_summary="Update a note.",
        responses={
            status.HTTP_200_OK: "Note updated successfully.",
            status.HTTP_400_BAD_REQUEST: "Invalid data.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to update this note.",
            status.HTTP_404_NOT_FOUND: "Note not found.",
        }
    )
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
        
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>')
        ],
        operation_summary="Delete a note.",
        responses={
            status.HTTP_204_NO_CONTENT: "Note deleted successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to delete this note.",
            status.HTTP_404_NOT_FOUND: "Note not found.",
        }
    )
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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user to share the note with'),
            },
        ),
        operation_summary="Share a note with a user",
        responses={
            status.HTTP_200_OK: "Note shared successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to share this note.",
            status.HTTP_404_NOT_FOUND: "Note not found or User with this email does not exist.",
        }
    )
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
            return Response({"detail": "Note not found or User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

class UnShareViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user to unshare the note with'),
            },
        ),
        operation_summary="Unshare a note with a user",
        responses={
            status.HTTP_200_OK: "Note unshared successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to unshare this note.",
            status.HTTP_404_NOT_FOUND: "Note not found or User with this email does not exist.",
        }
    )
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
            return Response({"detail": "Note not found or User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class MakePublicViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        operation_summary="Make a note public",
        responses={
            status.HTTP_200_OK: "Note made public successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to make this note public.",
            status.HTTP_404_NOT_FOUND: "Note not found.",
        }
    )
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        operation_summary="Make a note private",
        responses={
            status.HTTP_200_OK: "Note made private successfully.",
            status.HTTP_403_FORBIDDEN: "You do not have permission to make this note private.",
            status.HTTP_404_NOT_FOUND: "Note not found.",
        }
    )
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

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
            openapi.Parameter(
                'q', openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING
            )
        ],
        operation_summary="Search notes",
        responses={
            status.HTTP_200_OK: "List of notes matching the search query.",
            status.HTTP_400_BAD_REQUEST: "Invalid search query.",
        }
    )
    def search(self, request):
        search_query = request.query_params.get('q', '')
        if not search_query:
            return Response({"detail": "Invalid search query."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Note.objects.filter(
            user=request.user,
            search_vector=SearchVector('your_searchable_field_name')  # Replace with the actual field name
        ).annotate(
            rank=SearchRank(F('search_vector'), SearchQuery(search_query))
        ).order_by('-rank')

        serializer = NoteSerializer(queryset, many=True)
        return Response({'detail': 'List of notes matching the search query', 'notes': serializer.data}, status=status.HTTP_200_OK)