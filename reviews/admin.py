from django.contrib import admin
from . import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):

    """ Review Admin Definition """

    list_display = ("__str__", "avg")

    fieldsets = (
        (
            "Content",
            {
                "fields": (
                    "review",
                    "user",
                    "room",
                ),
            },
        ),
        (
            "Points",
            {
                "fields": (
                    "accuracy",
                    "communication",
                    "cleanliness",
                    "location",
                    "check_in",
                    "value",
                ),
            },
        ),
    )

    raw_id_fields = ("user", "room")
