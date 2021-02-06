import os
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, render
from django.db.utils import IntegrityError
from django.core.paginator import Paginator
from . import forms, models, mixins
from lists import models as list_models
from conversations import models as conversation_models
from .exception import (
    GithubException,
    KakaoException,
    LoggedInOnlyView,
    LoggedOutOnlyView,
    ChangePasswordException,
    VerifyUser,
    EmailLoggedInOnly,
)


# Sign Up CBV
class SignUpView(mixins.LoggedOutOnlyView, FormView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    template_name = "pages/users/signup.html"

    def form_valid(self, form):
        try:
            form.save()  # Save information of a registered user
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=email, password=password)
            user.verify_email()
            messages.success(self.request, f"{user.first_name} signed up")
            return super().form_valid(form)
        except IntegrityError:
            messages.error(
                self.request,
                "IntegrityError has occured. The user already exists in db",
            )
            return redirect(reverse("users:signup"))


# Sign Up FBV
# class SignUpView(FormView):
#     def get(self, request, *args, **kwargs):
#         return render(request, "pages/users/signup.html")

#     def post(self, request, *args, **kwargs):
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         password1 = request.POST.get("password1")

#         try:
#             models.User.objects.get(email=email)
#             raise forms.ValidationError("User already exists with that email")
#         except models.User.DoesNotExist:
#             if password != password1:
#                 raise forms.ValidationError("Password confirmation does not match")

#             new_user = models.User.objects.create_user(email, email, password)
#             new_user.first_name = first_name
#             new_user.last_name = last_name

#             if new_user is not None:
#                 login(request, new_user)
#             return redirect(reverse("core:home"))


class LoginView(mixins.LoggedOutOnlyView, FormView):
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    template_name = "pages/users/login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None and user.email_verified is True:
            messages.success(self.request, f"{user.first_name} logged in")
            login(self.request, user)
        return super().form_valid(form)


def github_login(request):
    try:
        if request.user.is_authenticated:
            raise LoggedOutOnlyView("User already logged in")
        client_id = os.environ.get("GH_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/github/callback/"
        scope = "read:user"
        return redirect(
            f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
        )
    except LoggedOutOnlyView as error:
        messages.error(request, error)
        return redirect("core:home")


def github_login_callback(request):
    try:
        if request.user.is_authenticated:
            raise LoggedOutOnlyView("User already logged in")
        code = request.GET.get("code", None)
        if code is None:
            raise GithubException("Can't get code")

        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")

        token_request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise GithubException("Can't get access token")

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = profile_request.json()
        username = profile_json.get("login", None)

        if username is None:
            raise GithubException("Can't get username from profile_request")

        avatar_url = profile_json.get("avatar_url", None)
        if avatar_url is None:
            raise GithubException("Can't get avatar_url from profile_request")

        name = profile_json.get("name", None)
        if name is None:
            raise GithubException("Can't get name from profile_request")

        email = profile_json.get("email", None)
        if email is None:
            raise GithubException("Can't get email from profile_request")

        bio = profile_json.get("bio", None)
        if bio is None:
            raise GithubException("Can't get bio from profile_request")

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_GITHUB:
                raise GithubException(f"Please login with {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                username=email,
                first_name=name,
                email=email,
                bio=bio,
                login_method=models.User.LOGIN_GITHUB,
                email_verified=True,
            )
            photo_request = requests.get(avatar_url)

            user.avatar.save(f"{name}-avatar", ContentFile(photo_request.content))
            user.set_unusable_password()
            user.save()
        messages.success(request, f"{user.email} logged in with Github")
        login(request, user)
        return redirect(reverse("core:home"))
    except GithubException as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))
    except LoggedOutOnlyView as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))


def kakao_login(request):
    try:
        if request.user.is_authenticated:
            raise LoggedOutOnlyView("User already logged in")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
    except KakaoException as error:
        messages.error(request, error)
        return redirect("core:home")
    except LoggedOutOnlyView as error:
        messages.error(request, error)
        return redirect("core:home")


def kakao_login_callback(request):
    try:
        if request.user.is_authenticated:
            raise LoggedOutOnlyView("User already logged in")
        code = request.GET.get("code", None)
        if code is None:
            KakaoException("Can't get code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback/"
        client_secret = os.environ.get("KAKAO_SECRET")
        request_access_token = requests.post(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
            headers={"Accept": "application/json"},
        )
        access_token_json = request_access_token.json()
        error = access_token_json.get("error", None)
        if error is not None:
            print(error)
            KakaoException("Can't get access token")
        access_token = access_token_json.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_request = requests.post(
            "https://kapi.kakao.com/v2/user/me",
            headers=headers,
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        profile = kakao_account.get("profile")

        nickname = profile.get("nickname", None)
        avatar_url = profile.get("profile_image_url", None)
        email = kakao_account.get("email", None)
        gender = kakao_account.get("gender", None)

        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise GithubException(f"Please login with {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create_user(
                email=email,
                username=email,
                first_name=nickname,
                gender=gender,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )

            if avatar_url is not None:
                avatar_request = requests.get(avatar_url)
                # print(avatar_request.content())
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(avatar_request.content)
                )
            user.set_unusable_password()
            user.save()
        messages.success(request, f"{user.email} signed up and logged in with Kakao")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))
    except LoggedOutOnlyView as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))


def log_out(request):
    try:
        if not request.user.is_authenticated:
            raise LoggedInOnlyView("Please login first")
        messages.info(request, f"See you later {request.user.first_name}")
        logout(request)
        return redirect(reverse("core:home"))
    except LoggedInOnlyView as error:
        messages.error(request, error)
        return redirect("users:login")


def userDetail(request, pk):
    try:
        user_obj = models.User.objects.get(pk=pk)

        page = int(request.GET.get("page", 1))
        page_sector = ((page - 1) // 5) * 5
        qs = user_obj.rooms.all()
        paginator = Paginator(qs, 12, orphans=6)
        rooms = paginator.get_page(page)

        conversations = conversation_models.Conversation.objects.filter(
            participants=request.user
        )
        conversation_count = conversations.count()

        the_list = list_models.List.objects.get(user=request.user)
        list_room_count = the_list.rooms.count()

    except models.User.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect(reverse("core:home"))
    except list_models.List.DoesNotExist:
        list_room_count = 0
    return render(
        request,
        "pages/users/profile.html",
        context={
            "user_obj": user_obj,
            "rooms": rooms,
            "page_sector": page_sector,
            "list_room_count": list_room_count,
            "conversation_count": conversation_count,
        },
    )


def updateProfile(request, pk):
    if request.method == "GET":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Please login first")

            if request.user.pk != pk:
                raise VerifyUser("Page Not found")

            user = models.User.objects.get(pk=pk)
            genders = models.User.GENDER_CHOICES
            languages = models.User.LANGUAGE_CHOICES
            currencies = models.User.CURRENCY_CHOICES
            login_methods = models.User.LOGIN_CHOICES

            choices = {
                "genders": genders,
                "languages": languages,
                "currencies": currencies,
                "login_methods": login_methods,
            }

            return render(
                request,
                "pages/users/update_profile.html",
                context={"user": user, **choices},
            )
        except models.User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect(reverse("core:home"))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect("users:login")
        except VerifyUser as error:
            messages.error(request, error)
            return redirect("core:home")
    elif request.method == "POST":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Please login first")
            if request.user.pk != pk:
                raise VerifyUser("Page Not found")

            user = models.User.objects.get(pk=pk)

            avatar = request.POST.get("avatar")
            if avatar is not None:
                user.avatar = avatar

            first_name = request.POST.get("first_name")
            if first_name is not None:
                user.first_name = first_name

            last_name = request.POST.get("last_name")
            if last_name is not None:
                user.last_name = last_name

            email = request.POST.get("email")
            if email is not None:
                user.email = email

            gender = request.POST.get("gender")
            if gender is not None:
                user.gender = gender

            language = request.POST.get("language")
            if language is not None:
                user.language = language

            currency = request.POST.get("currency")
            if currency is not None:
                user.currency = currency

            birthdate = request.POST.get("birthdate")

            if birthdate is not None:
                user.birthdate = birthdate

            superhost = bool(request.POST.get("superhost"))
            if superhost is not None:
                user.superhost = superhost

            bio = request.POST.get("bio")
            if bio is not None:
                user.bio = bio

            user.save()
            messages.success(request, f"{user.email} profile update succeded")
            return redirect(reverse("users:profile", kwargs={"pk": pk}))
        except models.User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect(reverse("core:home"))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect("users:login")
        except VerifyUser as error:
            messages.error(request, error)
            return redirect("core:home")


def complete_verification(request, key):
    try:
        if request.user.is_authenticated:
            raise LoggedOutOnlyView("Please verify email first")
        user = models.User.objects.get(email_secret=key)
        user.email_secret = ""
        user.email_verified = True
        user.save()
        login(request, user)
        messages.success(request, f"{user.email} verification is completed")
    except models.User.DoesNotExist:
        messages.error(request, "User does not exist")
    except LoggedOutOnlyView as error:
        messages.error(request, error)
        return redirect("core:home")
    return redirect(reverse("core:home"))


def change_password(request, pk):
    if request.method == "GET":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Please login first")
            if request.user.login_method != "email":
                raise EmailLoggedInOnly("Page not found 404")
            if request.user.pk != pk:
                raise VerifyUser("Page Not found 404")
            user = models.User.objects.get(pk=pk)

            return render(
                request,
                "pages/users/change_password.html",
                context={"user": user},
            )
        except models.User.DoesNotExist:
            print("User does not exist")
            return redirect(reverse("core:home"))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect("users:login")
        except VerifyUser as error:
            messages.error(request, error)
            return redirect("core:home")
        except EmailLoggedInOnly as error:
            messages.error(request, error)
            return redirect("core:home")
    elif request.method == "POST":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView
            if request.user.login_method != "email":
                raise EmailLoggedInOnly("Page not found 404")
            if request.user.pk != pk:
                raise VerifyUser("Page Not found")
            user = models.User.objects.get(pk=pk)
            old_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            new_password1 = request.POST.get("verify_password")

            user = authenticate(request, username=user.email, password=old_password)
            if user is None:
                raise ChangePasswordException("Current password is wrong!")

            if new_password != new_password1:
                raise ChangePasswordException("New password doesn't match")
            user.set_password(new_password)
            user.save()
            messages.success(request, f"{user.email}'password changed successfully")
            return redirect(reverse("users:profile", kwargs={"pk": pk}))
        except ChangePasswordException as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect("users:login")
        except VerifyUser as error:
            messages.error(request, error)
            return redirect("core:home")
        except EmailLoggedInOnly as error:
            messages.error(request, error)
            return redirect("core:home")


def switch_hosting(request):
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))