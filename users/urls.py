from django.urls import path
from . import views as user_views


app_name = "users"

urlpatterns = [
    path("signup/", user_views.SignUpView.as_view(), name="signup"),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("logout/", user_views.log_out, name="logout"),
    path("<int:pk>/profile/", user_views.UserDetail, name="profile"),
    path("<int:pk>/update-profile/", user_views.UpdateProfile, name="update-profile"),
]
