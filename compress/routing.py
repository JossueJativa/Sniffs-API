import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compress.settings')

from cartAPI.consumers import CartConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('/ws/cart/', CartConsumer) #type: ignore
    ])
})
