from django.shortcuts import render
from . import models as room_models


def HomeView(request):
    rooms = room_models.Room.objects.all()

    return render(request, "pages/rooms/home.html", context={"rooms": rooms})
