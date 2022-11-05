"""
ASGI config for VCCF project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
from main.routing import ws_urlpatterns


from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VCCF.settings')

# Sets up the websocket urls
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            URLRouter(ws_urlpatterns)
        )
    )
})

