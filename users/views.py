from django.shortcuts import render


def LoginView(request):
    return render(request, "pages/users/login.html")
