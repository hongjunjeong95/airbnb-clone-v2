from django.db import models
from django_countries.fields import CountryField
from django.shortcuts import redirect, reverse
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
        try:
            (photo,) = self.photos.all()[:1]
            return photo.file.url
        except Exception as error:
            print(error)
            return None

    def get_four_photo(self):
        photos = self.photos.all()[1:5]
        return enumerate(photos)

    def get_review_points(self):
        reviews = self.reviews.all()
        all_ratings = 0
        for review in reviews:
            all_ratings += review.avg

        if len(reviews) == 0:
            return 0
        ratings = round(all_ratings / len(reviews), 2)
        return ratings

    def calculate_accuracy(self):
        reviews = self.reviews.all()
        all_accuracy_points = 0
        for review in reviews:
            all_accuracy_points += review.accuracy

        if len(reviews) == 0:
            return 0
        accuracy = round(all_accuracy_points / len(reviews), 2)

        return accuracy

    def calculate_communication(self):
        reviews = self.reviews.all()
        all_communication_points = 0
        for review in reviews:
            all_communication_points += review.communication

        if len(reviews) == 0:
            return 0
        communication = round(all_communication_points / len(reviews), 2)

        return communication

    def calculate_cleanliness(self):
        reviews = self.reviews.all()
        all_cleanliness_points = 0
        for review in reviews:
            all_cleanliness_points += review.cleanliness

        if len(reviews) == 0:
            return 0
        cleanliness = round(all_cleanliness_points / len(reviews), 2)

        return cleanliness

    def calculate_location(self):
        reviews = self.reviews.all()
        all_location_points = 0
        for review in reviews:
            all_location_points += review.location

        if len(reviews) == 0:
            return 0
        location = round(all_location_points / len(reviews), 2)

        return location

    def calculate_check_in(self):
        reviews = self.reviews.all()
        all_check_in_points = 0
        for review in reviews:
            all_check_in_points += review.check_in

        if len(reviews) == 0:
            return 0
        check_in = round(all_check_in_points / len(reviews), 2)

        return check_in

    def calculate_value(self):
        reviews = self.reviews.all()
        all_value_points = 0
        for review in reviews:
            all_value_points += review.value

        if len(reviews) == 0:
            return 0
        value = round(all_value_points / len(reviews), 2)

        return value

    def get_absolute_url(self):
        return redirect(reverse("rooms:detail", kwargs={"pk": self.pk}))
