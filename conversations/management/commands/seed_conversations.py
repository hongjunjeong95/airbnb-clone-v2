from random import randint

from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten

from django_seed import Seed

from users import models as user_models
from conversations import models as conversation_models

NAME = "conversations"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help=f"How many {NAME} do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        users = user_models.User.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            conversation_models.Conversation,
            number,
        )
        conversations_pk = seeder.execute()
        conversations_pk = flatten(conversations_pk.values())

        for conversation_pk in conversations_pk:
            conversation_model = conversation_models.Conversation.objects.get(
                pk=conversation_pk
            )
            add_users = users[randint(0, 5) : randint(5, 10)]
            conversation_model.participants.add(*add_users)

        self.stdout.write(self.style.SUCCESS(f"Create {number} {NAME}"))
