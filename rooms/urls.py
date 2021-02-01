from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.roomDetail, name="room-detail"),
    path("create/", views.createRoom, name="create-room"),
    path("<int:pk>/edit/", views.editRoom, name="edit-room"),
    path("<int:pk>/delete/", views.deleteRoom, name="delete-room"),
]
