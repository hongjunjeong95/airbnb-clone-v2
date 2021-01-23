from django.urls import path
from rooms import views as room_views

app_name = "core"

urlpatterns = [
    path("", room_views.HomeView, name="home"),
    path("search/", room_views.SearchView, name="search"),
]
