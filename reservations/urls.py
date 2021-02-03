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
    path(
        "<int:pk>/reservation/list/",
        reservation_views.reservationList,
        name="list",
    ),
    path(
        "<int:user_pk>/reservation/<int:room_pk>/room-list/",
        reservation_views.reservationRoomList,
        name="room-list",
    ),
    path(
        "<int:pk>/confirm/",
        reservation_views.confirmReservation,
        name="confirm",
    ),
]
