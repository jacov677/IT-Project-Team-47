"""Create demo data so every team member starts with the same test accounts.

    python manage.py seed_demo

Only runs when DJANGO_DEBUG=True. Never use these accounts in production.
"""
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Coordinator, Mentor, Role, Student, User
from apps.logbook.models import LogbookEntry
from apps.organisations.models import HostOrganization
from apps.placements.models import Placement, PlacementStatus

DEMO_PASSWORD = "WilDemo#2026"


class Command(BaseCommand):
    help = "Create demo users, an organisation and sample placements for local development."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo only runs with DJANGO_DEBUG=True.")
        with transaction.atomic():
            self._seed()
        self.stdout.write(self.style.SUCCESS(f"Demo data ready. Every demo password is: {DEMO_PASSWORD}"))
        for email, role in [
            ("admin@wil.test", "Administrator (also Django admin site)"),
            ("coordinator@wil.test", "WIL Coordinator"),
            ("mentor@wil.test", "Mentor"),
            ("student1@wil.test", "Student with an active placement"),
            ("student2@wil.test", "Student with a pending placement"),
            ("newstudent@wil.test", "Inactive account waiting for activation"),
        ]:
            self.stdout.write(f"  {email:<24} {role}")

    def _user(self, email, role, **extra):
        user, created = User.objects.get_or_create(email=email, defaults={"role": role, **extra})
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        return user

    def _seed(self):
        self._user("admin@wil.test", Role.ADMIN, is_staff=True, is_superuser=True)

        coord_user = self._user("coordinator@wil.test", Role.COORDINATOR)
        coordinator, _ = Coordinator.objects.get_or_create(
            user=coord_user, defaults={"first_name": "Thandi", "last_name": "Mokoena", "department": "Faculty of IT"}
        )

        org, _ = HostOrganization.objects.get_or_create(
            registration_number="2015/123456/07",
            defaults={"organisation_name": "Demo Tech Solutions (Pty) Ltd", "industry": "Information Technology",
                      "address": "12 Main Road, Pretoria", "contact_email": "hr@demotech.test"},
        )

        mentor_user = self._user("mentor@wil.test", Role.MENTOR)
        mentor, _ = Mentor.objects.get_or_create(
            user=mentor_user, defaults={"organisation": org, "first_name": "Sipho", "last_name": "Dlamini",
                                        "job_title": "Senior Developer", "contact_number": "012 555 0100"}
        )

        s1_user = self._user("student1@wil.test", Role.STUDENT)
        s1, _ = Student.objects.get_or_create(
            student_number="STU0001", defaults={"user": s1_user, "first_name": "Lerato", "last_name": "Nkosi",
                                                "qualification": "BSc Information Technology"}
        )
        s2_user = self._user("student2@wil.test", Role.STUDENT)
        s2, _ = Student.objects.get_or_create(
            student_number="STU0002", defaults={"user": s2_user, "first_name": "Ayanda", "last_name": "Zulu",
                                                "qualification": "BSc Information Technology"}
        )
        new_user = self._user("newstudent@wil.test", Role.STUDENT, is_active=False)
        Student.objects.get_or_create(
            student_number="STU0003", defaults={"user": new_user, "first_name": "Naledi", "last_name": "Khumalo",
                                                "qualification": "Diploma in IT"}
        )

        today = timezone.localdate()
        active, created = Placement.objects.get_or_create(
            student=s1, organisation=org,
            defaults={"mentor": mentor, "coordinator": coordinator, "start_date": today - timedelta(days=21),
                      "end_date": today + timedelta(days=150), "status": PlacementStatus.ACTIVE,
                      "approved_at": timezone.now() - timedelta(days=25)},
        )
        if created:
            for days_ago, hours, signed in [(14, "8.00", True), (13, "7.50", True), (7, "8.00", False), (6, "6.00", False)]:
                LogbookEntry.objects.create(
                    placement=active, entry_date=today - timedelta(days=days_ago), hours_worked=Decimal(hours),
                    description="Worked on the support ticket system and attended the team stand-up.",
                    mentor_signed_off=signed, signed_off_at=timezone.now() if signed else None,
                )

        Placement.objects.get_or_create(
            student=s2, organisation=org,
            defaults={"mentor": mentor, "coordinator": coordinator, "start_date": today + timedelta(days=14),
                      "end_date": today + timedelta(days=180), "status": PlacementStatus.PENDING},
        )
