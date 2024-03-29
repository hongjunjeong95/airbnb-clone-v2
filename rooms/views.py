from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django_countries import countries
from django.contrib import messages

from . import models as room_models
from photos import models as photo_models
from users.exception import LoggedInOnlyView, VerifyUser, HostOnly


def homeView(request):
    try:
        # Get list of rooms
        rooms_list = room_models.Room.objects.all()

        # Get paginator
        page = int(request.GET.get("page", 1))
        page_sector = (page - 1) // 5
        page_sector = page_sector * 5
        paginator = Paginator(rooms_list, 12, orphans=6)
        rooms = paginator.get_page(page)

        # Get this year
        now = timezone.now()
        this_year = now.year
    except room_models.Room.DoesNotExist:
        messages.error(request, "Room does not exsit")
    except EmptyPage:
        print("Empty page")

    return render(
        request,
        "pages/root/home.html",
        context={"rooms": rooms, "year": this_year, "page_sector": page_sector},
    )


def searchView(request):
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
    instant_book = bool(request.GET.get("instant_book"))

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
        "instant_book": instant_book,
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

    if instant_book:
        filter_args["instant_book"] = instant_book

    qs = room_models.Room.objects.filter(**filter_args).order_by("created")
    paginoatr = Paginator(qs, 12, orphans=6)
    page = request.GET.get("page", 1)
    rooms = paginoatr.get_page(page)
    return render(
        request,
        "pages/root/search.html",
        context={"rooms": rooms, **form, **choices},
    )


def roomDetail(request, pk):
    room = room_models.Room.objects.get_or_none(pk=pk)
    if room is None:
        messages.error(request, "Room does not exsit")
        return redirect(reverse("core:home"))
    month = room.host.date_joined.strftime("%b")

    return render(
        request,
        "pages/rooms/room_detail.html",
        context={"room": room, "joined_month": month},
    )


def createRoom(request):
    if request.method == "GET":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Please login first")
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")

            room_types = room_models.RoomType.objects.all()
            amenities = room_models.Amenity.objects.all()
            facilities = room_models.Facility.objects.all()
            house_rules = room_models.HouseRule.objects.all()

            form = {
                "countries": countries,
                "room_types": room_types,
                "amenities": amenities,
                "facilities": facilities,
                "house_rules": house_rules,
            }
            return render(request, "pages/rooms/create_room.html", context={**form})
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
    elif request.method == "POST":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")

            host = request.user
            name = request.POST.get("name")
            city = request.POST.get("city")
            address = request.POST.get("address")
            country_code = request.POST.get("country")
            price = int(request.POST.get("price", 0))
            guests = int(request.POST.get("guests", 0))
            bedrooms = int(request.POST.get("bedrooms", 0))
            beds = int(request.POST.get("beds", 0))
            bathrooms = int(request.POST.get("bathrooms", 0))
            room_type = int(request.POST.get("room_type", 0))
            description = request.POST.get("description")
            amenities = request.POST.getlist("amenities")
            facilities = request.POST.getlist("facilities")
            house_rules = request.POST.getlist("house_rules")
            caption = request.POST.get("caption")
            photo = request.FILES.get("photo")
            instant_book = bool(request.POST.get("instant_book"))

            room = room_models.Room.objects.create(
                name=name,
                city=city,
                address=address,
                price=price,
                guests=guests,
                bedrooms=bedrooms,
                beds=beds,
                bathrooms=bathrooms,
                description=description,
                host=host,
                room_type_id=room_type,
                instant_book=instant_book,
            )

            room.country = country_code
            room.save()

            room.amenities.set(amenities)
            room.facilities.set(facilities)
            room.house_rules.set(house_rules)

            photo = photo_models.Photo.objects.create(
                file=photo, caption=caption, room_id=room.pk
            )

            messages.success(request, f"Create {room.name} successfully")
            return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))


def editRoom(request, pk):
    if request.method == "GET":
        try:
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Page Not Found")
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            room = room_models.Room.objects.get_or_none(pk=pk)
            if room is None:
                messages.error(request, "Room does not exsit")
                return redirect(reverse("core:home"))

            if request.user.pk != room.host.pk:
                raise VerifyUser("Page Not Found")

            amenities = room_models.Amenity.objects.all()
            facilities = room_models.Facility.objects.all()
            house_rules = room_models.HouseRule.objects.all()
            room_types = room_models.RoomType.objects.all()

            s_amenities = room.amenities.all()
            s_facilities = room.facilities.all()
            s_house_rules = room.house_rules.all()

            form = {
                "countries": countries,
                "room_types": room_types,
                "amenities": amenities,
                "facilities": facilities,
                "house_rules": house_rules,
            }

            choices = {
                "s_amenities": s_amenities,
                "s_facilities": s_facilities,
                "s_house_rules": s_house_rules,
            }
            return render(
                request,
                "pages/rooms/edit_room.html",
                context={"room": room, **form, **choices},
            )

        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except VerifyUser as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
    elif request.method == "POST":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            name = request.POST.get("name")
            city = request.POST.get("city")
            address = request.POST.get("address")
            country_code = request.POST.get("country")
            price = int(request.POST.get("price", 0))
            guests = int(request.POST.get("guests", 0))
            bedrooms = int(request.POST.get("bedrooms", 0))
            beds = int(request.POST.get("beds", 0))
            bathrooms = int(request.POST.get("bathrooms", 0))
            room_type = int(request.POST.get("room_type", 0))
            description = request.POST.get("description")
            amenities = request.POST.getlist("amenities")
            facilities = request.POST.getlist("facilities")
            house_rules = request.POST.getlist("house_rules")
            instant_book = bool(request.POST.get("instant_book"))

            room = room_models.Room.objects.get(pk=pk)
            s_room_type = room_models.RoomType.objects.get(pk=room_type)

            room.name = name
            room.city = city
            room.address = address
            room.price = price
            room.guests = guests
            room.bedrooms = bedrooms
            room.beds = beds
            room.bathrooms = bathrooms
            room.room_type = s_room_type
            room.description = description
            room.instant_book = instant_book

            room.country = country_code
            room.save()

            room.amenities.set(amenities)
            room.facilities.set(facilities)
            room.house_rules.set(house_rules)

            messages.success(request, f"Edit {room.name} successfully")
            return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))


def deleteRoom(request, pk):
    try:
        if not request.session.get("is_hosting"):
            raise HostOnly("Page Not Found")
        room = room_models.Room.objects.get_or_none(pk=pk)
        if room is None:
            messages.error(request, "Room does not exsit")
            return redirect(reverse("core:home"))

        if request.user.pk != room.host.pk:
            raise VerifyUser("Page Not Found")
        room.delete()
        messages.success(request, f"Delete {room.name} successfully")
        return redirect(reverse("users:profile", kwargs={"pk": request.user.pk}))
    except HostOnly as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))


def photoDetail(request, pk):
    try:
        if not request.session.get("is_hosting"):
            raise HostOnly("Page Not Found")
        if not request.user.is_authenticated:
            raise LoggedInOnlyView("Page Not Found")

        page = request.GET.get("page", 1)

        if page == "":
            page = 1
        else:
            page = int(page)

        page_sector = ((page - 1) // 5) * 5

        room = room_models.Room.objects.get_or_none(pk=pk)
        if room is None:
            messages.error(request, "Room does not exsit")
            return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))

        qs = room.photos.all()
        paginator = Paginator(qs, 10, orphans=5)
        photos = paginator.get_page(page)

        if request.user.pk != room.host.pk:
            raise VerifyUser("Page Not Found")

        return render(
            request,
            "pages/rooms/photos/photo_detail.html",
            context={
                "photos": photos,
                "page_sector": page_sector,
                "room": room,
            },
        )
    except VerifyUser as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))
    except HostOnly as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))


def createPhoto(request, pk):
    if request.method == "GET":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Page Not Found")

            room = room_models.Room.objects.get(pk=pk)

            if request.user.pk != room.host.pk:
                raise VerifyUser("Page Not Found")

            return render(
                request,
                "pages/rooms/photos/create_photo.html",
                context={"room": room},
            )
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
    elif request.method == "POST":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            caption = request.POST.get("caption")
            photo = request.FILES.get("photo")

            room = room_models.Room.objects.get(pk=pk)
            photo = photo_models.Photo.objects.create(
                file=photo, caption=caption, room_id=room.pk
            )

            messages.success(request, f"Create {caption}-photo successfully")
            return redirect(reverse("rooms:photo-detail", kwargs={"pk": room.pk}))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))


def editPhoto(request, room_pk, photo_pk):
    if request.method == "GET":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            if not request.user.is_authenticated:
                raise LoggedInOnlyView("Page Not Found")

            room = room_models.Room.objects.get(pk=room_pk)
            if request.user.pk != room.host.pk:
                raise VerifyUser("Page Not Found")
            photo = room.photos.get(pk=photo_pk)

            return render(
                request,
                "pages/rooms/photos/edit_photo.html",
                context={"room": room, "photo": photo},
            )
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
    elif request.method == "POST":
        try:
            if not request.session.get("is_hosting"):
                raise HostOnly("Page Not Found")
            caption = request.POST.get("caption")

            room = room_models.Room.objects.get(pk=room_pk)
            photo = room.photos.get(pk=photo_pk)
            photo.caption = caption
            photo.save()

            messages.success(request, f"Edit {caption}-photo successfully")
            return redirect(reverse("rooms:photo-detail", kwargs={"pk": room.pk}))
        except LoggedInOnlyView as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))
        except HostOnly as error:
            messages.error(request, error)
            return redirect(reverse("core:home"))


def deletePhoto(request, room_pk, photo_pk):
    try:
        if not request.session.get("is_hosting"):
            raise HostOnly("Page Not Found")
        room = room_models.Room.objects.get_or_none(pk=room_pk)
        if room is None:
            messages.error(request, "Room does not exsit")
            return redirect(reverse("core:home"))

        if request.user.pk != room.host.pk:
            raise VerifyUser("Page Not Found")

        photo = room.photos.get(pk=photo_pk)
        photo.delete()
        messages.success(request, f"Delete {photo} successfully")
        return redirect(reverse("rooms:photo-detail", kwargs={"pk": room.pk}))
    except HostOnly as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))