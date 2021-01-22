from datetime import datetime
from django.shortcuts import render
from . import models as room_models


def HomeView(request):
    rooms = room_models.Room.objects.all()
    now = datetime.now()
    year = datetime.date(now).year
    return render(
        request, "pages/rooms/home.html", context={"rooms": rooms, "year": year}
    )
