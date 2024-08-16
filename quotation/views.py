from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from verifyToken import verify_refresh_token, verify_refresh_token_and_superuser

from .serializer import QuotationHeaderSerializer, QuotationDetailSerializer
from .models import QuotationHeader, QuotationDetail
from authAPI.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt

class QuotationHeaderViewSet(viewsets.ModelViewSet):
    queryset = QuotationHeader.objects.all()
    serializer_class = QuotationHeaderSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request)
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
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)
    
    # List
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        return super().list(request, *args, **kwargs)
    
class QuotationDetailViewSet(viewsets.ModelViewSet):
    queryset = QuotationDetail.objects.all()
    serializer_class = QuotationDetailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        print(request.data)
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        error_response = verify_refresh_token(request)
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
        error_response = verify_refresh_token(request)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING),
            openapi.Parameter('id', openapi.IN_QUERY, description="Quotation Header ID", type=openapi.TYPE_INTEGER)
        ]
    )
    @action(detail=False, methods=['GET'])
    def getDetailsHeader(self, request):
        try:
            id = request.query_params.get('id')
            header = QuotationHeader.objects.get(id=id)
            details = QuotationDetail.objects.filter(header=header)
            # Devolver: id, nombreProducto, cantidad, precioAparato, precioMensual, mesesAContratar
            response = []
            for detail in details:
                response.append({
                    'id': detail.id, # type: ignore
                    'nombreProducto': detail.product.name,
                    'cantidad': detail.quantity,
                    'precioAparato': detail.product.price,
                    'precioMensual': detail.product.mensual_sales,
                    'mesesAContratar': detail.quotation_mensual
                })
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)})