from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from . import models as room_models


def HomeView(request):
    try:
        # Get list of rooms
        rooms_list = room_models.Room.objects.all()

        # Get paginator
        page = request.GET.get("page", 1)
        paginator = Paginator(rooms_list, 12, orphans=6)
        rooms = paginator.get_page(int(page))

        # Get this year
        now = timezone.now()
        this_year = now.year
    except room_models.Room.DoesNotExist:
        print("Model does not exsit")
    except EmptyPage:
        print("Empty page")

    return render(
        request,
        "pages/rooms/home.html",
        context={"rooms": rooms, "year": this_year},
    )


def RoomDetail(request, pk):
    try:
        room = room_models.Room.objects.get(pk=pk)
        month = room.host.date_joined.strftime("%b")

        return render(
            request,
            "pages/rooms/detail.html",
            context={"room": room, "joined_month": month},
        )
    except room_models.Room.DoesNotExist:
        print("Model does not exsit")
        return redirect(reverse("core:home"))