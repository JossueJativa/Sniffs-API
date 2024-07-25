from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import UserSerializer
from .models import User

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from verifyToken import verify_refresh_token, verify_refresh_token_and_superuser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request, kwargs.get('pk'))
        if error_response:
            return error_response
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request, kwargs.get('pk'))
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request, kwargs.get('pk'))
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'identity': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    def create(self, request):
        data = request.data
        fields_required = [
            'username',
            'password',
            'email',
            'phone',
            'identity'
        ]
        for field in fields_required:
            if field not in data:
                return Response({'error': 'Field {} is required'.format(field)}, status=400)
        data['password'] = make_password(data['password'])

        for field in fields_required:
            if User.objects.filter(**{field: data[field]}).exists():
                return Response({'error': 'Field {} already exists'.format(field)}, status=400)
            
        user = User.objects.create(**data)
        user.save()
        return Response({'success': 'User created successfully'}, status=201)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def login(self, request):
        data = request.data
        fields_required = [
            'username',
            'password'
        ]
        for field in fields_required:
            if field not in data:
                return Response({'error': 'Field {} is required'.format(field)}, status=400)
        
        try:
            if '@' in data['username']:
                user = User.objects.filter(email=data['username']).first()
                username = user.username # type: ignore
            elif data['username'].isdigit():
                user = User.objects.filter(phone=data['username']).first()
                username = user.username # type: ignore
            else:
                user = User.objects.filter(username=data['username']).first()
                username = data['username']
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=400)

        user = authenticate(username=username, password=data['password'])
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)  # type: ignore
        })
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'refresh': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        id = request.data.get('user_id') or request.query_params.get('user_id')
        error_response = verify_refresh_token(request, id)
        if error_response:
            return error_response
        
        data = request.data
        fields_required = [
            'user_id',
            'refresh'
        ]
        for field in fields_required:
            if field not in data:
                return Response({'error': 'Field {} is required'.format(field)}, status=400)
        
        user = User.objects.filter(id=data['user_id']).first()
        if user is None:
            return Response({'error': 'Invalid user'}, status=400)
        
        try:
            refresh = RefreshToken(data['refresh'])
            refresh.blacklist()
        except:
            return Response({'error': 'Invalid refresh token'}, status=400)
        return Response({'success': 'Logout successfully'}, status=200)