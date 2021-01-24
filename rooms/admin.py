from django.contrib import admin
from . import models as room_models
from photos import models as photo_models


@admin.register(
    room_models.RoomType,
    room_models.Facility,
    room_models.Amenity,
    room_models.HouseRule,
)
class ImteAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


class PhotoInline(admin.TabularInline):
    model = photo_models.Photo


@admin.register(room_models.Room)
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
        "count_photos",
    )

    list_filter = (
        "guests",
        "bedrooms",
        "beds",
        "bathrooms",
        "host",
        "room_type",
        "instant_book",
        "country",
        "city",
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

    inlines = (PhotoInline,)

    def count_amenities(self, obj):
        return obj.amenities.count()

    count_amenities.short_description = "Amenity Count"

    def count_facilities(self, obj):
        return obj.facilities.count()

    count_facilities.short_description = "Facility Count"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"
