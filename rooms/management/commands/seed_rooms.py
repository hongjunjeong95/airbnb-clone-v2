import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models
from photos import models as photo_models


class Command(BaseCommand):

    help = "This command creates some roome types"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help="How many rooms do you want to create?"
        )

    def handle(self, *args, **options):
        number = options.get("number", 1)
        users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.company(),
                "city": lambda x: seeder.faker.city(),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 20),
                "bedrooms": lambda x: random.randint(1, 5),
                "beds": lambda x: random.randint(1, 5),
                "bathrooms": lambda x: random.randint(1, 5),
                "host": lambda x: random.choice(users),
                "room_type": lambda x: random.choice(room_types),
            },
        )
        created_rooms = seeder.execute()
        cleaned_data = flatten(created_rooms.values())

        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        house_rules = room_models.HouseRule.objects.all()

        for pk in cleaned_data:
            room = room_models.Room.objects.get(pk=pk)

            for amenity in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(amenity)

            for facility in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(facility)

            for house_rule in house_rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(house_rule)

            for i in range(10, 30):
                photo_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1,31)}.webp",
                )

        self.stdout.write(self.style.SUCCESS(f"Create {number} rooms"))
