from rest_framework import viewsets
from rest_framework.response import Response

from verifyToken import verify_refresh_token, verify_refresh_token_and_superuser

from .serializer import BillHeaderSerializer, BillDetailSerializer
from .models import BillHeader, BillDetail
from authAPI.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt

class BillHeaderViewSet(viewsets.ModelViewSet):
    queryset = BillHeader.objects.all()
    serializer_class = BillHeaderSerializer

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
    def create(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request, request.data.get('user'))
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
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
    
class BillDetailViewSet(viewsets.ModelViewSet):
    queryset = BillDetail.objects.all()
    serializer_class = BillDetailSerializer

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
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING),
            openapi.Parameter('user_id', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def create(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request, request.query_params.get('user_id'))
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)
    
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
    def partial_update(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
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