from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse, render
from django.db.utils import IntegrityError
from . import forms, models


# Sign Up CBV
class SignUpView(FormView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    template_name = "pages/users/signup.html"

    def form_valid(self, form):
        form.save()  # Save information of a registered user
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        try:
            user = authenticate(self.request, username=email, password=password)
            user.verify_email()
            return super().form_valid(form)
        except IntegrityError:
            print("IntegrityError has occured")
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


class LoginView(FormView):
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    template_name = "pages/users/login.html"

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None and user.email_verified == True:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


def UserDetail(request, pk):
    try:
        user_obj = models.User.objects.get(pk=pk)
        return render(
            request, "pages/users/profile.html", context={"user_obj": user_obj}
        )
    except models.User.DoesNotExist:
        print("User does not exist")
        return redirect(reverse("core:home"))


def UpdateProfile(request, pk):
    if request.method == "GET":
        try:
            user = models.User.objects.get(pk=pk)
            genders = models.User.GENDER_CHOICES
            languages = models.User.LANGUAGE_CHOICES
            currencies = models.User.CURRENCY_CHOICES

            choices = {
                "genders": genders,
                "languages": languages,
                "currencies": currencies,
            }

            return render(
                request,
                "pages/users/update_profile.html",
                context={"user": user, **choices},
            )
        except models.User.DoesNotExist:
            print("User does not exist")
            return redirect(reverse("core:home"))
    elif request.method == "POST":
        try:
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
            return redirect(reverse("core:home"))
        except models.User.DoesNotExist:
            print("User does not exist")
            return redirect(reverse("core:home"))


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_secret = ""
        user.email_verified = True
        user.save()
        login(request, user)
    except models.User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))