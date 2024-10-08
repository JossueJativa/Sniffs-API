import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compress.settings')

django_application = get_asgi_application()

async def application(scope, receive, send):
    if scope['type'] == 'http':
        await django_application(scope, receive, send)
    elif scope['type'] == 'websocket':
        pass
    else:
        raise NotImplementedError(f"Unknown scope type {scope['type']}")