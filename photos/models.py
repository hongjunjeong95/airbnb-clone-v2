from django.db import models
from core import models as core_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=200)
    file = models.ImageField(upload_to="room_photos", blank=True)
    room = models.ForeignKey(
        "rooms.Room", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caption
