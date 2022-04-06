from django.urls import path
from app import consumers
from django.urls import re_path

websocket_urlpattrens=[
     path('ws/sc/<str:GroupName>/',consumers.MySyncConsumer.as_asgi()),
     path('ws/ac/',consumers.MyAsyncConsumer.as_asgi()),
]