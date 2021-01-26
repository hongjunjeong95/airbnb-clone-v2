from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    GENDER_OTHER = "Other"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_KOREAN = "KR"
    LANGUAGE_ENGLISH = "EN"
    LANGUAGE_CHOICES = ((LANGUAGE_KOREAN, "Korean"), (LANGUAGE_ENGLISH, "English"))

    CURRENCY_KRW = "KRW"
    CURRENCY_USD = "USD"
    CURRENCY_CHOICES = ((CURRENCY_KRW, "KRW"), (CURRENCY_USD, "USD"))

    avatar = models.ImageField()
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    birthdate = models.DateField(null=True)
    superhost = models.BooleanField(default=False)

    def verify_email(self):
        pass