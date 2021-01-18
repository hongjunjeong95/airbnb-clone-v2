from django.contrib import admin
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ImteAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    list_display = (
        "name",
        "country",
        "city",
        "address",
        "price",
        "guests",
        "bedrooms",
        "beds",
        "bathrooms",
        "host",
        "room_type",
        "count_amenities",
        "count_facilities",
    )

    list_filter = (
        "city",
        "guests",
        "bedrooms",
        "beds",
        "bathrooms",
        "host",
        "room_type",
        "country",
        "instant_book",
    )

    search_fields = ("^city", "name", "host__username")

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "host",
                    "price",
                    "room_type",
                ),
            },
        ),
        (
            "Space",
            {
                "fields": (
                    "guests",
                    "bedrooms",
                    "beds",
                    "bathrooms",
                )
            },
        ),
        (
            "More about space",
            {
                "fields": (
                    "amenities",
                    "facilities",
                    "house_rules",
                )
            },
        ),
        (
            "Booking",
            {"fields": ("instant_book",)},
        ),
    )

    raw_id_fields = ("host",)

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    def count_facilities(self, obj):
        return obj.facilities.count()

    count_facilities.short_description = "Facility Count"
