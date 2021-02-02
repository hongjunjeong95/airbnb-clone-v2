from django.contrib import admin
from . import models


@admin.register(models.BookedDay)
class BookedDay(admin.ModelAdmin):
    """ BookedDAy Admin Definition """

    list_display = (
        "__str__",
        "reservation",
    )


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):

    """ Reservation Admin Definition """

    list_display = (
        "__str__",
        "status",
        "guest",
        "room",
        "check_in",
        "check_out",
        "in_progress",
        "is_finished",
    )

    list_filter = ("status",)

    search_fields = ("guest", "room", "check_in", "check_out")

    raw_id_fields = ("guest",)
