from django.urls import path
from . import views


app_name = "conversations"

urlpatterns = [
    path(
        "<int:room_pk>/<int:host_pk>/<int:guest_pk>/",
        views.go_conversation,
        name="conversation",
    ),
    path(
        "<int:room_pk>/<int:conversation_pk>/",
        views.createMessage,
        name="create-message",
    ),
]
