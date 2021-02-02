from django.urls import path
from . import views as reservation_views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room_pk>/<int:year>-<int:month>-<int:day>/",
        reservation_views.createReservation,
        name="create",
    ),
    path(
        "<int:pk>/",
        reservation_views.reservationDetail,
        name="detail",
    ),
    path(
        "<int:pk>/cancel/",
        reservation_views.cancelReservation,
        name="cancel",
    ),
]
