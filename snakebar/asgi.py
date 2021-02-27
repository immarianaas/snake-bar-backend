"""
ASGI config for snakebar project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from typing import Protocol
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

import gametest.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snakebar.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            gametest.routing.websocket_urlpatterns
        )
    )
})

# channel_layer = channels.asgi.get_channel_layer()

