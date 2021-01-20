from django.db import models
from core import models as core_models


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    cpation = models.CharField(max_length=50)
    file = models.ImageField()
    room = models.ForeignKey(
        "rooms.Room", related_name="photos", on_delete=models.CASCADE
    )
