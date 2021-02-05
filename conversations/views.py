from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from . import models as conversation_models
from rooms import models as room_models
from users import models as user_models


def go_conversation(request, room_pk, host_pk, guest_pk):
    room = room_models.Room.objects.get(pk=room_pk)
    host = user_models.User.objects.get(pk=host_pk)
    guest = user_models.User.objects.get(pk=guest_pk)
    print(host, guest)
    if host == guest:
        return redirect(reverse("core:home"))
    try:
        conversation = conversation_models.Conversation.objects.filter(
            participants=host
        ).get(participants=guest)
    except conversation_models.Conversation.DoesNotExist:
        conversation = conversation_models.Conversation.objects.create()
        conversation.participants.add(host, guest)
    return render(
        request,
        "pages/conversations/conversation_detail.html",
        context={"room": room, "conversation": conversation},
    )


def createMessage(request, room_pk, conversation_pk):
    message = request.POST.get("message")
    try:
        conversation = conversation_models.Conversation.objects.get(pk=conversation_pk)
        pk = []
        for participant in conversation.participants.all():
            pk.append(participant.pk)
        if message is not None:
            conversation_models.Message.objects.create(
                message=message, user=request.user, conversation=conversation
            )
        print(conversation.messages.all())
    except conversation_models.Conversation.DoesNotExist:
        messages.error(request, "Conversation does not exist")
    return redirect(
        reverse(
            "conversations:conversation",
            kwargs={"room_pk": room_pk, "host_pk": pk[0], "guest_pk": pk[1]},
        )
    )
