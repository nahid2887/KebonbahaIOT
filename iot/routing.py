# iot/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/iot/oneway/$', consumers.OneWayConsumer.as_asgi()),
    re_path(r'ws/iot/twoway/$', consumers.TwoWayConsumer.as_asgi()),
]
