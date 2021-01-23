from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django_countries import countries
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
        "pages/root/home.html",
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


def SearchView(request):
    city = request.GET.get("city", "Anywhere")
    country = request.GET.get("country")
    price = request.GET.get("price")
    guests = request.GET.get("guests")
    bedrooms = request.GET.get("bedrooms")
    beds = request.GET.get("beds")
    bathrooms = request.GET.get("bathrooms")

    filter_args = {}

    form = {
        "city": city,
        "countries": countries,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "bathrooms": bathrooms,
    }

    choices = {"s_country": country}

    filter_args["city__startswith"] = city
    filter_args["country"] = country

    rooms = room_models.Room.objects.filter(**filter_args)
    return render(
        request,
        "pages/root/search.html",
        context={"rooms": rooms, **form, **choices},
    )
