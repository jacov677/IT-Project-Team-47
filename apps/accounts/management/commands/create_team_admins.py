"""
Create an administrator account for every team member, for local testing.

Usage:
    python manage.py create_team_admins
    python manage.py create_team_admins --password "MyTestPass#2026"

Each account is a superuser with the Admin role, so it can open /admin/,
approve students and see every page. Running it again updates the
existing accounts instead of making duplicates.
"""
from getpass import getpass

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()

TEAM = [
    ("Jaco", "van Niekerk", "jaco@team47.test"),
    ("Amikar", "Motilal", "amikar@team47.test"),
    ("Percy", "Maile", "percy@team47.test"),
    ("Khaya", "Cele", "khaya@team47.test"),
    ("Khanya", "Khoza", "khanya@team47.test"),
    ("Tshepo", "Hlelesi", "tshepo@team47.test"),
]


class Command(BaseCommand):
    help = "Create an admin account for every team member (development only)."

    def add_arguments(self, parser):
        parser.add_argument("--password", help="Password for all team admin accounts. Asked for if left out.")

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Team admin accounts are for development only (DJANGO_DEBUG must be True).")

        password = options["password"] or getpass("Password for the team admin accounts: ")
        try:
            validate_password(password)
        except ValidationError as error:
            raise CommandError(" ".join(error.messages))

        for first, last, email in TEAM:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": email, "first_name": first, "last_name": last},
            )
            user.username = email
            user.role = User.Role.ADMIN
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(f"{'Created' if created else 'Updated'}: {email}")

        self.stdout.write(self.style.SUCCESS(f"{len(TEAM)} team admin accounts ready. Log in at /accounts/login/ with the email."))
