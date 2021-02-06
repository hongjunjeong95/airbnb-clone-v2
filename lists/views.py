from django.shortcuts import redirect, reverse, render
from django.core.paginator import Paginator
from . import models as list_models
from rooms import models as room_models
from django.contrib import messages


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


def favs(request):
    page = request.GET.get("page", 1)

    if page == "":
        page = 1
    else:
        page = int(page)

    page_sector = ((page - 1) // 5) * 5

    the_list = list_models.List.objects.get_or_none(user=request.user)
    if the_list is None:
        messages.error(request, "List does not exist")
        return redirect(reverse("core:home"))
    qs = the_list.rooms.all()
    paginator = Paginator(qs, 12, orphans=6)
    rooms = paginator.get_page(page)
    return render(
        request,
        "pages/lists/list_detail.html",
        context={"rooms": rooms, "page_sector": page_sector},
    )
