from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.roomDetail, name="detail"),
    path("create/", views.createRoom, name="create"),
    path("<int:pk>/edit/", views.editRoom, name="edit"),
    path("<int:pk>/delete/", views.deleteRoom, name="delete"),
]
