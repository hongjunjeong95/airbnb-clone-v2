from django.core.management.base import BaseCommand
from rooms.models import HouseRule


class Command(BaseCommand):

    help = "This command creates some house rules"

    def handle(self, *args, **options):
        house_rules = [
            "No smoking.",
            "No parties or events.",
            "No pets/Pets allowed.",
            "No unregistered guests.",
            "No food or drink in bedrooms.",
            "No loud noise after 11 PM.",
        ]

        for house_rule in house_rules:
            HouseRule.objects.create(name=house_rule)

        self.stdout.write(self.style.SUCCESS("Create house rules"))
