from django.core.management.base import BaseCommand
from random import choice, randint
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reviews import models as review_models

NAME = "reviews"


class Command(BaseCommand):

    help = f"This command creates {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help=f"How many {NAME} do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "user": lambda x: choice(users),
                "room": lambda x: choice(rooms),
                "accuracy": lambda x: randint(1, 5),
                "communication": lambda x: randint(1, 5),
                "cleanliness": lambda x: randint(1, 5),
                "location": lambda x: randint(1, 5),
                "check_in": lambda x: randint(1, 5),
                "value": lambda x: randint(1, 5),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"Create {number} {NAME}"))
