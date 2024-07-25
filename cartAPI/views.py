from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from verifyToken import verify_refresh_token

from .models import Cart
from .serializer import CartSerializer

from authAPI.models import User
from productsAPI.models import Product

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import jwt

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = request.data.get('user_id') if request.data.get('user_id') else decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        
        product_id = request.data.get('product')
        
        try:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(user=user, product=product_id)

            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Invalid product ID'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)
        except Cart.DoesNotExist:
            cart = Cart(
                user=user,
                product = Product.objects.get(id=product_id),
                quantity = request.data.get('quantity')
            )
            cart.save()

            serializer = CartSerializer(cart)
            return Response(serializer.data)
        
        cart_product = Cart.objects.get(user=user, product=product)
        if cart_product:
            cart_product = cart_product
            cart_product.quantity += request.data.get('quantity')
            cart_product.save()
            serializer = CartSerializer(cart_product)
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def update(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def destroy(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        decodeJWT = jwt.decode(request.query_params.get('refresh'), options={"verify_signature": False})
        user_id = decodeJWT['user_id']
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('refresh', openapi.IN_QUERY, description="Refresh Token", type=openapi.TYPE_STRING)
        ]
    )
    @action(detail=False, methods=['get'])
    def getCartByUserId(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        refresh_token = request.query_params.get('refresh')
        
        if not user_id or not refresh_token:
            return Response({'error': 'User ID and Refresh token are required'}, status=400)
        
        try:
            decodeJWT = jwt.decode(refresh_token, options={"verify_signature": False})
            if str(decodeJWT['user_id']) != user_id:
                return Response({'error': 'Invalid user ID'}, status=401)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid refresh token'}, status=401)
        
        error_response = verify_refresh_token(request, user_id)
        if error_response:
            return error_response

        try:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.filter(user=user)
            cart_detail = []
            for item in cart:
                cart_detail.append({
                    'id': item.id, # type: ignore
                    'product': item.product.name,
                    'price': item.product.price,
                    'quantity': item.quantity
                })
            return Response(cart_detail)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=401)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=401)