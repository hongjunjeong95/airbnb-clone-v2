from django.shortcuts import render


def HomeView(request):
    return render(request, "pages/rooms/home.html")