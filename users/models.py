import uuid
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config import settings


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

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    birthdate = models.DateField(null=True)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    login_method = models.CharField(
        max_length=6, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            send_mail(
                "Verify Hairbnb Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                ["wjdghdwns0@gmail.com"],
                fail_silently=False,
                html_message=html_message,
            )
            self.save()
        return
