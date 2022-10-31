from django.urls import path

from .consumers import WSConsumer

# creates the websocket url 'some_url', sending data from the consumer
ws_urlpatterns = [
    path('ws/load_path/', WSConsumer.as_asgi())
]