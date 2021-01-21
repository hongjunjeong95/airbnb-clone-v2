from django.core.management.base import BaseCommand
from rooms.models import RoomType


class Command(BaseCommand):

    help = "This command creates some room types"

    def handle(self, *args, **options):
        room_types = ["Hotel Room", "Entire Place", "Shared Room", "Private Room"]
        for room_type in room_types:
            RoomType.objects.create(name=room_type)

        self.stdout.write(self.style.SUCCESS("Create room types"))
