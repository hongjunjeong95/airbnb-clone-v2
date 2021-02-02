from datetime import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.day == 0:
        return
    try:
        date_obj = datetime(year=day.year, month=day.month, day=day.day)
        reservation_models.BookedDay.objects.get(reservation__room=room, day=date_obj)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
