from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("<int:room_pk>/toggle-list/", views.toggleList, name="toggle-list"),
    path("favs/", views.favs, name="favs"),
]
