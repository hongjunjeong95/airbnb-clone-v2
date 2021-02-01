from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.roomDetail, name="room-detail"),
    path("create/", views.createRoom, name="create-room"),
    path("<int:pk>/edit/", views.editRoom, name="edit-room"),
    path("<int:pk>/delete/", views.deleteRoom, name="delete-room"),
    path("<int:pk>/photos/create/", views.createPhoto, name="create-photo"),
    path("<int:pk>/photos/photo-detail/", views.photoDetail, name="photo-detail"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit-photo/",
        views.editPhoto,
        name="edit-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete-photo/",
        views.deletePhoto,
        name="delete-photo",
    ),
]
