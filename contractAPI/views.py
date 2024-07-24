from rest_framework import viewsets
from rest_framework.response import Response

from .serializer import ContractSerializer
from .models import Contract
from authAPI.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def verify_refresh_token_and_superuser(self, request):
        refresh = request.query_params.get('refresh')
        if not refresh:
            return Response({'error': 'Refresh token is required'}, status=400)

        try:
            payload = jwt.decode(refresh, options={"verify_signature": False})
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            if not user:
                return Response({'error': 'Invalid refresh token'}, status=400)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)

        if not user.is_superuser:
            return Response({'error': 'Access denied. Only superusers can access this resource.'}, status=403)
        
        return None

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().destroy(request, *args, **kwargs)