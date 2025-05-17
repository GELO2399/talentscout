# talentscout/routing.py
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from jobs.consumers import JobConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/jobs/<int:job_id>/', JobConsumer.as_asgi()),
        ])
    ),
})
