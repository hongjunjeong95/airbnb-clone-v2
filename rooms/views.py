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
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    bathrooms = int(request.GET.get("bathrooms", 0))
    room_type = int(request.GET.get("room_type", 0))
    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")
    s_house_rules = request.GET.getlist("house_rules")

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()
    house_rules = room_models.HouseRule.objects.all()

    filter_args = {}

    form = {
        "city": city,
        "countries": countries,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "bathrooms": bathrooms,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
        "house_rules": house_rules,
    }

    choices = {
        "s_country": country,
        "s_room_type": room_type,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "s_house_rules": s_house_rules,
    }

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if price != 0:
        filter_args["price__lte"] = price
    if guests != 0:
        filter_args["guests__gte"] = guests
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms
    if beds != 0:
        filter_args["beds__gte"] = beds
    if bathrooms != 0:
        filter_args["bathrooms__gte"] = bathrooms

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    if len(s_house_rules) > 0:
        for s_house_rule in s_house_rules:
            filter_args["house_rules__pk"] = int(s_house_rule)

    qs = room_models.Room.objects.filter(**filter_args).order_by("created")
    paginoatr = Paginator(qs, 10, orphans=5)
    page = request.GET.get("page", 1)
    rooms = paginoatr.get_page(page)
    return render(
        request,
        "pages/root/search.html",
        context={"rooms": rooms, **form, **choices},
    )
