from django.contrib import admin
from . import models


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    list_display = ("__str__", "count_participants", "count_messages")

    filter_horizontal = ("participants",)

    def count_participants(self, obj):
        return obj.participants.count()

    count_participants.short_description = "Participants count"

    def count_messages(self, obj):
        return obj.messages.count()

    count_messages.short_description = "Messages count"


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = ("__str__", "created")

    raw_id_fields = ("user", "conversation")
