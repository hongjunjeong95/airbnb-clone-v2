import datetime
from django.contrib import messages
from django.shortcuts import redirect, reverse, render
from django.core.paginator import Paginator
from django.http import Http404

from users.exception import LoggedInOnlyView
from . import models as reservation_models
from rooms import models as room_models


class CreateError(Exception):
    pass


def createReservation(request, room_pk, year, month, day):
    try:
        if not request.user.is_authenticated:
            raise LoggedInOnlyView("Login First Please.")
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room_pk)
        reservation_models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't reserve that room")
        return redirect(reverse("core:home"))
    except LoggedInOnlyView as error:
        messages.error(request, error)
        return redirect(reverse("core:home"))
    except reservation_models.BookedDay.DoesNotExist:
        reservation = reservation_models.Reservation.objects.create(
            status=reservation_models.Reservation.STATUS_PENDING,
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )

        messages.success(request, f"Reserve {room} successfully")
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


def reservationList(request, user_pk):
    qs = reservation_models.Reservation.objects.filter(guest_id=user_pk)
    if qs is None:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))

    for reservation in qs:
        # Route Protection
        if reservation.guest != request.user:
            raise Http404()

    page = request.GET.get("page", 1)
    if page == "":
        page = 1
    else:
        page = int(page)
    page_sector = (page - 1) // 5
    page_sector = page_sector * 5
    paginator = Paginator(qs, 8, orphans=4)
    reservations = paginator.get_page(page)
    return render(
        request,
        "pages/reservations/reservation_list.html",
        context={"reservations": reservations, "page_sector": page_sector},
    )


def reservationDetail(request, pk):
    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    if reservation is None:
        messages.error(request, "Reservation does not exist")
        return redirect(reverse("core:home"))
    if reservation.guest != request.user:
        raise Http404()
    bookedDays = reservation.bookedDays.all()
    days = []

    for day in bookedDays:
        day = str(day)
        day = int(day.split("-")[2])
        days.append(day)

    room = reservation.room
    return render(
        request,
        "pages/reservations/reservation_detail.html",
        context={"room": room, "reservation": reservation, "days": days},
    )


def cancelReservation(request, pk):
    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    if reservation is None:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
    if request.user != reservation.guest and request.user != reservation.room.host:
        raise Http404()
    room = reservation.room
    reservation.delete()
    return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))


def confirmReservation(request, pk):
    reservation = reservation_models.Reservation.objects.get_or_none(pk=pk)
    if reservation is None:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
    # Route Protection
    if reservation.room.host != request.user:
        raise Http404()
    reservation.status = reservation_models.Reservation.STATUS_CONFIRMED
    reservation.save()

    room = reservation.room

    user_pk = request.user.pk
    room_pk = room.pk

    return redirect(
        reverse(
            "reservations:host-room-list",
            kwargs={
                "user_pk": user_pk,
                "room_pk": room_pk,
            },
        )
    )


def reservationHostList(request, pk):
    reservations = reservation_models.Reservation.objects.filter(room__host_id=pk)
    if reservation is None:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
    qs = []
    for reservation in reservations:
        # Route Protection
        if reservation.room.host != request.user:
            raise Http404()
        if reservation.room not in qs:
            qs.append(reservation.room)
    page = request.GET.get("page", 1)
    if page == "":
        page = 1
    else:
        page = int(page)
    page_sector = (page - 1) // 5
    page_sector = page_sector * 5
    paginator = Paginator(qs, 8, orphans=4)
    rooms = paginator.get_page(page)
    return render(
        request,
        "pages/reservations/reservation_host_list.html",
        context={"rooms": rooms, "page_sector": page_sector},
    )


def reservationHostRoomList(request, user_pk, room_pk):
    qs = reservation_models.Reservation.objects.filter(
        room__host_id=user_pk, room_id=room_pk
    )
    if qs is None:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
    if qs[0].room.host != request.user:
        raise Http404()
    room_name = qs[0].room.name

    page = request.GET.get("page", 1)

    if page == "":
        page = 1
    else:
        page = int(page)

    page_sector = (page - 1) // 5
    page_sector = page_sector * 5
    paginator = Paginator(qs, 8, orphans=4)
    reservations = paginator.get_page(page)
    return render(
        request,
        "pages/reservations/reservation_host_room_list.html",
        context={"reservations": reservations, "room_name": room_name},
    )
