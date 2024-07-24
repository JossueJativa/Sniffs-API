from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializer import CommentSerializer

from .models import Comment

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token(request)
        if error_response:
            return error_response
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token(request)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        error_response = self.verify_refresh_token(request)
        if error_response:
            return error_response
        return super().destroy(request, *args, **kwargs)

    def verify_refresh_token(self, request):
        refresh_token = request.query_params.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=400)
        return None