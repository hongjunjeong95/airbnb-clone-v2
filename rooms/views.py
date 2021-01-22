from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from . import models as room_models


def HomeView(request):
    # Get list of rooms
    rooms_list = room_models.Room.objects.all()

    # Get this year
    now = timezone.now()
    this_year = now.year

    # Get paginator
    page = request.GET.get("page", 1)
    paginator = Paginator(rooms_list, 12, orphans=6)
    rooms = paginator.get_page(int(page))

    return render(
        request, "pages/rooms/home.html", context={"rooms": rooms, "year": this_year}
    )
