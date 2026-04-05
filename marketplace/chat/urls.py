from django.urls import path
from chat.views import private_chat

app_name = "chat"

urlpatterns = [
    path("<str:user1>/<str:user2>/", private_chat, name="private_chat"),
]