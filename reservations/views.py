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


def reservationDetail(request, pk):
    try:
        reservation = reservation_models.Reservation.objects.get(pk=pk)
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
    except room_models.Room.DoesNotExist:
        messages.error(request, "Reservation does not exist")
        return redirect(reverse("core:home"))


def cancelReservation(request, pk):
    try:
        reservation = reservation_models.Reservation.objects.get(pk=pk)
        if reservation.guest != request.user or request.user != reservation.room.host:
            raise Http404()
        room = reservation.room
        reservation.delete()
        return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))
    except reservation_models.Reservation.DoesNotExist:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))


def reservationList(request, pk):
    try:
        reservations = reservation_models.Reservation.objects.filter(room__host_id=pk)
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
            "pages/reservations/reservation_list.html",
            context={"rooms": rooms, "page_sector": page_sector},
        )
    except reservation_models.Reservation.DoesNotExist:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))


def reservationRoomList(request, user_pk, room_pk):
    try:
        qs = reservation_models.Reservation.objects.filter(
            room__host_id=user_pk, room_id=room_pk
        )
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
            "pages/reservations/reservation_room_list.html",
            context={"reservations": reservations, "room_name": room_name},
        )
    except reservation_models.Reservation.DoesNotExist:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))


def confirmReservation(request, pk):
    try:
        reservation = reservation_models.Reservation.objects.get(pk=pk)
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
                "reservations:room-list",
                kwargs={
                    "user_pk": user_pk,
                    "room_pk": room_pk,
                },
            )
        )
    except reservation_models.Reservation.DoesNotExist:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
