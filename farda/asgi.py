import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farda.settings')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farda.settings')

# Ensure Django is fully loaded before importing Channels routing
import django
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import iot.routing
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            iot.routing.websocket_urlpatterns
        )
    ),
})
