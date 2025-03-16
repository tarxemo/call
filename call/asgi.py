import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import record.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "call.settings")
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            record.routing.websocket_urlpatterns
        )
    ),
})
