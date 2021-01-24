from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from . import forms


# Sign Up CBV
class SignUpView(FormView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    template_name = "pages/users/signup.html"

    def form_valid(self, form):
        form.save()  # Save information of a registered user
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


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
        if user is not None:
            login(self.request, user)
            print("login")
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
