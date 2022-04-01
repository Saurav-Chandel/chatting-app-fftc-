"""
ASGI config for chatapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from app import routing
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatapp.settings')

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket":URLRouter(routing.websocket_urlpattrens)

  # Just HTTP for now. (We can add other protocols later.)
})
