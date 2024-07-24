import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.response import Response
from django.conf import settings

from authAPI.models import User

def verify_refresh_token(request, user_id=None):
    refresh_token = request.data.get('refresh') or request.query_params.get('refresh')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=400)
    
    try:
        decode = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_decode_id = int(decode['user_id'])
        user_id = int(user_id) if user_id else None

        if user_id and user_decode_id != user_id:
            return Response({'error': 'Invalid user'}, status=400)
        
    except ExpiredSignatureError:
        return Response({'error': 'Refresh token is expired'}, status=400)
    except InvalidTokenError:
        return Response({'error': 'Invalid refresh token'}, status=400)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({'error': 'An error occurred while verifying the refresh token'}, status=400)
    
    return None

def verify_refresh_token_and_superuser(request):
        refresh = request.query_params.get('refresh')
        if not refresh:
            return Response({'error': 'Refresh token is required'}, status=400)

        try:
            payload = jwt.decode(refresh, options={"verify_signature": False})
            user_id = int(payload['user_id'])
            user = User.objects.get(id=user_id)
            if not user:
                return Response({'error': 'Invalid refresh token'}, status=400)
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=400)

        if not user.is_superuser:
            return Response({'error': 'Access denied. Only superusers can access this resource.'}, status=403)
        
        return None