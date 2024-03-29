from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "gender",
        "language",
        "currency",
        "birthdate",
        "superhost",
        "is_active",
        "is_staff",
        "is_superuser",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + (
        "gender",
        "language",
        "currency",
        "superhost",
        "login_method",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "bio",
                    "gender",
                    "language",
                    "currency",
                    "birthdate",
                    "superhost",
                    "email_verified",
                    "email_secret",
                    "login_method",
                )
            },
        ),
    )
