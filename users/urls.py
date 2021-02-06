from django.urls import path
from . import views as user_views


app_name = "users"

urlpatterns = [
    path("signup/", user_views.SignUpView.as_view(), name="signup"),
    path("login/", user_views.LoginView.as_view(), name="login"),
    path("login/github/", user_views.github_login, name="github-login"),
    path(
        "login/github/callback/",
        user_views.github_login_callback,
        name="github-callback",
    ),
    path("login/kakao/", user_views.kakao_login, name="kakao-login"),
    path(
        "login/kakao/callback/",
        user_views.kakao_login_callback,
        name="kakao-callback",
    ),
    path("logout/", user_views.log_out, name="logout"),
    path("<int:pk>/profile/", user_views.userDetail, name="profile"),
    path("<int:pk>/update-profile/", user_views.updateProfile, name="update-profile"),
    path(
        "<int:pk>/change-password/", user_views.change_password, name="change-password"
    ),
    path(
        "verify/<str:key>/",
        user_views.complete_verification,
        name="complete-verification",
    ),
    path("switch-hosting", user_views.switch_hosting, name="switch-hosting"),
    path("switch-language", user_views.switch_language, name="switch-language"),
]
