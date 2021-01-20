from django.contrib import admin
from . import models


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
    )

    list_filter = ("status",)

    search_fields = ("guest", "room", "check_in", "check_out")

    raw_id_fields = ("guest",)
