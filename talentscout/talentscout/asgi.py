# talentscout/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import jobs.routing
import messaging.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentscout.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            jobs.routing.websocket_urlpatterns + 
            messaging.routing.websocket_urlpatterns
        )
    ),
})
