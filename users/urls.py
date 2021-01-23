from django.urls import path
from . import views as user_views


app_name = "users"

urlpatterns = [path("login/", user_views.LoginView, name="login")]
