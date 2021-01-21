from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from users.models import User


class Command(BaseCommand):

    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, help="How many users do you want to create"
        )

    def handle(self, *args, **options):
        try:
            number = options.get("number", 1)
            seeder = Seed.seeder()
            seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
            seeder.execute()
            self.stdout.write(self.style.SUCCESS(f"Create {number} users"))
        except CommandError:
            print("error")