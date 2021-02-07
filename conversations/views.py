from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from . import models as conversation_models
from users import models as user_models


def createConversation(request, host_pk, guest_pk):
    try:
        host = user_models.User.objects.get(pk=host_pk)
        guest = user_models.User.objects.get(pk=guest_pk)
        conversation = conversation_models.Conversation.objects.filter(
            participants=guest
        ).get(participants=host)

        return redirect(
            reverse("conversations:conversation-detail", kwargs={"pk": conversation.pk})
        )
    except conversation_models.Conversation.DoesNotExist:
        conversation = conversation_models.Conversation.objects.create()
        conversation.participants.add(host, guest)
        return redirect(
            reverse("rooms:conversation-detail", kwargs={"pk": conversation.pk})
        )


def conversationList(request):
    qs = conversation_models.Conversation.objects.filter(participants=request.user)

    page = request.GET.get("page", 1)

    if page == "":
        page = 1
    else:
        page = int(page)

    page_sector = ((page - 1) // 5) * 5
    paginator = Paginator(qs, 12, orphans=6)
    conversations = paginator.get_page(page)

    return render(
        request,
        "pages/conversations/conversation_host_list.html",
        context={"conversations": conversations, "page_sector": page_sector},
    )


def conversationDetail(request, pk):
    conversation = conversation_models.Conversation.objects.get(pk=pk)

    return render(
        request,
        "pages/conversations/conversation_detail.html",
        context={"conversation": conversation},
    )


def createMessage(request, conversation_pk):
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
    except conversation_models.Conversation.DoesNotExist:
        messages.error(request, "Conversation does not exist")
    return redirect(
        reverse("conversations:conversation-detail", kwargs={"pk": conversation.pk})
    )
