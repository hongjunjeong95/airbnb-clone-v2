from random import choice
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from conversations import models as conversation_models

NAME = "messages"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help=f"How many {NAME} do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        users = user_models.User.objects.all()
        conversations = conversation_models.Conversation.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            conversation_models.Message,
            number,
            {
                "user": lambda x: choice(users),
                "conversation": lambda x: choice(conversations),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"Create {number} {NAME}"))
