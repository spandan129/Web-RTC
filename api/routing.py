from django.urls import re_path
from .consumers import MyConsumer
from .consumers import GroupChatConsumer
from .consumers import CallConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', MyConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<group_name>[\w-]+)/$', GroupChatConsumer.as_asgi()),
    re_path(r'ws/call/', CallConsumer.as_asgi()),
]