from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
            },
            required=['username', 'password'],
        ),
        operation_summary="Get Access and Refresh Tokens",
        responses={
            200: 'Successfully retrieved access and refresh tokens',
            401: 'Invalid credentials',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class CustomTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Your refresh token'),
            },
            required=['refresh'],
        ),
        operation_summary="Refresh Access Token",
        responses={
            200: 'Successfully retrieved a new access token',
            401: 'Invalid refresh token',
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description='Authorization header with Bearer token', type=openapi.TYPE_STRING, format=openapi.FORMAT_SLUG, default='Bearer <your_token_here>'),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Your refresh token'),
            },
            required=['refresh_token'],
        ),
        operation_summary="User Logout",
        responses={
            200: 'Successfully logged out',
            401: 'Invalid refresh token',
        },
    )
    def post(self, request):
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({'detail': 'User logged out successfully.'}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Your username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Your email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Your password'),
            },
            required=['username', 'email', 'password'],
        ),
        operation_summary="User Registration",
        responses={
            201: 'User created successfully',
            400: 'Bad Request: Invalid input data',
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': 'Bad Request: Invalid input data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)