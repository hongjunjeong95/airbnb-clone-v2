from django.db import models
from django_countries.fields import CountryField
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Room(core_models.TimeStampedModel):
    name = models.CharField(max_length=140)
    country = CountryField()
    city = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    price = models.IntegerField()
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    bathrooms = models.IntegerField()
    description = models.TextField()
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)
    instant_book = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_first_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.file.url

    def get_review_points(self):
        reviews = self.reviews.all()
        all_ratings = 0
        for review in reviews:
            all_ratings += review.avg

        if len(reviews) == 0:
            return 0
        ratings = round(all_ratings / len(reviews), 2)
        return ratings
