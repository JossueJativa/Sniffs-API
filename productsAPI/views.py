from rest_framework import viewsets
from rest_framework.response import Response

from verifyToken import verify_refresh_token_and_superuser

from .serializer import ProductSerializer
from .models import Product
from authAPI.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
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
    def destroy(self, request, *args, **kwargs):
        error_response = verify_refresh_token_and_superuser(request)
        if error_response:
            return error_response
        return super().destroy(request, *args, **kwargs)
    
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