from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models


class Review(core_models.TimeStampedModel):

    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    avg = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.review} - {self.room}"

    def save(self, *args, **kwargs):
        self.avg = (
            self.accuracy
            + self.communication
            + self.cleanliness
            + self.location
            + self.check_in
            + self.value
        ) / 6
        self.avg = round(self.avg, 2)
        super().save(*args, **kwargs)
