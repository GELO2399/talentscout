"""
ASGI config for talentscout project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
<<<<<<< HEAD
from channels.auth import AuthMiddlewareStack
import jobs.routing
=======
from django.core.asgi import get_asgi_application
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
import messaging.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
<<<<<<< HEAD
    "websocket": AuthMiddlewareStack(
        URLRouter(
            jobs.routing.websocket_urlpatterns + 
            messaging.routing.websocket_urlpatterns
        )
=======
    "websocket": URLRouter(
        messaging.routing.websocket_urlpatterns
>>>>>>> parent of 4094cd6f (Addition of Messaging and Chat, Development is on progress)
    ),
})
