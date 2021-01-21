from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """ List Admin Definition """

    list_display = ("__str__", "user", "count_rooms")
    search_fields = ("name",)

    filter_horizontal = ("rooms",)

    raw_id_fields = ("user",)

    def count_rooms(self, obj):
        return obj.rooms.count()
