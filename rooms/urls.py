from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>/", views.roomDetail, name="detail"),
    path("create/", views.roomCreate, name="create"),
]
