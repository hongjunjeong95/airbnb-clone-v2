from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [path("<int:reservation_pk>/create/", views.createView, name="create")]
