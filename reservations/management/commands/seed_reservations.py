from random import choice
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from random import randint
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from reservations import models as reservations_models


class Command(BaseCommand):

    help = "This command creates reservations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help="How many reservations do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()

        seeder = Seed.seeder()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            {
                "guest": lambda x: choice(users),
                "room": lambda x: choice(rooms),
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now() + timedelta(days=randint(1, 30)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"Create {number} rooms"))
