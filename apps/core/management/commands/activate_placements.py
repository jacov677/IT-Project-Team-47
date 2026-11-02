"""Daily job: approved placements become active on their start date.

Schedule with cron on the server, e.g.  5 0 * * *  python manage.py activate_placements
"""
from django.core.management.base import BaseCommand

from apps.placements.services import activate_due_placements


class Command(BaseCommand):
    help = "Set approved placements whose start date has arrived to active."

    def handle(self, *args, **options):
        count = activate_due_placements()
        self.stdout.write(self.style.SUCCESS(f"{count} placement(s) activated."))
