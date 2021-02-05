from django.shortcuts import redirect, reverse
from . import models as list_models
from rooms import models as room_models


def toggleList(request, room_pk):
    user = request.user
    if str(user) == "AnonymousUser":
        return redirect(reverse("users:login"))
    action = request.GET.get("action")
    room = room_models.Room.objects.get(pk=room_pk)
    if room is not None and action is not None:
        the_list, b = list_models.List.objects.get_or_create(
            user=request.user, name="My Favorite Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("core:home"))
