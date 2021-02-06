from django.urls import path
from . import views


app_name = "conversations"

urlpatterns = [
    path(
        "<int:host_pk>/<int:guest_pk>/",
        views.createConversation,
        name="create-conversation",
    ),
    path(
        "conversation-list/",
        views.conversationList,
        name="conversation-list",
    ),
    path(
        "<int:pk>/conversation-detail/",
        views.conversationDetail,
        name="conversation-detail",
    ),
    path(
        "<int:conversation_pk>/messages/",
        views.createMessage,
        name="create-message",
    ),
]
