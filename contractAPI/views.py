from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from verifyToken import verify_refresh_token

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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING),
            openapi.Parameter('user_id', openapi.IN_QUERY, description="ID of the contract", type=openapi.TYPE_INTEGER)
        ]
    )
    @action(detail=False, methods=['get'])
    def getContractByUserId(self, request):
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=400)
        
        try:
            user_id = int(user_id)
        except:
            return Response({'error': 'Invalid user ID'}, status=400)
        
        contracts = Contract.objects.filter(user_id=user_id)
        data = []
        # Enviar la fecha de inicio y fin, estado, total y el id del contrato
        for contract in contracts:
            data.append({
                'id': contract.id, # type: ignore
                'start_date': contract.date_start, # type: ignore
                'end_date': contract.date_end, # type: ignore
                'status': contract.status,
                'total': contract.product.price,
                'description': contract.product.name
            })
        return Response(data)