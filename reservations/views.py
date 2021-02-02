import datetime
from django.contrib import messages
from django.shortcuts import redirect, reverse, render
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
    reservation = reservation_models.Reservation.objects.get(pk=pk)
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
    try:
        reservation = reservation_models.Reservation.objects.get(pk=pk)
        room = reservation.room
        reservation.delete()
        return redirect(reverse("rooms:room-detail", kwargs={"pk": room.pk}))
    except reservation_models.Reservation.DoesNotExist:
        messages.error(request, "Rservation does not exist")
        return redirect(reverse("core:home"))
